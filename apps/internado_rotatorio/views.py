from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from apps.authentication.jwt_authentication import CustomJWTAuthentication

from .models import Area, Tema
from .serializers import AreaAndTemaSerializer

from openai import OpenAI
from django.http import StreamingHttpResponse


class ListCreateTemaView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            temas = Tema.objects.filter(is_status=True)

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
            serializer = AreaAndTemaSerializer(data=request.data)

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


class GenerateIAQAView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
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
                        Eres un tutor en español especializado en medicina. Tu tarea es generar preguntas relacionadas de un tema de medicina
                        que se te proporcionará, tambien se te proporcionara una breve descripcion. Las preguntas deben ser complejas.
                        Solo debes generar preguntas de forma directa sin brindar niguna introduccion. 
                        """,
                    },
                    {
                        "role": "user",
                        "content": """Tema: diabetes. Descripcion: La diabetes es una enfermedad en la que los niveles de
                     glucosa (azúcar) de la sangre están muy altos. La glucosa proviene de los alimentos que consume. La insulina 
                     es una hormona que ayuda a que la glucosa entre a las células para suministrarles energía. Cantidad preguntas: 10 """,
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
            response["X-Accel-Buffering"] = (
                "no"  # Desactivar el buffering para streaming
            )
            response["Cache-Control"] = "no-cache"  # prevent client cache
            return response

        except Exception as e:
            return Response(
                {
                    "payload": {},
                    "api_status": False,
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


"""
Clase para generar cuestionario segun un determinado tema, IA genera el cuestonario
"""
class AIGenerateQuestionsView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            exists_tema = Tema.objects.filter(
                uuid=request.data.get("uuid", None)
            ).exists()
            if not exists_tema:
                return Response(
                    {
                        "api_status": False,
                        "detail": "No se encontro ningun tema.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

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
                        Eres un tutor en español especializado en medicina. Tu tarea es generar preguntas de un determinado tema de medicina
                        que se te proporcionará, tambien se te proporcionara una breve descripcion. Las preguntas deben ser complejas.
                        Solo debes generar preguntas de forma directa sin brindar introduccion. 
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"""Tema: {tema.short_title}. 
                     Descripcion:{tema.contenido}.
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
            response["X-Accel-Buffering"] = (
                "no"  # Desactivar el buffering para streaming
            )
            response["Cache-Control"] = "no-cache"  # prevent client cache
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
        print(request)
        return Response(
            {
                "api_status": True,
                "detail": "OK",
            },
            status=status.HTTP_200_OK,
        )
