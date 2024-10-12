from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.usuario.models import Usuario
from .utils import Auth
from rest_framework.permissions import AllowAny
from django.utils import timezone
import datetime


class LoginView(APIView):
    permission_classes = [AllowAny]  # Permitir el acceso a todos

    def post(self, request):
        try:
            # Obtener los datos enviados
            request_user = request.data.get("user")
            request_password = request.data.get("password")

            # Verificar si el usuario existe
            usuario = Usuario.objects.get(
                user=request_user, is_status=True, is_active=True
            )

            # Verificar si la contraseña es correcta
            if Auth.check_password(request_password, usuario.password):
                usuario.last_login = timezone.now()
                usuario.save()

                # Generar tokens JWT
                refresh = RefreshToken.for_user(usuario)
                access_token = refresh.access_token
                access_token_expiration = access_token[
                    "exp"
                ]  # Tiempo  unix en segundos

                return Response(
                    {
                        "access_auth": {
                            "refresh_token": str(refresh),
                            "access_token": str(access_token),
                            "access_token_expiration": access_token_expiration,
                        },
                        "detail": "OK",
                        "api_status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "detail": "Credenciales incorrectas.",
                        "api_status": False,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except Usuario.DoesNotExist:
            return Response(
                {
                    "detail": "Credenciales incorrectas. efeaf",
                    "api_status": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return Response(
                {
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
