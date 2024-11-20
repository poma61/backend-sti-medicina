from django.urls import path
from .views import (
    LoginView,
    UserAuthDataView,
    UserUpdateView,
    LogoutView,
    CustomTokenRefreshView,
    UserPermission,
)

urlpatterns = [
    path("auth/login/", LoginView.as_view(),name = "n-login"),
    path("auth/me/", UserAuthDataView.as_view()),
    path("auth/user-update/", UserUpdateView.as_view()),
    # URL para renovar access token
    path("auth/token/refresh/", CustomTokenRefreshView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/permission/", UserPermission.as_view()),
]
