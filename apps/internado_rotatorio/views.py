from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from apps.authentication.jwt_authentication import CustomJWTAuthentication
from apps.authentication.utils import Auth

from .models import Area, Tema
from .serializers import AreaAndTemaSerializer, TemaSerializer

from openai import OpenAI
from django.http import StreamingHttpResponse


class ListCreateTemaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, area):
        try:
            print(request.data)
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

    # Este metodo es para crear, pero se esta en uso
    def post(self, request):
        try:
            serializer = TemaSerializer(data=request.data)

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


class AIGenerateQuestionsView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # verificamos si existe el tema
            exists_tema = Tema.objects.filter(uuid=request.data.get("uuid")).exists()
            if not exists_tema:
                return Response(
                    {
                        "api_status": False,
                        "detail": "No se encontro ningun tema.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            # obtener el tema
            tema = Tema.objects.get(uuid=request.data.get("uuid"))

            client = OpenAI(
                base_url="https://lsrkkppjiuwoo83o.us-east-1.aws.endpoints.huggingface.cloud/v1/",
                api_key="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",
            )

            # Crear el chat_completion con streaming habilitado
            chat_completion = client.chat.completions.create(
                model="tgi",
                messages=[
                    {
                        "role": "system",
                        "content": """ 
                        Eres un tutor en español especializado en medicina. Tu tarea es generar preguntas de un determinado tema de medicina.
                        Se te proporcionará, el tema, una breve introducción del tema y la cantidad de preguntas. Las preguntas deben ser complejas.
                        Solo debes generar preguntas de forma directa sin brindar ninguna introduccion ni informacion adicional. 
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"""Tema: {tema.short_title}. 
                     Introducción del tema:{tema.contenido}.
                     Cantidad preguntas: 10 """,
                    },
                ],
                top_p=0.9,
                temperature=0.3,
                max_tokens=600,
                stream=True,  # Habilitar streaming
                seed=None,
                frequency_penalty=None,
                presence_penalty=None,
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
            return Response(
                {
                    "api_status": False,
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            request_questions = request.data.get("questions")
            user_auth = Auth.user(request)

            # verificamos si existe el tema
            exists_tema = Tema.objects.filter(uuid=request_tema.get("uuid")).exists()
            if not exists_tema:
                return Response(
                    {
                        "api_status": False,
                        "detail": "No se encontro ningun tema.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # obtener el tema
            tema = Tema.objects.get(uuid=request_tema.get("uuid"))
            # Obtener pregunta  respuesta
            text_output = []
            for index, row in enumerate(request_questions, start=1):
                text_output.append(f"**{row['pregunta']}\nRespuesta:{row['respuesta']}")

            # Unir todo en un texto plano
            plain_text = "\n".join(text_output)
            user_auth = Auth.user(request)

            client = OpenAI(
                base_url="https://lsrkkppjiuwoo83o.us-east-1.aws.endpoints.huggingface.cloud/v1/",
                api_key="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",
            )
            # Crear el chat_completion con streaming habilitado
            chat_completion = client.chat.completions.create(
                model="tgi",
                messages=[
                    {
                        "role": "system",
                        "content": f"""Eres un tutor en español especializado en medicina. 
                        Tu tarea es evaluar el cuestionario del estudiante {user_auth.estudiante.nombres} {user_auth.estudiante.apellido_paterno} {user_auth.estudiante.apellido_materno}.
                        Se te proporcionara el tema, una breve introduccion del tema y el cuestionario con sus respectivas respuestas. 
                        Una vez terminado la revisión del cuestionario debes indicar que debe ir al menu del sistema, ir a la opcion TutorAI, para que
                        pueda realizar sus consultas de manera personalizada y pueda conversar contigo. 
                        """,
                    },
                    {
                        "role": "user",
                        "content": f""" Hola soy {user_auth.estudiante.nombres} {user_auth.estudiante.apellido_paterno} {user_auth.estudiante.apellido_materno}.
                        Te envio mi tema, breve introducción del tema y mi cuestionario para que puedas evaluarme.
                    Tema: {tema.short_title}. 
                     Introducción:{tema.contenido}.
                     cuestionario:
                     {plain_text}
                    """,
                    },
                ],
                top_p=0.9,
                temperature=0.7,
                max_tokens=1200,
                stream=True,
                seed=None,
                frequency_penalty=None,
                presence_penalty=None,
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
            return Response(
                {
                    "api_status": False,
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
