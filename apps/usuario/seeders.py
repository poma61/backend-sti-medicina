# Se debe instalar pip install djando-seeding
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry

from .models import Permiso


@SeederRegistry.register
class PermisoSeeder(seeders.ModelSeeder):
    id = "PermisoSeeder005"
    model = Permiso
    data = [
        # permisos estudiantes
        {
            "module": "Estudiante",
            "name": "Registrar estudiante",
            "is_type": "data",
            "is_type_content": "students",
            "code": "data_create_students",
        },
        {
            "module": "Estudiante",
            "name": "Editar estudiante",
            "is_type": "data",
            "is_type_content": "students",
            "code": "data_update_students",
        },
        {
            "module": "Estudiante",
            "name": "Eliminar estudiante",
            "is_type": "data",
            "is_type_content": "students",
            "code": "data_delete_students",
        },
        # permisos personal
        {
            "module": "Personal institucional",
            "name": "Registrar personal",
            "is_type": "data",
            "is_type_content": "institutional_staff",
            "code": "data_create_institutional_staff",
        },
        {
            "module": "Personal institucional",
            "name": "Editar personal",
            "is_type": "data",
            "is_type_content": "institutional_staff",
            "code": "data_update_institutional_staff",
        },
        {
            "module": "Personal institucional",
            "name": "Eliminar personal",
            "is_type": "data",
            "is_type_content": "institutional_staff",
            "code": "data_delete_institutional_staff",
        },
    ]
