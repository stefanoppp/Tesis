from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
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

# Vistas protegidas
class MainPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Ingresado exitosamente! Usuario, {request.user.username}!"}, status=status.HTTP_200_OK)

class UploadFileView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        # Obtén el archivo y los parámetros numéricos
        file = request.FILES.get('file')
        param1 = request.data.get('param1')
        param2 = request.data.get('param2')

        # Verifica si el archivo y los parámetros están presentes
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if param1 is None or param2 is None:
            return Response({'error': 'Both param1 and param2 must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Aquí puedes agregar validaciones para los parámetros numéricos si es necesario

        # Guarda el archivo (puedes usar almacenamiento en S3)
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        
        # Llama a tu proceso de IA aquí, pasando los parámetros
        # process_data(filename, param1, param2)

        return Response({'message': 'File uploaded successfully', 'filename': filename, 'param1': param1, 'param2': param2}, status=status.HTTP_201_CREATED)