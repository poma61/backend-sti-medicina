from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.authentication.jwt_authentication import CustomJWTAuthentication

from apps.usuario.models import Usuario
from .models import Estudiante

from .serializers import UsuarioEstudianteSerializer


class UsuarioEstListCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Estudiante tiene una relacion uno a uno con Usuario por esa reazon ya estan relacionadas
            user_and_estudiants = Estudiante.objects.filter(
                is_status=True, usuario__is_status=True
            )

            serializer = UsuarioEstudianteSerializer(user_and_estudiants, many=True)

            return Response(
                {"is_data": serializer.data, "detail": "OK", "api_status": True},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"is_data": [], "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            est_usuario_serializer = UsuarioEstudianteSerializer(data=request.data)
            if est_usuario_serializer.is_valid():
                est_usuario_serializer.save()
                return Response(
                    {
                        "is_data": est_usuario_serializer.data,
                        "detail": "Registro creado.",
                        "api_status": True,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "is_data": {},
                        "detail": "Verificar los campos!",
                        "serializer_errors": est_usuario_serializer.errors,
                        "api_status": False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
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


class UsuarioEstUpdateDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication]  # Requiere autenticación con JWT
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def put(self, request, uuid):
        try:
            # Estudiante tiene una relacion uno a uno con Usuario por esa reazon ya estan relacionadas
            exists_est_and_usuario = Estudiante.objects.filter(
                usuario__uuid=uuid, usuario__is_status=True, is_status=True
            ).exists()

            if not exists_est_and_usuario:
                return Response(
                    {
                        "is_data": {},
                        "detail": "Registro no encontrado",
                        "api_status": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Buscar el estudiante que se quiere actualizar
            usuario_est = Estudiante.objects.get(usuario__uuid=uuid)

            est_usuario_serializer = UsuarioEstudianteSerializer(
                instance=usuario_est, data=request.data, partial=True
            )

            if est_usuario_serializer.is_valid():
                est_usuario_serializer.save()
                return Response(
                    {
                        "is_data": est_usuario_serializer.data,
                        "detail": "Registro actualizado.",
                        "api_status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "is_data": {},
                        "serializer_errors": est_usuario_serializer.errors,
                        "detail": "Verificar los campos.",
                        "api_status": True,
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

    def delete(self, request, uuid):
        try:
            # Estudiante tiene una relacion uno a uno con Usuario por esa reazon ya estan relacionadas
            estudiante = Estudiante.objects.get(usuario__uuid=uuid)
            estudiante.is_status = False
            estudiante.save()

            estudiante.usuario.is_status = False
            estudiante.usuario.save()

            return Response(
                {
                    "detail": "Registro eliminado.",
                    "api_status": True,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



