from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.usuario.models import Usuario
from .utils import Auth
from .permission import IsActive
from .verify_user_deleted import UserNotDeleted
from rest_framework.permissions import AllowAny
from django.utils import timezone
import datetime
from apps.estudiante.models import Estudiante
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


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
                    "detail": "Credenciales incorrectas.",
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


class UserAuthenticate(APIView):
    # Requiere autenticación con JWT
    authentication_classes = [JWTAuthentication]  
    # Solo usuarios autenticados pueden acceder y usuarios que esten activos (IsActive) 
    # y que No fueron eliminados (UserNotDeleted)
    permission_classes = [IsAuthenticated, IsActive, UserNotDeleted]

    def post(self, request):
        try:
            # NOTA *************************************************************
            # Se debe verificar que tipo de usuario es 'estudiante' 'personal institucional'

            # Primera forma
            # # Devuelve el primer estudiante o None
            # estudiante = (
            #     Estudiante.objects.select_related("usuario")
            #     .filter(usuario__id=1)
            #     .values(
            #         "nombres",
            #         "apellido_paterno",
            #         "apellido_materno",
            #         "usuario__picture",
            #     )
            #     .first()
            # )
            # # Para acceder a un dato
            # picture = estudiante["usuario__picture"]

            # Segunda forma
            # relacion one to one (join)
            estudiante = Estudiante.objects.select_related("usuario").get(
                usuario__id=Auth.user(request).id
            )

            return Response(
                {
                    "is_data": {
                        "nombres": estudiante.nombres,
                        "apellido_paterno": estudiante.apellido_paterno,
                        "apellido_materno": estudiante.apellido_materno,
                        "picture": estudiante.usuario.picture.url,
                    },
                    "detail": "OK",
                    "api_status": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"is_data": [], "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
