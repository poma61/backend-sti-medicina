from django.urls import path
from .views import TutorAIGenerateView

urlpatterns = [
    path("gen-ai/interaccion-tutorai/", TutorAIGenerateView.as_view() ),
]