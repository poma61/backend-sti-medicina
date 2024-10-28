# Se debe instalar pip install djando-seeding
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry

from .models import Permiso


@SeederRegistry.register
class PermisoSeeder(seeders.ModelSeeder):
    id = "PermisoSeeder"
    model = Permiso
    data = [
        # permisos estudiantes
        {"name": "Editar estudiante", "is_type": "data", "code": "data_edit_students"},
        {
            "name": "Eliminar estudiante",
            "is_type": "data",
            "code": "data_delete_students",
        },
        {"name": "Editar personal", "is_type": "data", "code": "data_edit_personal"},
        # permisos personal
        {
            "name": "Eliminar personal institucional",
            "is_type": "data",
            "code": "data_delete_personal",
        },
        {
            "name": "Eliminar personal institucional",
            "is_type": "data",
            "code": "data_delete_personal",
        },
        # modulo
         {
            "name": "Acceso al modulo estudiante",
            "is_type": "module",
            "code": "access_personal",
        },
          {
            "name": "Acceso al modulo institucional",
            "is_type": "module",
            "code": "access_institucional",
        },
    ]


