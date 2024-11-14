import pytest
from apps.authentication.utils import Auth

@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass
@pytest.fixture(scope='session')
def django_db_setup():
    """Evita configurar y crear la base de datos de prueba"""
    pass

from apps.usuario.models import Usuario
@pytest.mark.django_db()
def test_usuario_create():
    print("\n")
    print("*****************" * 5)
    data = {
            "user": "test",
            "email": "test@gmail.com",
            "is_active": True,
            "password": "pbkdf2_sha256$870000$vDxLFnvChTmBHqS286ulQs$c/Mvco/7vyhuWbzlNU/MLVx+jAnANq6t1ifwkMtO/ZU=",  # Contraseña: 1234
            "user_type": "administrativo",
    }
    usuario = Usuario.objects.create(**data)
    print("=> Modelo Usuario")
    print("Prueba unitaria exitosa")
    assert usuario

