
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static # Para archivos staticos

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/', include('apps.usuario.urls')),
    path('api/', include('apps.authentication.urls')),
]

# Para agregar media
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)   

