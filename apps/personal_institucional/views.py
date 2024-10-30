from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.authentication.jwt_authentication import CustomJWTAuthentication

from rest_framework.parsers import MultiPartParser
from .serializers import UsuarioPersonalInstSerializer
from .models import PersonalInstitucional

from .utils import process_nested_form_data
from apps.usuario.permissions import (
    CreatePersonalInstPermission,
    UpdatePersonalInstPermission,
    DeletePersonalInstPermission,
)


class UsuarioPersonalInstListCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, CreatePersonalInstPermission]
    parser_classes = [MultiPartParser]

    def get(self, request):
        try:
            # PersonalInstitucional ya tiene una relacion uno a uno con Usuarios por lo cual ya vienen los datos
            # de usuarios
            user_personal_inst = PersonalInstitucional.objects.filter(
                is_status=True, usuario__is_status=True
            )
            serializer = UsuarioPersonalInstSerializer(user_personal_inst, many=True)

            return Response(
                {
                    "payload": serializer.data,
                    "detail": "OK",
                    "api_status": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"payload": [], "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            process_data = process_nested_form_data(request.data)

            serializer = UsuarioPersonalInstSerializer(data=process_data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "api_status": True,
                        "detail": "Registo creado.",
                        "payload": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "api_status": False,
                        "payload": {},
                        "serializer_errors": serializer.errors,
                        "detail": "Verificar los campos.",
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        except Exception as e:
            return Response(
                {"payload": {}, "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UsuarioPersonalInstUpdateDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        # Aplicar permisos según el método de la solicitud
        if self.request.method == "PUT":
            self.permission_classes = [UpdatePersonalInstPermission]
        elif self.request.method == "DELETE":
            self.permission_classes = [DeletePersonalInstPermission]

        # Llama al método base para obtener los permisos
        return super().get_permissions()

    def put(self, request, uuid):
        try:
            # Verificamos si el registro existe
            exists_user_personal_inst = PersonalInstitucional.objects.filter(
                is_status=True, usuario__is_status=True, usuario__uuid=uuid
            ).exists()

            if not exists_user_personal_inst:
                return Response(
                    {
                        "payload": {},
                        "detail": "Registro no encontrado.",
                        "api_status": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            data = request.data.copy()
            # si no tenemos password eliminams el campo
            # si es update serializer indicara que dicho campo no debe ser vacio
            if data.get("usuario[password]") in [None, ""]:
                data.pop("usuario[password]")

            process_data = process_nested_form_data(data)

            # Ya no necesitamos verificar el is_status, se verifico arriba
            usuario_personal_inst = PersonalInstitucional.objects.get(
                usuario__uuid=uuid
            )
            serializer = UsuarioPersonalInstSerializer(
                instance=usuario_personal_inst, data=process_data, partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "payload": serializer.data,
                        "detail": "Registro actualizado.",
                        "api_status": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "payload": {},
                        "detail": "Verificar los campos.",
                        "serializer_errors": serializer.errors,
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
            # Personal institucional ya estan relacionados (uno a uno)
            exists_user_personal_inst = PersonalInstitucional.objects.filter(
                is_status=True, usuario__is_status=True, usuario__uuid=uuid
            ).exists()

            if not exists_user_personal_inst:
                return Response(
                    {"detail": "Registro no encontrado. ", "api_status": False},
                    status=status.HTTP_404_NOT_FOUND,
                )

            user_personal_inst = PersonalInstitucional.objects.get(usuario__uuid=uuid)
            user_personal_inst.is_status = False
            user_personal_inst.save()

            user_personal_inst.usuario.is_status = False
            user_personal_inst.usuario.is_active = False
            user_personal_inst.usuario.save()

            return Response(
                {"detail": "Registro eliminado.", "api_status": True},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"payload": {}, "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
