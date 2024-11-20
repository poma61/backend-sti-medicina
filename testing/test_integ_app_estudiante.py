import pytest

from rest_framework import status


@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass
@pytest.fixture(scope='session')
def django_db_setup():
    """Evita configurar y crear la base de datos de prueba"""
    pass

from django.urls import reverse
from rest_framework.test import APIClient
@pytest.mark.django_db()
def test_estudiante_endpoint_post():
    print("\n")
    print("**************" * 5)

    # Obtener la URL mediante el nombre de la ruta
    url = reverse('n-estudiante-list-create')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer token-invalido')
    # Hacemos una solicitud POST
    response = client.post(url)

    print("=> app estudiante, endpoint n-estudiante-list-create")
    print(response.status_code)
    print("Prueba de integracion exitosa")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED



