# Se debe instalar pip install djando-seeding 
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry

from apps.usuario.models import Usuario
from apps.estudiante.models import Estudiante

@SeederRegistry.register
class UsuarioSeeder(seeders.ModelSeeder):
    id = "UsuarioSeeder"
    # priority = 6
    model = Usuario
    data = [
        {
            "id":1,
            "user": "admin2",
            "email": "admin@gmail.com",
            "is_active": True,
            "password": "pbkdf2_sha256$870000$vDxLFnvChTmBHqS286ulQs$c/Mvco/7vyhuWbzlNU/MLVx+jAnANq6t1ifwkMtO/ZU=",  # 1234
            "user_type": "estudiante",
        },
    ]

@SeederRegistry.register
class EstudianteSeeder(seeders.ModelSeeder):
    id = "EstudianteSeeder"
    # priority = 1
    model = Estudiante
    data = [
        {
            "nombres": "Juan",
            "apellido_paterno": "Perez",
            "apellido_materno": "Mamani",
            "ci": "435445",
            "ci_expedido": "OR",
            "genero": "masculino",
            "fecha_nacimiento": "2000-01-01",
            "numero_contacto": "1234567",
            "direccion": " La Paz , Bolivia",
            "matricula_univ": "7534547",
            "internado_rot": "Hospital del norte",
            "usuario_id": 1,
        },
    ]

