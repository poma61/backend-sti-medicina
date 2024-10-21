from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.authentication.jwt_authentication import CustomJWTAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser

from .models import Estudiante

from .serializers import UsuarioEstudianteSerializer


class UsuarioEstListCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request, format=None):
        try:
            # Estudiante tiene una relacion uno a uno con Usuario por esa razon ya estan relacionadas
            user_and_estudiants = Estudiante.objects.filter(
                is_status=True, usuario__is_status=True
            )

            serializer = UsuarioEstudianteSerializer(user_and_estudiants, many=True)

            return Response(
                {"payload": serializer.data, "detail": "OK", "api_status": True},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"payload": [], "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, format=None):
        try:
            data = request.data

            usuario_data = {
                "id": data.get("usuario[id]"),
                "user": data.get("usuario[user]"),
                "password": data.get("usuario[password]"),
                "email": data.get("usuario[email]"),
                "is_active": data.get("usuario[is_active]"),
                "user_type": data.get("usuario[user_type]"),
            }

            if data.get("usuario[picture]"):
                usuario_data["picture"] = data.get("usuario[picture]")

            # Crear un nuevo diccionario con los datos correctos
            reorganized_data = {
                "usuario": usuario_data,
                "nombres": data.get("nombres"),
                "apellido_paterno": data.get("apellido_paterno"),
                "apellido_materno": data.get("apellido_materno"),
                "ci": data.get("ci"),
                "ci_expedido": data.get("ci_expedido"),
                "genero": data.get("genero"),
                "fecha_nacimiento": data.get("fecha_nacimiento"),
                "numero_contacto": data.get("numero_contacto"),
                "direccion": data.get("direccion"),
                "matricula_univ": data.get("matricula_univ"),
                "internado_rot": data.get("internado_rot"),
                "observaciones": data.get("observaciones"),
            }
            est_usuario_serializer = UsuarioEstudianteSerializer(data=reorganized_data)

            if est_usuario_serializer.is_valid():
                est_usuario_serializer.save()
                return Response(
                    {
                        "payload": est_usuario_serializer.data,
                        "detail": "Registro creado.",
                        "api_status": True,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "payload": {},
                        "detail": "Verificar los campos!",
                        "serializer_errors": est_usuario_serializer.errors,
                        "api_status": False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
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


class UsuarioEstUpdateDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication]  # Requiere autenticación con JWT
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    parser_classes = [MultiPartParser]

    def put(self, request, uuid):
        try:
            # Estudiante tiene una relacion uno a uno con Usuario por esa reazon ya estan relacionadas
            exists_est_and_usuario = Estudiante.objects.filter(
                usuario__uuid=uuid, usuario__is_status=True, is_status=True
            ).exists()

            if not exists_est_and_usuario:
                return Response(
                    {
                        "payload": {},
                        "detail": "Registro no encontrado",
                        "api_status": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Buscar el estudiante que se quiere actualizar
            usuario_est = Estudiante.objects.get(usuario__uuid=uuid)

            data = request.data
            usuario_data = {
                "id": data.get("usuario[id]"),
                "user": data.get("usuario[user]"),
                "email": data.get("usuario[email]"),
                "is_active": data.get("usuario[is_active]"),
                "user_type": data.get("usuario[user_type]"),
            }

            # Verifica si el valor NO es  None o vacio
            if data.get("usuario[password]"):
                usuario_data["password"] = data.get("usuario[password]")
            # Verifica si el valor NO es  None o vacio
            if data.get("usuario[picture]"):
                usuario_data["picture"] = data.get("usuario[picture]")

            # Crear un nuevo diccionario con los datos correctos
            reorganized_data = {
                "usuario": usuario_data,
                "nombres": data.get("nombres"),
                "apellido_paterno": data.get("apellido_paterno"),
                "apellido_materno": data.get("apellido_materno"),
                "ci": data.get("ci"),
                "ci_expedido": data.get("ci_expedido"),
                "genero": data.get("genero"),
                "fecha_nacimiento": data.get("fecha_nacimiento"),
                "numero_contacto": data.get("numero_contacto"),
                "direccion": data.get("direccion"),
                "matricula_univ": data.get("matricula_univ"),
                "internado_rot": data.get("internado_rot"),
                "observaciones": data.get("observaciones"),
            }

            est_usuario_serializer = UsuarioEstudianteSerializer(
                instance=usuario_est,
                data=reorganized_data,
                partial=True,
            )

            if est_usuario_serializer.is_valid():
                est_usuario_serializer.save()
                return Response(
                    {
                        "payload": est_usuario_serializer.data,
                        "detail": "Registro actualizado.",
                        "api_status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "payload": {},
                        "serializer_errors": est_usuario_serializer.errors,
                        "detail": "Verificar los campos.",
                        "api_status": False,
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        except Exception as e:
            return Response(
                {"payload": {}, "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, uuid):
        try:
            # Veriricamos si estudiante existe
            exists_user_estudiante = Estudiante.objects.filter(
                is_status=True, usuario__is_status=True, usuario__uuid=uuid
            ).exists()
            if not exists_user_estudiante:
                return Response(
                    {"detail": "Registro no encontrado.", "api_status": False},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Estudiante tiene una relacion uno a uno con Usuario por esa reazon ya estan relacionadas
            estudiante = Estudiante.objects.get(usuario__uuid=uuid)
            estudiante.is_status = False
            estudiante.save()

            estudiante.usuario.is_status = False
            estudiante.usuario.is_active = False
            estudiante.usuario.save()

            return Response(
                {"detail": "Registro eliminado.", "api_status": True},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
