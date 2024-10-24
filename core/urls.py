
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static # Para archivos staticos


urlpatterns = [
    path("api/", include("apps.usuario.urls")),
    path("api/", include("apps.authentication.urls")),
    path("api/", include("apps.estudiante.urls")),
    path("api/", include("apps.personal_institucional.urls")), 
    path("api/", include("apps.interaccion_gen_ai.urls")), 
    path("api/", include("apps.internado_rotatorio.urls")),  
]
   
# Para agregar media
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)   

