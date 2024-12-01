from django.contrib import admin
from .models import Tema
from django.contrib.admin import AdminSite

# Administrador personalizado para el modelo Tema
class TemaAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_title', 'area',
                    'is_status', 'created_at', 'updated_at',)
    search_fields = ('title', 'short_title', 'description',)
    list_filter = ('area',)
    ordering = ('created_at',)

    # Deshabilitar la opción de eliminar
    def has_delete_permission(self, request, obj=None):
        return False 

# Admin personalizado para cambiar cómo se muestra el sitio Admin
class CustomAdminSite(AdminSite):
    site_header = 'Administración del Sistema'
    site_title = 'Admin Tema'
    index_title = 'Panel de administración'

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Eliminar aplicaciones no deseadas
        excluded_apps = ['django_seeding', 'rest_framework', 'token_blacklist']
        app_list = [app for app in app_list if app['app_label']
                    not in excluded_apps]
        return app_list

# Usamos el sitio de administración personalizado
admin.site = CustomAdminSite()
# Registrar el modelo con su admin personalizado
admin.site.register(Tema, TemaAdmin)
