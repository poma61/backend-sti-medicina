import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken 
from rest_framework.test import APIRequestFactory
from apps.authentication.utils import Auth

@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass
@pytest.fixture(scope='session')
def django_db_setup():
    """Evita configurar y crear la base de datos de prueba"""
    pass

from apps.usuario.models import Usuario
from apps.personal_institucional.views import UsuarioPersonalInstListCreateView   
@pytest.mark.django_db()
def test_authenticated_api_view_direct_call():
    print("\n")
    print("*****************" * 5)
    user = Usuario.objects.get(user="admin")

    if Auth.check_password('1234', user.password):
        token = AccessToken.for_user(user)

    factory = APIRequestFactory()
    # La URL es irrelevante, pero ejeucta el metodo get de UsuarioPersonalInstListCreateView
    request_get = factory.get('/')
    request_get.META['HTTP_AUTHORIZATION'] = f'Bearer {str(token)}'

    # Instancia la vista y llama al método get
    view = UsuarioPersonalInstListCreateView.as_view()
    response = view(request_get)

    print("=> UsuarioPersonalInstListCreateView, metodo get")
    print(response.data.get("api_status"))
    print("Prueba unitaria exitosa")
    assert response.status_code == status.HTTP_200_OK

