from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.authentication.jwt_authentication import CustomJWTAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser

from apps.authentication.utils import Auth

from .models import Estudiante, ProgresoEstudio, ResultadoCuestionarioTema
from .utils import process_nested_form_data

from .serializers import (
    UsuarioEstudianteSerializer,
    ProgresoEstudioSerializer,
    ResultadoCuestionarioTemaSerializer,
    ProgresoEstudioTemaSerializer,
    CuestionarioEvaluadoOfAISerializer,
)

from datetime import datetime, time

from apps.usuario.permissions import (
    ViewEstudentPermission,
    CreateEstudentPermission,
    UpdateEstudentPermission,
    DeleteEstudentPermission,
)


class UsuarioEstListCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        # Aplicar permisos según el método de la solicitud
        if self.request.method == "GET":
            self.permission_classes = [ViewEstudentPermission]
        elif self.request.method == "POST":
            self.permission_classes = [CreateEstudentPermission]

        return super().get_permissions()

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


class ProgresoEstudioListCreateOrUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = Auth.user(request)
            if user.user_type != "estudiante":
                return Response(
                    {"detail": "El usuario no es un estudiante.", "api_status": False},
                    status=status.HTTP_403_FORBIDDEN,
                )

            progreso_estudio = ProgresoEstudio.objects.filter(
                estudiante__id=user.estudiante.id
            )
            serializer = ProgresoEstudioTemaSerializer(progreso_estudio, many=True)

            return Response(
                {"payload": serializer.data, "detail": "OK", "api_status": True},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"payload": [], "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            # Obtenemos estudiante autenticado y si no es estudiante hacemos un return

            user = Auth.user(request)
            if user.user_type != "estudiante":
                return Response(
                    {"detail": "El usuario no es un estudiante.", "api_status": False},
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data.copy()
            data["estudiante"] = user.estudiante.id

            # verificamos si ya existe el progreso
            exists_progreso_estudio = ProgresoEstudio.objects.filter(
                estudiante__id=user.estudiante.id,
                tema__id=data.get("tema"),
            ).exists()

            if exists_progreso_estudio:
                # si ya existe el progreso de estudio hacemos un update
                # pero antes verificamos valores anteriores
                progreso_estudio = ProgresoEstudio.objects.get(
                    estudiante__id=user.estudiante.id,
                    tema__id=data.get("tema"),
                )
                old_time = self.parsed_time(progreso_estudio.tiempo_est)
                new_time = self.parsed_time(data.get("tiempo_est"))

                progress = [
                    0.1,
                    0.2,
                    0.3,
                    0.4,
                    0.5,
                    0.6,
                    0.7,
                    0.8,
                ]
                # el progress 0.9 solo se aplica si termina el cuestionario (actividad)
                tiempos = [
                    self.parsed_time("00:10:00"),
                    self.parsed_time("00:20:00"),
                    self.parsed_time("00:30:00"),
                    self.parsed_time("00:40:00"),
                    self.parsed_time("01:00:00"),
                    self.parsed_time("01:20:00"),
                    self.parsed_time("01:40:00"),
                    self.parsed_time("02:00:00"),
                ]

                if new_time > tiempos[0]:
                    data["progress"] = progress[0]
                elif new_time > tiempos[1]:
                    data["progress"] = progress[1]
                elif new_time > tiempos[2]:
                    data["progress"] = progress[2]
                elif new_time > tiempos[3]:
                    data["progress"] = progress[3]
                elif new_time > tiempos[4]:
                    data["progress"] = progress[4]
                elif new_time > tiempos[5]:
                    data["progress"] = progress[5]
                elif new_time > tiempos[6]:
                    data["progress"] = progress[6]
                elif new_time > tiempos[7]:
                    data["progress"] = progress[7]

                # Si el estudiante esta siendo evaluado completamos el prorgeso al 100% (1.00)
                if data.get("finished_tema_and_question"):
                    data["progress"] = 1.00
                    serializer = ProgresoEstudioSerializer(
                        instance=progreso_estudio, data=data, partial=True
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    data_evaluation_of_ai = {"evaluate": data.get("evaluation_of_ai")}

                    self.save_tema_is_evualuate_question(
                        data.get("questionary"),
                        progreso_estudio.id,
                        data_evaluation_of_ai,
                    )

                    return Response(
                        {
                            "payload": serializer.data,
                            "detail": "Estudiante termino el tema completo y el cuestionario",
                            "api_status": True,
                            "type": "update",
                        },
                        status=status.HTTP_201_CREATED,
                    )
                # caso contrario el estudinate sigue estudiando (leendo el tema)
                # solo actualizamos si new_time(tiempo actual obtenido del frontend) es mayor que
                #  old_time (ultimo tiempo guardado en la bd)
                elif new_time > old_time:
                    serializer = ProgresoEstudioSerializer(
                        instance=progreso_estudio, data=data, partial=True
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(
                        {
                            "payload": serializer.data,
                            "detail": "Actualizando, estudiante sigue estudiando",
                            "api_status": True,
                            "type": "update",
                        },
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {
                            "detail": "Tiempo nuevo de estudio no superado.",
                            "api_status": True,
                            "type": "update",
                        },
                        status=status.HTTP_206_PARTIAL_CONTENT,
                    )
            else:
                data["progress"] = 0.05  # inizializamos el progreso en 5% (0.05)
                # si no existe un progreso de estudio hacemos un create
                serializer = ProgresoEstudioSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "payload": serializer.data,
                            "detail": "Progreso de estudio creado.",
                            "api_status": True,
                            "type": "create",
                        },
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {
                            "payload": {},
                            "detail": "Verificar los campos.",
                            "serializer_errors": serializer.errors,
                            "api_status": False,
                            "type": "create",
                        },
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )
        except Exception as e:
            return Response(
                {"payload": {}, "detail": str(e), "api_status": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def parsed_time(self, time_str):
        return datetime.strptime(str(time_str), "%H:%M:%S").time()

    # Una vez terminado el estudio guardamos el cuestionario
    def save_tema_is_evualuate_question(
        self, questionary, progreso_estudio_id, data_evaluation_of_ai
    ):
        serializer_cuestionario_evaluado_of_ai = CuestionarioEvaluadoOfAISerializer(
            data=data_evaluation_of_ai
        )
        serializer_cuestionario_evaluado_of_ai.is_valid(raise_exception=True)
        cuestionario_evaluado_of_ai = serializer_cuestionario_evaluado_of_ai.save()
        for row in questionary:
            is_data = {
                "pregunta": row["pregunta"],
                "respuesta": row["respuesta"],
                "progreso_estudio": progreso_estudio_id,
                "cuestionario_evaluado_of_ai": cuestionario_evaluado_of_ai.id,
            }
            serializer = ResultadoCuestionarioTemaSerializer(data=is_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
