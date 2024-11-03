from django.urls import path
from .views import (
    UsuarioEstListCreateView,
    UsuarioEstUpdateDeleteView,
    ProgresoEstudioListCreateOrUpdateView,
    ResultCuestionarioTemaAndEvaluadoOfAIListView,
)

urlpatterns = [
    path("user/estudiante/", UsuarioEstListCreateView.as_view()),
    path("user/estudiante/<uuid:uuid>/", UsuarioEstUpdateDeleteView.as_view()),
    # progreso estudio
    path(
        "user/estudiante/progreso-estudio/",
        ProgresoEstudioListCreateOrUpdateView.as_view(),
    ),
    path(
        "user/estudiante/progreso-estudio/resultado-cuestionario-and-evaluado-of-ai/<uuid:uuid_progreso_estudio>/",
        ResultCuestionarioTemaAndEvaluadoOfAIListView.as_view(),
    ),
]
