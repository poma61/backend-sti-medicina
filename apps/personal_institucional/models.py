from django.db import models
from apps.usuario.models import Usuario
import uuid


class PersonalInstitucional(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="personal_institucional",
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    ci = models.CharField(max_length=100)
    ci_expedido = models.CharField(max_length=10)
    genero = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    numero_contacto = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)

    cargo = models.CharField(max_length=100)
    grado_academico = models.CharField(max_length=100)
    observaciones = models.CharField(max_length=300, null=True, blank=True)

    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
