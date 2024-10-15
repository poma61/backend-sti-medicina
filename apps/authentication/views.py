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

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .jwt_authentication import CustomJWTAuthentication

from .serializers import AuthUsuarioSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]  # Permitir el acceso a todos

    def post(self, request):
        try:
            # Obtener los datos enviados
            request_user = request.data.get("user")
            request_password = request.data.get("password")

            # Verificar si el usuario existe
            exists_usuario = Usuario.objects.filter(
                user=request_user, is_status=True, is_active=True
            ).exists()
            if not exists_usuario:
                return Response(
                    {
                        "detail": "Credenciales incorrectas.",
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

                return Response(
                    {
                        "access_auth": {
                            "refresh_token": str(refresh),
                            "access_token": str(access_token),
                            "access_token_expiration": access_token[
                                "exp"
                            ],  # Tiempo  unix en segundos
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
        except Exception as e:
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
            # Otra forma
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
            #     .first() # el primer dato
            # )
            # # Para acceder a un dato
            # picture = estudiante["usuario__picture"]
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
                    "is_data": {
                        "user": estudiante_or_personal_inst.usuario.user,
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
                {"is_data": {}, "detail": str(e), "api_status": False},
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

            #  partial=True =>  indica que por json se pueden enviar solo algunos campos
            #  si no tiene ese parametro, entonces serializer indicara que todos los campos son obligatorios
            # usuario_serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
            usuario_serializer = AuthUsuarioSerializer(usuario, data=request.data,partial=True)

            if usuario_serializer.is_valid():
                usuario_serializer.save()  # Internamente llama a la funcion update
                return Response(
                    {
                        "is_data": usuario_serializer.data,
                        "detail": "Registro actualizado.",
                        "api_status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "is_data": {},
                        "serializer_errors": usuario_serializer.errors,
                        "detail": "Verificar los campos.",
                        "api_status": False,
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        except Exception as e:
            return Response(
                {
                    "is_data": {},
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
