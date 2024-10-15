from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer
from .models import Usuario
from apps.estudiante.models import Estudiante
from rest_framework.permissions import IsAuthenticated
from  apps.authentication.jwt_authentication import CustomJWTAuthentication

# Todas estas clases se deben crear usuario tambien se debe crear estudiantes al mismo tiempo
# Cada una debe ir a la App de EStudiante  Y No estar en la app Usuario

class UsuarioListCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]  # Requiere autenticación con JWT
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):
        try:
            usuarios = Usuario.objects.filter(is_status=True)
            serializer = UsuarioSerializer(usuarios, many=True)

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
            serializer = UsuarioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "is_data": serializer.data,
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
                        "serializer_errors": serializer.errors,
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


class UsuarioUpdateDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication]  # Requiere autenticación con JWT
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    def put(self, request, id):
        try:
            usuario = Usuario.objects.get(id=id, is_status=True)
            serializer = UsuarioSerializer(usuario, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "is_data": serializer.data,
                        "detail": "Registro actualizado.",
                        "api_status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "is_data": {},
                        "serializer_errors": serializer.errors,
                        "detail": "Verificar los campos.",
                        "api_status": True,
                    },
                    status=status.HTTP_200_OK,
                )
        except Usuario.DoesNotExist:
            return Response(
                {
                    "is_data": {},
                    "detail": "Registro no encontrado.",
                    "api_status": False,
                },
                status=status.HTTP_404_NOT_FOUND,
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

   # Esta funcion No es necesario ya que se eliminara el usuario al eliminar el estudiante
    def delete(self, request, id):
        try:
            
            user = Usuario.objects.get(id=id, is_status=True)
            user.is_status = False
            user.save()
            
            # NOTA ************************** Eliminar tambien al estudiante
            

            return Response(
                {
                    "detail": "Registro eliminado.",
                    "api_status": True,
                },
                status=status.HTTP_200_OK
            )

        except Usuario.DoesNotExist:
            return Response(
                {
                    "detail": "Registro no encontrado.",
                    "api_status": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {
                    "detail": str(e),
                    "api_status": False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
