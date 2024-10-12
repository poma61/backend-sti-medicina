from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.usuario.models import Usuario
from .utils import Auth
from rest_framework.permissions import AllowAny
from django.utils import timezone

class LoginView(APIView):
    permission_classes = [AllowAny]  # Permitir el acceso a todos
    def post(self, request):
        try:
            # Obtener los datos enviados
            request_user = request.data.get("user")
            request_password = request.data.get("password")
        
            # Verificar si el usuario existe
            usuario = Usuario.objects.get(user=request_user, is_status=True, is_active=True)
            
            # Verificar si la contraseña es correcta
            if Auth.check_password(request_password, usuario.password):
                usuario.last_login = timezone.now()
                usuario.save()
                # Generar tokens JWT
                refresh = RefreshToken.for_user(usuario) 
                return Response({
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    'message': 'Login exitoso',
                    'api_status': True,
                }, status=status.HTTP_200_OK)
        
        except Usuario.DoesNotExist:
             return Response({
                    'message': 'Credenciales incorrectas',
                    'api_status': False,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'message': str(e),
                'api_status': False,
            }, status=status.HTTP_404_NOT_FOUND)

