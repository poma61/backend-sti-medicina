from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
import re

def user_profile_directory_path(instance, filename):
    profile_picture_name = 'usuario/{0}/profile.jpg'.format(instance.user)
    path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    
    if os.path.exists(path):
        os.remove(path)


class Usuario(AbstractBaseUser):
    options_user_types = ( 
        ('estudiante', 'Estudiante'),
        ('doctor', 'Doctor(a)'),
        ('administrativo', 'Administrativo')
    )
    user = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_status = models.BooleanField(default=True)  
    user_type = models.CharField(max_length=50, choices=options_user_types)
    picture = models.ImageField(default='users/user_default_profile.png', upload_to=user_profile_directory_path, blank=True, null=True, verbose_name='Picture')
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = ['email', 'user_type']

    def __str__(self):
        return self.email

    def clean(self):
        # Sobrescribir la validación de los campos
        if not self.user:
            raise ValidationError({'user': 'El campo user es obligatorio.'})

        if len(self.password) < 8:
            raise ValidationError({'password': 'La contraseña debe tener al menos 8 caracteres.'})

        if not re.search(r'[A-Z]', self.password):
            raise ValidationError({'password': 'La contraseña debe contener al menos una letra mayúscula.'})

        if not re.search(r'\d', self.password):
            raise ValidationError({'password': 'La contraseña debe contener al menos un número.'})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password):
            raise ValidationError({'password': 'La contraseña debe contener al menos un carácter especial.'})

    def save(self, *args, **kwargs):
        # Llamar a clean antes de guardar el objeto
        self.clean()
        super().save(*args, **kwargs)
