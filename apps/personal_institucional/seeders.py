# Se debe instalar pip install djando-seeding
# y ejecutar codigo python3 manage.py
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry

from apps.usuario.models import Usuario
from apps.personal_institucional.models import PersonalInstitucional


@SeederRegistry.register
class UsuarioSeeder(seeders.ModelSeeder):
    id = "UsuarioSeeder2"
    # priority = 6
    model = Usuario
    data = [
        {
            "id": 2,
            "user": "admin3",
            "email": "admin@gmail.com",
            "is_active": True,
            "password": "pbkdf2_sha256$870000$vDxLFnvChTmBHqS286ulQs$c/Mvco/7vyhuWbzlNU/MLVx+jAnANq6t1ifwkMtO/ZU=",  # 1234
            "user_type": "estudiante",
        },
    ]


@SeederRegistry.register
class PersonalInstitucionalSeeder(seeders.ModelSeeder):
    id = "PersonalInstitucional"
    # priority = 1
    model = PersonalInstitucional
    data = [
        {
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
            "usuario_id": 2,
        },
    ]
