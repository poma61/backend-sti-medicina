# Se debe instalar pip install djando-seeding
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry

from .models import Permiso


@SeederRegistry.register
class PermisoSeeder(seeders.ModelSeeder):
    id = "PermisoSeeder"
    model = Permiso
    data = [
        # modulo
        {
            "name": "Acceso al modulo estudiante",
            "is_type": "module",
            "is_type_content": "students",
            "code": "access_students",
        },
        {
            "name": "Acceso al modulo institucional",
            "is_type": "module",
            "is_type_content": "institutional_staff",
            "code": "access_institutional_staff",
        },
        # permisos estudiantes
        {
            "name": "Registrar estudiante",
            "is_type": "data",
            "is_type_content": "students",
            "code": "data_create_students",
        },
        {
            "name": "Editar estudiante",
            "is_type": "data",
            "is_type_content": "students",
            "code": "data_edit_students",
        },
        {
            "name": "Eliminar estudiante",
            "is_type": "data",
            "is_type_content": "students",
            "code": "data_delete_students",
        },
        # permisos personal
        {
            "name": "Registrar personal",
            "is_type": "data",
            "is_type_content": "institutional_staff",
            "code": "data_create_institutional_staff",
        },
        {
            "name": "Editar personal",
            "is_type": "data",
            "is_type_content": "institutional_staff",
            "code": "data_edit_institutional_staff",
        },
        {
            "name": "Eliminar personal",
            "is_type": "data",
            "is_type_content": "institutional_staff",
            "code": "data_delete_institutional_staff",
        },
    ]
