from django.urls import path
from .views import UsuarioListCreateView, UsuarioUpdateDeleteView

urlpatterns =[
    path('usuario/', UsuarioListCreateView.as_view()),
    path('usuario/<int:id>/', UsuarioUpdateDeleteView.as_view(), ),
]




