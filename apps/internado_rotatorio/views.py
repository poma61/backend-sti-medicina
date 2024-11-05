from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from apps.authentication.jwt_authentication import CustomJWTAuthentication
from apps.authentication.utils import Auth

from .models import Area, Tema
from .serializers import AreaAndTemaSerializer, TemaSerializer
from .utils import create_chat_completion
from openai import OpenAI
from django.http import StreamingHttpResponse

import environ

env = environ.Env()
environ.Env.read_env()


class ListTemaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, area):
        try:
            temas = Tema.objects.filter(is_status=True, area__name=area)
            serializer = AreaAndTemaSerializer(temas, many=True)

            return Response(
                {"payload": serializer.data, "detail": "OK", "api_status": True},
                status=status.HTTP_200_OK,
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


class CreateTemaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Este metodo es para crear, pero se esta en uso
    def post(self, request):
        try:
            # convertimos en diccionario, por si pasamos multipart el is_status no se autoagrega
            data = request.data.dict()
            serializer = TemaSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "payload": serializer.data,
                        "detail": "Registor creado",
                        "api_status": True,
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


class DetailTemaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, area, uuid):
        try:
            exists_tema = Tema.objects.filter(
                is_status=True, area__name=area, uuid=uuid
            ).exists()

            if not exists_tema:
                return Response(
                    {
                        "payload": {},
                        "detail": "El tema seleccionado no existe.",
                        "api_status": False,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            # obtendemos el tema directamente por uuid ya no es necesario hacer otras verificiones
            # porque ya se iso en el codio de arriba
            temas = Tema.objects.get(uuid=uuid)
            serializer = AreaAndTemaSerializer(temas)

            return Response(
                {"payload": serializer.data, "detail": "OK", "api_status": True},
                status=status.HTTP_200_OK,
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


"""
Clase para generar cuestionario
"""


class AIGenerateQuestionsView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # verificamos si existe el tema
            exists_tema = Tema.objects.filter(uuid=request.data.get("uuid")).exists()
            if not exists_tema:
                return StreamingHttpResponse(
                    {"No existe el tema."},
                    status=404,
                )
            # obtener el tema
            tema = Tema.objects.get(uuid=request.data.get("uuid"))
            generate_questions = {"tema": tema}

            base_url = env("AI_BASE_URL")
            access_token = env("AI_ACCESS_TOKEN")

            chat_completion = create_chat_completion(
                base_url=base_url,
                access_token=access_token,
                generate_questions=generate_questions,
            )

            # Función generadora para streaming
            def generate():
                for chunk in chat_completion:
                    # Asegura de que 'choices' existe y tiene datos
                    if hasattr(chunk, "choices") and len(chunk.choices) > 0:
                        delta_content = chunk.choices[0].delta.content
                        if delta_content:  # Verificar que el contenido no esté vacío
                            yield delta_content  # Enviar el contenido como parte de la respuesta de streaming

            # Crear una respuesta de streaming
            response = StreamingHttpResponse(
                generate(), content_type="text/event-stream"
            )
            # Desactivar el buffering para streaming
            response["X-Accel-Buffering"] = "no"
            # prevent client cache
            response["Cache-Control"] = "no-cache"
            return response

        except Exception as e:
            return StreamingHttpResponse(
                {str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


"""
Clase para calificar, evaluar los cuestionarios, generados por la misma ia
"""


class AIEvaluateQuestions(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request_tema = request.data.get("tema")
            request_questionary = request.data.get("questionary")
            user_auth = Auth.user(request)

            if user_auth.user_type != "estudiante":
                return StreamingHttpResponse(
                    {"El usuario no es un estudiante."},
                    status=403,
                ) 

            # verificamos si existe el tema
            exists_tema = Tema.objects.filter(uuid=request_tema.get("uuid")).exists()
            if not exists_tema:
                return StreamingHttpResponse(
                    {"No existe el tema."},
                    status=404,
                )

            # obtener el tema
            tema = Tema.objects.get(uuid=request_tema.get("uuid"))
            # Obtener pregunta  respuesta
            text_output = []
            for row in request_questionary:
                text_output.append(f"**{row['pregunta']}\nRespuesta:{row['respuesta']}")

            # Unir todo en un texto plano con saltos de linea para cada pregunta y respuesta
            question_plain_text = "\n".join(text_output)

            base_url = env("AI_BASE_URL")
            access_token = env("AI_ACCESS_TOKEN")
            evaluation_questions = {
                "tema": tema,
                "user_auth": user_auth,
                "questions": question_plain_text,
            }

            chat_completion = create_chat_completion(
                base_url=base_url,
                access_token=access_token,
                evaluation_questions=evaluation_questions,
            )

            # Función generadora para streaming
            def generate():
                for chunk in chat_completion:
                    # Asegura de que 'choices' existe y tiene datos
                    if hasattr(chunk, "choices") and len(chunk.choices) > 0:
                        delta_content = chunk.choices[0].delta.content
                        if delta_content:  # Verificar que el contenido no esté vacío
                            yield delta_content  # Enviar el contenido como parte de la respuesta de streaming

            # Crear una respuesta de streaming
            response = StreamingHttpResponse(
                generate(), content_type="text/event-stream"
            )
            # Desactivar el buffering para streaming
            response["X-Accel-Buffering"] = "no"
            # prevent client cache
            response["Cache-Control"] = "no-cache"
            return response

        except Exception as e:
            return StreamingHttpResponse(
                {str(e)}, status=500
            )


