from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from .core import ModelProcessor
from .models import ModeloEntrenado
from rest_framework.authtoken.models import Token
import os
import pickle
import pandas as pd
from pycaret.classification import predict_model
# Registro
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Vistas protegidas-------------------------------
class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        file = request.FILES.get('file')
        target = request.data.get('target')
        ignore = request.data.get('ignore')
        processing = request.data.get('processing')

        # Verifica si el archivo y los parámetros están presentes
        if not file:
            return Response({'error': 'No se ha enviado archivo.'}, status=status.HTTP_400_BAD_REQUEST)

        if target is None:
            return Response({'error': 'Target debe ser indicado.'}, status=status.HTTP_400_BAD_REQUEST)

        if processing not in ["time-series", "classification", "regression"]:
            return Response({'error': 'Procesamiento no valido.'}, status=status.HTTP_400_BAD_REQUEST)
        # Guarda el archivo (puedes usar almacenamiento en S3)
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        filename_sin_extension = os.path.splitext(filename)[0]

        model = ModelProcessor(processing, target, ignore, filename_sin_extension)
        modelo_entrenado = model.process()

        # Serializa el modelo entrenado
        modelo_entrenado_serializado = pickle.dumps(modelo_entrenado)

        modelo_entrenado_db = ModeloEntrenado.objects.create(
            modelo=modelo_entrenado_serializado,
            usuario=request.user
        )

        return Response({'modelo_id': modelo_entrenado_db.id}, status=status.HTTP_201_CREATED)


class PredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        modelo_id = request.data.get('modelo_id')
        params = request.data.get('params')

        modelo = self._obtener_modelo(modelo_id)
        if not modelo:
            return Response({'error': 'Modelo no encontrado o inválido'}, status=404)

        # Validar parámetros de entrada
        if not self._validar_parametros(modelo, params):
            return Response({'error': 'Parámetros inválidos o incompletos'}, status=400)

        # Hacer predicción
        try:
            data_nueva = pd.DataFrame([params])
            predicciones = modelo.predict(data_nueva)
            return Response({'predicción': predicciones.tolist()}, status=200)
        except Exception as e:
            return Response({'error': f'Error al hacer la predicción: {str(e)}'}, status=500)

    def _obtener_modelo(self, modelo_id):
        """Obtiene y deserializa el modelo entrenado."""
        try:
            modelo_entrenado = ModeloEntrenado.objects.get(id=modelo_id)
            return pickle.loads(modelo_entrenado.modelo)
        except (ModeloEntrenado.DoesNotExist, pickle.UnpicklingError):
            return None

    def _validar_parametros(self, modelo, params):
        """Verifica que los parámetros coincidan con los esperados por el modelo."""
        try:
            features_esperados = modelo.feature_names_in_
            print("Parámetros esperados por el modelo:", features_esperados)
            return all(key in params for key in features_esperados)
        except AttributeError:
            return False