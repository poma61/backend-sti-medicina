from django.shortcuts import render
from rest_framework.views import APIView
from openai import OpenAI
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from rest_framework.permissions import AllowAny
from gtts import gTTS
from gtts import gTTS
import io


class TutorAIGenerateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_message = request.data.get("user_message")
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
                        Eres un tutor en español de medicina, debes responder de forma clara y concisa.
                        Si no sabes algun concepto medico, debes indicar que no esta en tu base de conocimientos.
                        Solo debes enfocarte en el area de medicina, si te preguntan de otra area que no es medicina debes indicar que no
                        tienes conocimiento sobre esa area. Fuiste un modelo preentrenado, el universitario Cecilio Poma
                        Muñoz te hizo un entrenamiento con datos medicos recopilados de hugging face 
                        y textos , libros medicos de la carrera de medicina de  Universidad Publica de el alto.
                        Los textos y libros medicos fueron seleccionados con ayuda del Dr. Luis Flores Que es el coordinador del Internado Rotatorio.
                        Eres un modelo de inteligencia artificial creado por el universitario Cecilio Poma Muñoz que es de la carrera
                        de Ingenieria de sistemas de  La universidad publica de el alto. Eeres un modelo medico para estudiantes de medicina
                        que estan realizando el internado rotatorio.
                        La Universidad  Publica de El Alto se situa  en La ciudad De el Alto, Bolivia.
                        """,
                    },
                    {"role": "user", "content": user_message},
                ],
                top_p=0.9,
                temperature=0.6,
                max_tokens=500,
                stream=True,  # Habilitar streaming
                seed=None,
                frequency_penalty=None,
                presence_penalty=None,
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
            return Response(
                {
                    "api_status": False,
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TextToSpeechView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            text = request.data.get("text")
            if text is None:
                return StreamingHttpResponse(f"No hay texto", status=404)

            # Generar audio
            tts = gTTS(text=text, lang="es")
            # Guardar el audio en un objeto de BytesIO en lugar de un archivo
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)  # Regresar al inicio del buffer para leerlo desde el comienzo
            
            # Leer el archivo de audio y crear un StreamingHttpResponse
            response = StreamingHttpResponse(audio_bytes, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
            return response

        except Exception as e:
              return StreamingHttpResponse(f"Error al generar audio: {str(e)}", status=500)
#
# codigo funciona pero esta guardando el audio
# class TextToSpeechView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         text = request.data.get("text")

#         # Generar audio
#         tts = gTTS(text='Hola como estas', lang="es",slow=True)
#         audio_file_path = 'audio.mp3'  # Ruta temporal del archivo de audio

#         # Guardar el audio en un archivo temporal
#         tts.save(audio_file_path)
  
#         # Leer el archivo de audio y crear un StreamingHttpResponse
#         response = StreamingHttpResponse(open(audio_file_path, 'rb'), content_type='audio/mpeg')
#         response['Content-Disposition'] = 'attachment; filename="audio.mp3"'

#         # Borrar el archivo de audio después de enviarlo
#         # os.remove(audio_file_path)

#         return response
