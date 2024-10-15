from apps.usuario.models import Usuario
from django.db import models

class Estudiante(models.Model):
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    ci = models.CharField(max_length=100)
    ci_expedido = models.CharField(max_length=20)
    genero = models.CharField(max_length=20)
    fecha_nacimiento= models.DateField()
    numero_contacto = models.CharField(max_length=100)
    direccion = models.CharField(max_length=300)
    
    matricula_univ = models.CharField(max_length=100)
    internado_rot = models.CharField(max_length=255)
    # por defecto blank=False indica que debe ser obligatorio en json y formularios django
    obervaciones = models.CharField(max_length=400, null=True, blank=True) 
    
    is_status = models.BooleanField(default=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.nombres
    
