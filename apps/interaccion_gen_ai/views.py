from django.shortcuts import render
from rest_framework.views import APIView
from openai import OpenAI
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from rest_framework.permissions import AllowAny

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
                        "content": ''' 
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
                        ''',
                    },
                    {"role": "user", "content": user_message}, 
                ],
                top_p=0.9,
                temperature=0.6,
                max_tokens=300,
                stream=True,  # Habilitar streaming
                seed=None,
                frequency_penalty=None,
                presence_penalty=None,
            )

            # Función generadora para streaming
            def generate():
                for chunk in chat_completion:
                    # print("Chunk recibido:", chunk)  # Imprimir el chunk completo

                    # Asegúrate de que 'choices' existe y tiene datos
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta_content = chunk.choices[0].delta.content
                        if delta_content:  # Verificar que el contenido no esté vacío
                            # print("Contenido del mensaje:", delta_content)  # Imprimir el contenido del mensaje
                            yield delta_content  # Enviar el contenido como parte de la respuesta de streaming

            # Crear una respuesta de streaming
            response = StreamingHttpResponse(generate(), content_type='text/event-stream')
            response['X-Accel-Buffering'] = 'no'  # Desactivar el buffering para streaming
            response['Cache-Control'] = 'no-cache'  # prevent client cache
         
            return response

        except Exception as e:
            print("Error:", str(e))  # Imprimir el error para depuración
            return Response(
                {
                    "payload": {},
                    "api_status": False,
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



