from rest_framework import permissions

class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica los estados del usuario
        return request.user.is_active 
     
