# usuario/utils.py
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class Auth:
    @staticmethod
    def encrypt_password(raw_password):
        """Encripta la contraseña proporcionada."""
        return make_password(raw_password)

    @staticmethod
    def check_password(raw_password, hashed_password):
        """Verifica si la contraseña proporcionada coincide con la contraseña encriptada."""
        return check_password(raw_password, hashed_password)
    
    @staticmethod
    def user(request):
        return request.user
        

