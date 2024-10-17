from django.urls import path
from .views import LoginView, UserAuthDataView, UserUpdateView, LogoutView, CustomTokenRefreshView

urlpatterns = [ 
    path("auth/login/", LoginView.as_view()),
    path("auth/me/", UserAuthDataView.as_view()),
    path("auth/user-update/", UserUpdateView.as_view()),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view()),  # URL para renovar access token
    path("auth/logout/", LogoutView.as_view()),
]



