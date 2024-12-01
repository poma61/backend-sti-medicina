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
            "name": "cirugia",
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

