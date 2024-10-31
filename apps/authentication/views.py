from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Auth
from django.utils import timezone
import datetime

from apps.estudiante.models import Estudiante
from apps.personal_institucional.models import PersonalInstitucional
from apps.usuario.models import Usuario
from apps.usuario.serializers import PermisoSerializer

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken

from .jwt_authentication import CustomJWTAuthentication
from .serializers import AuthUsuarioSerializer
import jwt

from django.conf import settings

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Procesa la solicitud con en  metodo axistente
            get_access_token = super().post(request, *args, **kwargs)
            access_token = get_access_token.data["access"]

            # Decodificar el token para obtener el campo de expiración
            decoded_access_token = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            access_token_expiration = decoded_access_token["exp"]

            # Personalizamos la respuesta
            return Response(
                {
                    "new_access_token": access_token,
                    "access_token_expiration": access_token_expiration,
                    "api_status": True,
                    "detail": "Token de acceso renovado exitosamente.",
                },
                status=status.HTTP_200_OK,
            )
        except InvalidToken as e:
            # En caso de error de token
            return Response(
                {"api_status": False, "detail": "Refresh token no válido."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            # Otro error
            return Response(
                {"api_status": False, "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    permission_classes = [AllowAny]  # Permitir el acceso a todos

    def post(self, request):
        try:
            # Obtener los datos enviados
            request_user = request.data.get("user")
            request_password = request.data.get("password")

            # Verificar si el usuario existe
            exists_usuario = Usuario.objects.filter(
                user=request_user,
                is_status=True,
            ).exists()
            if not exists_usuario:
                return Response(
                    {
                        "detail": "Credenciales incorrectas.",
                        "api_status": False,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Verificar si esta deshabilitado
            exists_usuario = Usuario.objects.filter(
                user=request_user, is_active=False
            ).exists()
            if exists_usuario:
                return Response(
                    {
                        "detail": "El usuario fue deshabilitado; contactese con el administrador del sistema.",
                        "api_status": False,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

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

                # tiempos de expiración
                access_token_expiration = access_token[
                    "exp"
                ]  # Expiración del access token
                refresh_token_expiration = refresh[
                    "exp"
                ]  # Expiración del refresh token

                return Response(
                    {
                        "access_token": str(access_token),
                        "refresh_token": str(refresh),
                        "access_token_expiration": access_token_expiration,  # Tiempo  unix en segundos desde 1970,
                        "refresh_token_expiration": refresh_token_expiration,
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
        except Exception as e:
            return Response(
                {
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")

            # Revocar token
            RefreshToken(refresh_token).blacklist()

            return Response(
                {
                    "detail": "Logout exitoso.",
                    "api_status": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as es:
            return Response(
                {
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserAuthDataView(APIView):
    # CustomJWTAuthentication verifica si el usuairo fue eliminado
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            auth_user = Auth.user(request)

            if auth_user.user_type == "estudiante":
                estudiante_or_personal_inst = Estudiante.objects.select_related(
                    "usuario"
                ).get(usuario__id=auth_user.id)
            else:
                estudiante_or_personal_inst = (
                    PersonalInstitucional.objects.select_related("usuario").get(
                        usuario__id=auth_user.id
                    )
                )
            return Response(
                {
                    "payload": {
                        "user": estudiante_or_personal_inst.usuario.user,
                        "user_type": estudiante_or_personal_inst.usuario.user_type,
                        "nombres": estudiante_or_personal_inst.nombres,
                        "apellido_paterno": estudiante_or_personal_inst.apellido_paterno,
                        "apellido_materno": estudiante_or_personal_inst.apellido_materno,
                        "ci": estudiante_or_personal_inst.ci,
                        "ci_expedido": estudiante_or_personal_inst.ci_expedido,
                        "numero_contacto": estudiante_or_personal_inst.numero_contacto,
                        "email": estudiante_or_personal_inst.usuario.email,
                        "direccion": estudiante_or_personal_inst.direccion,
                        "picture": estudiante_or_personal_inst.usuario.picture.url,
                    },
                    "detail": "OK",
                    "api_status": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"payload": {}, "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserPermission(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = Auth.user(request)
            permisos = user.permisos.all()

            serializer = PermisoSerializer(permisos, many=True)
            # Extraemos solo los códigos de cada permiso en una lista
            permisos_codes = [permiso["code"] for permiso in serializer.data]

            return Response(
                {
                    "payload": permisos_codes,
                    "detail": "OK",
                    "api_status": False,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "payload": [],
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class UserUpdateView(APIView):
    # CustomJWTAuthentication verifica si el usuairo fue eliminado (is_status)
    # JWT por defecto verifica si el usuario esta activo o no (is_active)
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Verificar si las credenciales de acceso estan bien
            user_auth = Auth.user(request)
            usuario = Usuario.objects.get(id=user_auth.id)
            request_password = request.data.get("password")

            if not Auth.check_password(request_password, usuario.password):
                return Response(
                    {
                        "detail": "Contraseña actual incorrecta.",
                        "api_status": False,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            usuario_serializer = AuthUsuarioSerializer(
                usuario, data=request.data, partial=True
            )

            if usuario_serializer.is_valid():
                usuario_serializer.save()  # Internamente llama a la funcion update
                return Response(
                    {
                        "payload": usuario_serializer.data,
                        "detail": "Registro actualizado.",
                        "api_status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "payload": {},
                        "serializer_errors": usuario_serializer.errors,
                        "detail": "Verificar los campos.",
                        "api_status": False,
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        except Exception as e:
            return Response(
                {
                    "payload": {},
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
