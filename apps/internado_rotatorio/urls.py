from django.urls import path
from .views import ListTemaView, DetailTemaView, AIGenerateQuestionsView, AIEvaluateQuestions, CreateTemaView

urlpatterns = [
   path("internado-root/all-tema/<str:area>/", ListTemaView.as_view()),
   path("internado-root/tema/", CreateTemaView.as_view()),
   path("internado-root/tema/<str:area>/<uuid:uuid>/", DetailTemaView.as_view()),
   path("internado-root/ai-generate-questions/", AIGenerateQuestionsView.as_view()),
   path("internado-root/ai-evaluate-questions/", AIEvaluateQuestions.as_view()),
]

# falta probar el metodo post