from django.urls import path
from .views import ListCreateTemaView, DetailTemaView, AIGenerateQuestionsView, AIEvaluateQuestions

urlpatterns = [
   path("internado-root/area-and-tema/", ListCreateTemaView.as_view()),
   path("internado-root/area-and-tema/<str:area>/<uuid:uuid>/", DetailTemaView.as_view()),
   path("internado-root/ai-generate-questions/", AIGenerateQuestionsView.as_view()),
   path("internado-root/ai-evaluate-questions/", AIEvaluateQuestions.as_view()),
]

# falta probar el metodo post