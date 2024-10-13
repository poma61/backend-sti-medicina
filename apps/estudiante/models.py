from django.db import models
from apps.usuario.models import Usuario

class Estudiante(models.Model):
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    matricula = models.CharField(max_length=100)
    is_status = models.BooleanField(default=True)
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombres
    
