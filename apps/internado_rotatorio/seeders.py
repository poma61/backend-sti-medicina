# Se debe instalar pip install djando-seeding
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry

from .models import Tema, Area


@SeederRegistry.register
class AreaInternadoRotatorioSeeder(seeders.ModelSeeder):
    id = "AreaInternadoRotatorioSeeder"
    model = Area
    data = [
        {
            "name": "medicina-interna",
        },
        {
            "name": "cirurgia",
        },
        {
            "name": "pediatria",
        },
        {
            "name": "ginecologia-obstetricia",
        },
        {
            "name": "salud-publica",
        },
    ]


@SeederRegistry.register
class TemaSeeder(seeders.ModelSeeder):
    id = "TemaSeeder"
    model = Tema
    data = [
        {
            "title": "Medicina Iterna, Tomo I, 4ta edicion",
            "description": """La medicina interna y 
                        la formación del médico""",
            "contenido": "La medicina interna",
            "archivo_pdf": "areas_internado_rotatorio/medicina_interna/Medicina-Interna-TomoI-4ed.pdf",
            "area_id": 1
        },
    ]
