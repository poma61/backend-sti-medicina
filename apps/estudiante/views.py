from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.authentication.jwt_authentication import CustomJWTAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser

from .models import Estudiante
from .utils import process_nested_form_data

from .serializers import UsuarioEstudianteSerializer

from apps.usuario.permissions import (
    CreateEstudentPermission,
    UpdateEstudentPermission,
    DeleteEstudentPermission,
)

class UsuarioEstListCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, CreateEstudentPermission]
    parser_classes = [MultiPartParser]

    def get(self, request):
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
            process_data = process_nested_form_data(request.data)

            est_usuario_serializer = UsuarioEstudianteSerializer(data=process_data)

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

    def get_permissions(self):
        # Aplicar permisos según el método de la solicitud
        if self.request.method == "PUT":
            self.permission_classes = [UpdateEstudentPermission]
        elif self.request.method == "DELETE":
            self.permission_classes = [DeleteEstudentPermission]

        # Llama al método base para obtener los permisos
        return super().get_permissions()

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

            data = request.data.copy()
            # si no tenemos password eliminams el campo
            # si es update serializer indicara que dicho campo no debe ser vacio
            if data.get("usuario[password]") in [None, ""]:
                data.pop("usuario[password]")

            process_data = process_nested_form_data(data)

            est_usuario_serializer = UsuarioEstudianteSerializer(
                instance=usuario_est,
                data=process_data,
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
