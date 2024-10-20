from django.db import models
from django.conf import settings
import os
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
import uuid

def user_profile_directory_path(instance, filename):
    return filename
    # Limpia el nombre del archivo para evitar path traversal, conserva el nombre del archivo
    filename = os.path.basename(filename)

    unique_filename = (
        f"{get_random_string(length=10)}_{get_random_string(length=10)}_{filename}"
    )
    user_directory = "usuario/"

    # Comprobar si la carpeta del usuario existe y crearla si no
    user_directory_path = os.path.join(settings.MEDIA_ROOT, user_directory)
    if not os.path.exists(user_directory_path):
        os.makedirs(user_directory_path)

    # Devuelve la ruta donde se guardará la nueva imagen
    return os.path.join(user_directory, unique_filename)


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
    )
    last_login = models.DateTimeField(
        null=True, blank=True
    )  # Campo para almacenar la última fecha de inicio de sesión
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    USERNAME_FIELD = "user"

    REQUIRED_FIELDS = []

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
