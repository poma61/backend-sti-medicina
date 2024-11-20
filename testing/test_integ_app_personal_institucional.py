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
from apps.usuario.models import Usuario
from apps.authentication.utils import Auth
from rest_framework_simplejwt.tokens import RefreshToken
@pytest.mark.django_db()
def test_personal_endpoint_post():
    print("\n")
    print("*****************" * 5)

    # Obtener el token de acceso 
    user =  Usuario.objects.get(user = "admin")
    if Auth.check_password("1234", user.password):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token) 
    else:
        access_token = "no-token"

    # Obtener la URL mediante el nombre de la ruta
    url = reverse('n-personal-list-create')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    # Hacemos una solicitud POST
    response = client.post(url)

    print("=> App personal_institucional, endpoint n-personal-list-create, metodo post")
    print(response.status_code)
    print("Prueba de integracion exitosa")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


