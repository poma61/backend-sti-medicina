from django.urls import path
from .views import  UsuarioPersonalInstListCreateView, UsuarioPersonalInstUpdateDeleteView

urlpatterns = [
    path("user/personal-institucional/", UsuarioPersonalInstListCreateView.as_view(), name = "n-personal-list-create"),
    path("user/personal-institucional/<uuid:uuid>/", UsuarioPersonalInstUpdateDeleteView.as_view()),
]