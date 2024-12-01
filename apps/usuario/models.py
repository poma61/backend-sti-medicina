from django.db import models
from django.utils.crypto import get_random_string
import uuid
import os
from apps.authentication.utils import Auth

def user_profile_directory_path(instance, filename):
    # Limpia el nombre del archivo para evitar path transversal, conserva el nombre del archivo
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

class UsuarioManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(user=username)

    def create_user(self, user, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        email = self.normalize_email(email)
        usuario = self.model(user=user, email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, user, email, password=None, **extra_fields):
        # Establece los campos necesarios para un superusuario
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError("El superusuario debe tener una contraseña")
        return self.create_user(user, email, password, **extra_fields)

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
    is_staff =  models.BooleanField(default=False) 
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
    permisos = models.ManyToManyField(
        Permiso, related_name="usuario", blank=True)

    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = "user"

    REQUIRED_FIELDS = ["email"]

    objects = UsuarioManager()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_superuser(self):
        return True
    
    def check_password(self, raw_password):
        """
        Verifica si la contraseña proporcionada coincide con la contraseña cifrada almacenada.
        """
        return Auth.check_password(raw_password, self.password)

    def set_password(self, raw_password):
        """
        Cifra y establece la contraseña proporcionada.
        """
        self.password = Auth.encrypt_password(raw_password)

    def __str__(self):
        return self.user

    # Métodos de permisos
    def has_perm(self, perm, obj=None):
        """
        Devuelve True si el usuario tiene el permiso especificado.
        """
        return self.is_staff  

    def has_module_perms(self, app_label):
        """
        Devuelve True si el usuario tiene permisos para un módulo específico.
        """
        return self.is_staff  

    def get_group_permissions(self):
        """
        Devuelve los permisos de grupo del usuario.
        """
        return set()  
    


