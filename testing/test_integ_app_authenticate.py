import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from rest_framework import status


@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass
@pytest.fixture(scope='session')
def django_db_setup():
    """Evita configurar y crear la base de datos de prueba"""
    pass


@pytest.mark.django_db()
def test_login_view_post():
    print("\n")
    print("**************" * 5)
    datos_de_entrada = {
    "user": "admin",
    "password": "otro_password"
    }

    # Obtener la URL mediante el nombre de la ruta
    url = reverse('n-login')
    client = APIClient()
    # Hacemos una solicitud POST al endpoint de login
    response = client.post(url, datos_de_entrada, format='json')

    print("=> app authenticate, endpoint n-login")
    print(response.status_code)
    print("Prueba de integracion exitosa")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

