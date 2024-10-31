from apps.usuario.models import Usuario
from django.db import models
import uuid

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, primary_key=True, on_delete=models.CASCADE, related_name='estudiante')    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    ci = models.CharField(max_length=100)
    ci_complemento = models.CharField(max_length=20, blank=True, null=True)
    ci_expedido = models.CharField(max_length=20)
    genero = models.CharField(max_length=20)
    fecha_nacimiento= models.DateField()
    numero_contacto = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    
    matricula_univ = models.CharField(max_length=50)
    internado_rot = models.CharField(max_length=100)
    # por defecto blank=False indica que debe ser obligatorio en json y formularios django
    observaciones = models.CharField(max_length=300, null=True, blank=True) 
    
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
