from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Sobreescribimos el método get_user para verificar el campo is_status.
        """
        # Obtenemos el usuario usando el token validado
        user = super().get_user(validated_token)
        
        # Verifica si el usuario tiene is_status en False, indicando que ha sido "eliminado"
        if not user.is_status:
            raise AuthenticationFailed('El usuario ha sido eliminado.')
        
        return user
    
    # Por defecto simple jwt verifica el campo is_active y verifica si el usuario esta activo 
    # Si No esta activo el usuario no puede hacer login
