from django.db import models
from django.contrib.auth.models import User

class ModeloEntrenado(models.Model):
    modelo = models.BinaryField()  
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Modelo entrenado por {self.usuario.username} el {self.fecha_creacion}"

