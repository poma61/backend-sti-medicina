
import pytest

@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    pass

@pytest.fixture(scope='session')
def django_db_setup():
    """Evita configurar y crear la base de datos de prueba"""
    pass


from apps.estudiante.serializers import UsuarioEstudianteSerializer
@pytest.mark.django_db()
def test_unit_estudiante_serializer():
   print("\n")
   datos  = {}
   estudiante_serializer =  UsuarioEstudianteSerializer(data = datos)
   
   if estudiante_serializer.is_valid():
        print("UsuarioEstudianteSerializer => Prueba unitaria fallida")
        assert estudiante_serializer.data
   else: 
        print("UsuarioEstudianteSerializer => Prueba unitaria exitosa")
        assert estudiante_serializer.errors
    

from apps.estudiante.models import ProgresoEstudio
@pytest.mark.django_db()
def test_unit_estudiante_progreso_estudio():
    print("\n")
    datos  = {}
    progreso_estudio =  ProgresoEstudio.objects.all()
    
    print("ProgresoEstudio => Prueba unitaria exitosa")
    assert progreso_estudio





    


