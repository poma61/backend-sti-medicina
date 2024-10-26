from django.urls import path
from .views import TutorAIGenerateView, TextToSpeechView

urlpatterns = [
    path("gen-ai/interaccion-tutorai/", TutorAIGenerateView.as_view() ),
    path("text-to-speech/", TextToSpeechView.as_view() ), 
]