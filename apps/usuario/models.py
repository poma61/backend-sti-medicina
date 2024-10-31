from django.db import models
from django.utils.crypto import get_random_string
import uuid
import os


def user_profile_directory_path(instance, filename):
    # Limpia el nombre del archivo para evitar path traversal, conserva el nombre del archivo 
    # tambien tiene el tipo de archivo
    filename = os.path.basename(filename)

    unique_filename = (
        f"{get_random_string(length=10)}_{instance.user}_{filename}"
    )
    user_directory = "usuario/"
    # Devuelve la ruta donde se guardará la nueva imagen
    return os.path.join(user_directory, unique_filename)


class Permiso(models.Model):
    module = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_type = models.CharField(max_length=100)
    is_type_content = models.CharField(max_length=100)
    code = models.CharField(max_length=100)


class Usuario(models.Model):
    options_user_types = (
        ("estudiante", "Estudiante"),
        ("doctor", "Doctor(a)"),
        ("administrativo", "Administrativo"),
    )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField()
    user_type = models.CharField(max_length=50, choices=options_user_types)
    picture = models.ImageField(
        default="usuario/default_profile.png",
        upload_to=user_profile_directory_path,
        blank=True,
        null=True,
    )
    # Campo para almacenar la última fecha de inicio de sesión
    last_login = models.DateTimeField(null=True, blank=True)
    permisos = models.ManyToManyField(Permiso, related_name="usuario", blank=True)

    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = "user"

    REQUIRED_FIELDS = []

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
