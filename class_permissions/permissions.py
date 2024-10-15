from rest_framework import permissions

class ModificarPermiso(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica los estados del usuario
        pass
     

    
