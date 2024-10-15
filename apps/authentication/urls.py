from django.urls import path
from .views import LoginView, UserAuthDataView, UserUpdateView

urlpatterns = [
    path("auth/login/", LoginView.as_view()),
    path("auth/me/", UserAuthDataView.as_view()),
    path("auth/user-update/", UserUpdateView.as_view()),
]
