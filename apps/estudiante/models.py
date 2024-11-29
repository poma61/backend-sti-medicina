from apps.usuario.models import Usuario
from django.db import models
import uuid
from apps.internado_rotatorio.models import Tema


class Estudiante(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="estudiante"
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    ci = models.CharField(max_length=100)
    ci_complemento = models.CharField(max_length=20, blank=True, null=True)
    ci_expedido = models.CharField(max_length=20)
    genero = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    numero_contacto = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)

    matricula_univ = models.CharField(max_length=50)
    internado_rot = models.CharField(max_length=100)
    # por defecto blank=False indica que debe ser obligatorio en json y formularios django
    observaciones = models.CharField(max_length=300, null=True, blank=True)

    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class ProgresoEstudio(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    progress = models.DecimalField(max_digits=5, decimal_places=2)
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, related_name="progreso_estudio"
    )
    tema = models.ForeignKey(
        Tema, on_delete=models.CASCADE, related_name="progreso_estudio"
    )
    ult_actualizacion = models.DateTimeField(auto_now=True)
    tiempo_est = models.TimeField()
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class CuestionarioEvaluadoOfAI(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    evaluate = models.TextField()
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class ResultadoCuestionarioTema(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    progreso_estudio = models.ForeignKey(
        ProgresoEstudio,
        on_delete=models.CASCADE,
        related_name="resultado_cuestionario_tema",
    )
    pregunta = models.CharField(max_length=400)
    respuesta = models.CharField(max_length=400, blank=True, null=True)
    cuestionario_evaluado_of_ai = models.ForeignKey(
        CuestionarioEvaluadoOfAI,
        on_delete=models.CASCADE,
        related_name="resultado_cuestionario_tema",
    )
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

