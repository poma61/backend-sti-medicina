from django.urls import path
from .views import LoginView, UserAuthenticate

urlpatterns =[
    path('auth/login/', LoginView.as_view()),
    path('auth/me/', UserAuthenticate.as_view()),
]




