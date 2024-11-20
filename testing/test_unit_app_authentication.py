import pytest

@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass

@pytest.fixture(scope='session')
def django_db_setup():
    """Evita configurar y crear la base de datos de prueba"""
    pass

from apps.usuario.models import Usuario
from apps.authentication.utils import Auth
@pytest.mark.django_db()
def test_unit_authentication_password():
    print("\n")
    usuario = Usuario.objects.get(user="admin")
    
    if Auth.check_password("1234", usuario.password):
        print("Prueba unitaria exitosa")
        assert Auth.check_password("1234", usuario.password)
    else:
        print("Prueba unitaria fallida")
        assert Auth.check_password("1234", usuario.password)
    
