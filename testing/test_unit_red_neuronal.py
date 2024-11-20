from apps.tutor_ai.utils import red_neuronal
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

@pytest.mark.django_db()
def test_red_neuronal():
    print("\n")
    print("*****************" * 5)

    is_red_neuronal = red_neuronal(
        input="hola",
        top_p=0.9,
        temperature=0.6,
        max_tokens=2000,
        stream=True,
        seed=None,
    )
    print("Prueba unitaria exitosa")
    assert is_red_neuronal


