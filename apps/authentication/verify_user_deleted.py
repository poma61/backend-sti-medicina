from rest_framework import permissions

class UserNotDeleted(permissions.BasePermission):

    def has_permission(self, request, view):
        # Verifica si el usuario fue eliminado
        return request.user.is_status

