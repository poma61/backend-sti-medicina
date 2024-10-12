from django.db import models
from django.conf import settings
import os
from django.contrib.auth.hashers import make_password, check_password

# Código para las imágenes del usuario 
def user_profile_directory_path(instance, filename):
    profile_picture_name = 'usuario/{0}/profile.jpg'.format(instance.user)
    path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(path):
        os.remove(path)


class Usuario(models.Model):
    options_user_types = ( 
        ('estudiante', 'Estudiante'),
        ('doctor', 'Doctor(a)'),
        ('administrativo', 'Administrativo')
    )
    user = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField()  
    is_status = models.BooleanField(default=True)  
    user_type = models.CharField(max_length=50, choices=options_user_types)
    picture = models.ImageField(default='/media/usuario/profile.png', upload_to=user_profile_directory_path, verbose_name='Picture')
    last_login = models.DateTimeField(null=True, blank=True)  # Campo para almacenar la última fecha de inicio de sesión
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'user'
    
    REQUIRED_FIELDS = []
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
