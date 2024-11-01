from django.urls import path
from .views import (
    UsuarioEstListCreateView, 
    UsuarioEstUpdateDeleteView, 
    ProgresoEstudioListCreateOrUpdateView,
    )

urlpatterns = [
    path("user/estudiante/", UsuarioEstListCreateView.as_view() ),
    path("user/estudiante/<uuid:uuid>/", UsuarioEstUpdateDeleteView.as_view() ),
    path("user/estudiante/progreso-estudio/", ProgresoEstudioListCreateOrUpdateView.as_view() ),

]





