from rest_framework.permissions import BasePermission
from apps.authentication.utils import Auth

"""
Permisos para el modulo estudiantes
"""
class ViewEstudentPermission(BasePermission):
    def has_permission(self, request, view):
        # "Visualizar estudiantes" 
        code = "data_view_students"
        user = Auth.user(request)
        # Filtra permisos asociados al usuario y verifica
        return user.permisos.filter(code=code).exists()


class CreateEstudentPermission(BasePermission):
    def has_permission(self, request, view):
        # "Registrar estudiante" 
        code = "data_create_students"
        user = Auth.user(request)

        return user.permisos.filter(code=code).exists()


class UpdateEstudentPermission(BasePermission):
    def has_permission(self, request, view):
        # "Editar estudiante"
        code = "data_update_students"
        user = Auth.user(request)

        return user.permisos.filter(code=code).exists()


class DeleteEstudentPermission(BasePermission):
    def has_permission(self, request, view):
        # "Eliminar estudiante"
        code = "data_delete_students"
        user = Auth.user(request)

        return user.permisos.filter(code=code).exists()



"""
 Permisos para el modulo personal institucional
"""
class ViewPersonalInstPermission(BasePermission):
    def has_permission(self, request, view):
        #  "visualizar personal" 
        code = "data_view_institutional_staff"
        user = Auth.user(request)

        return user.permisos.filter(code=code).exists()

class CreatePersonalInstPermission(BasePermission):
    def has_permission(self, request, view):
        # "Registrar personal" 
        code = "data_create_institutional_staff"
        user = Auth.user(request)

        return user.permisos.filter(code=code).exists()


class UpdatePersonalInstPermission(BasePermission):
    def has_permission(self, request, view):
        # "Editar personal"
        code = "data_update_institutional_staff"
        user = Auth.user(request)


        return user.permisos.filter(code=code).exists()


class DeletePersonalInstPermission(BasePermission):
    def has_permission(self, request, view):
        # "Eliminar personal"
        code = "data_delete_institutional_staff"
        user = Auth.user(request)

        return user.permisos.filter(code=code).exists()
