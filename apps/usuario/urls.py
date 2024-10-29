from django.urls import path
from .views import ListPermiso

urlpatterns = [path("permiso/", ListPermiso.as_view())]


