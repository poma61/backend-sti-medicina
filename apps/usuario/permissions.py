from rest_framework.permissions import BasePermission

"""
Permisos para el modulo estudiantes
"""
class CreateEstudentPermission(BasePermission):
    def has_permission(self, request, view):
        action = "Registrar estudiante" # tambien aplica para listar  estudiantes
        code = "data_create_students"

        # Filtra permisos asociados al usuario y verifica
        return request.user.permisos.filter(code=code).exists()


class UpdateEstudentPermission(BasePermission):
    def has_permission(self, request, view):
        action = "Editar estudiante"
        code = "data_update_students"

        # Filtra permisos asociados al usuario y verifica
        return request.user.permisos.filter(code=code).exists()


class DeleteEstudentPermission(BasePermission):
    def has_permission(self, request, view):
        action = "Eliminar estudiante"
        code = "data_delete_students"

        # Filtra permisos asociados al usuario y verifica
        return request.user.permisos.filter(code=code).exists()



"""
 Permisos para el modulo personal institucional
"""
class CreatePersonalInstPermission(BasePermission):
    def has_permission(self, request, view):
        action = "Registrar personal" # tambien aplica para listar  personal institucional
        code = "data_create_institutional_staff"

        # Filtra permisos asociados al usuario y verifica
        return request.user.permisos.filter(code=code).exists()


class UpdatePersonalInstPermission(BasePermission):
    def has_permission(self, request, view):
        action = "Editar personal"
        code = "data_update_institutional_staff"

        # Filtra permisos asociados al usuario y verifica
        return request.user.permisos.filter(code=code).exists()


class DeletePersonalInstPermission(BasePermission):
    def has_permission(self, request, view):
        action = "Eliminar personal"
        code = "data_delete_institutional_staff"

        # Filtra permisos asociados al usuario y verifica
        return request.user.permisos.filter(code=code).exists()
