# Se debe instalar pip install djando-seeding
# y ejecutar codigo => python3 manage.py seed
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry

from apps.usuario.models import Usuario, Permiso
from apps.personal_institucional.models import PersonalInstitucional


@SeederRegistry.register
class UsuarioSeeder(seeders.Seeder):
    id = "UsuarioSeeder"

    # Crear los usuarios
    data = [
        {
            "user": "admin",
            "email": "admin@gmail.com",
            "is_active": True,
            "password": "pbkdf2_sha256$870000$vDxLFnvChTmBHqS286ulQs$c/Mvco/7vyhuWbzlNU/MLVx+jAnANq6t1ifwkMtO/ZU=",  # Contraseña: 1234
            "user_type": "administrativo",
        },
    ]

    def seed(self):
        user = Usuario.objects.create(**self.data[0])
        permisos = Permiso.objects.all()
        user.permisos.set(permisos)


@SeederRegistry.register
class PersonalInstitucionalSeeder(seeders.ModelSeeder):
    id = "PersonalInstitucional"
    # priority = 1
    model = PersonalInstitucional
    data = [
        {
            "usuario_id": 1,
            "nombres": "Carlos",
            "apellido_paterno": "Perez",
            "apellido_materno": "Mamani",
            "ci": "454545",
            "ci_expedido": "SC",
            "genero": "masculino",
            "fecha_nacimiento": "2000-01-01",
            "numero_contacto": "1234567",
            "direccion": " La Paz , Bolivia",
            "cargo": "Docente",
            "grado_academico": "Doctor",
        },
    ]


