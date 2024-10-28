from django.shortcuts import render
from .utils import create_chat_completion
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from rest_framework.permissions import AllowAny
from gtts import gTTS
import io

from apps.authentication.jwt_authentication import CustomJWTAuthentication

import environ
env = environ.Env()
environ.Env.read_env()


class TutorAIGenerateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            user_message = request.data.get("user_message", None)

            if user_message is None:
                return StreamingHttpResponse(f"No hay texto", status=404)

            base_url = env("AI_BASE_URL")
            access_token = env("AI_ACCESS_TOKEN")

            # iniciar chat con tutor ahi
            chat_completion = create_chat_completion(
                base_url, access_token, user_message
            )

            # Función generadora para streaming
            def generate():
                for chunk in chat_completion:
                    # Asegurar de que 'choices' existe y tiene datos
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
            return StreamingHttpResponse({str(e)}, status=500)


class TextToSpeechView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            text = request.data.get("text", None)
            if text is None:
                return StreamingHttpResponse(f"No hay texto", status=404)

            # Generar audio
            tts = gTTS(text=text, lang="es")
            # Guardar el audio en un objeto de BytesIO en lugar de un archivo
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            # Regresar al inicio del buffer para leerlo desde el comienzo
            audio_bytes.seek(0)

            # Leer el archivo de audio y crear un StreamingHttpResponse
            response = StreamingHttpResponse(audio_bytes, content_type="audio/mpeg")
            response["Content-Disposition"] = 'attachment; filename="audio.mp3"'
            return response

        except Exception as e:
            return StreamingHttpResponse(
                f"Error al generar audio: {str(e)}", status=500
            )
