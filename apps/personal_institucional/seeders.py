# Se debe instalar pip install djando-seeding
# y ejecutar codigo => python3 manage.py seed
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry

from apps.usuario.models import Usuario, Permiso
from apps.personal_institucional.models import PersonalInstitucional


@SeederRegistry.register
class PersonalInstitucionalSeeder(seeders.Seeder):
    id = "PersonalInstitucional01"
    # Crear los usuarios
    data = {
        "nombres": "Cecilio",
        "apellido_paterno": "Poma",
        "apellido_materno": "Muñoz",
        "ci": "454545",
        "ci_expedido": "SC",
        "genero": "masculino",
        "fecha_nacimiento": "2000-01-01",
        "numero_contacto": "1234567",
        "direccion": " La Paz , Bolivia",
        "cargo": "Docente",
        "grado_academico": "Doctor",
        "usuario": {
            "user": "admin",
            "email": "admin@gmail.com",
            "is_active": True,
            "password": "pbkdf2_sha256$870000$vDxLFnvChTmBHqS286ulQs$c/Mvco/7vyhuWbzlNU/MLVx+jAnANq6t1ifwkMtO/ZU=",  # Contraseña: 1234
            "user_type": "administrativo",
        },
    }

    def seed(self):
        data_usuario = self.data.pop("usuario")
        user = Usuario.objects.create(**data_usuario)
        permisos = Permiso.objects.all()
        user.permisos.set(permisos)
        PersonalInstitucional.objects.create(usuario=user, **self.data)
