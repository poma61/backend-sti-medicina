from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.authentication.jwt_authentication import CustomJWTAuthentication

from rest_framework.parsers import MultiPartParser
from .serializers import UsuarioPersonalInstSerializer
from .models import PersonalInstitucional


class UsuarioPersonalInstListCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
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
            data = request.data

            usuario_data = {
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
                "cargo": data.get("matricula_univ"),
                "grado_academico": data.get("grado_academico"),
                "observaciones": data.get("observaciones"),
            }
            serializer = UsuarioPersonalInstSerializer(data=reorganized_data)
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    parser_classes = [MultiPartParser]

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
                "cargo": data.get("cargo"),
                "grado_academico": data.get("grado_academico"),
                "observaciones": data.get("observaciones"),
            }

            # Ya no necesitamos verificar el is_status, se verifico arriba
            usuario_personal_inst = PersonalInstitucional.objects.get(usuario__uuid=uuid)
            serializer = UsuarioPersonalInstSerializer(
                instance=usuario_personal_inst, data=reorganized_data, partial=True
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

            user_personal_inst = PersonalInstitucional.objects.get(
                usuario__uuid=uuid
            )
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
