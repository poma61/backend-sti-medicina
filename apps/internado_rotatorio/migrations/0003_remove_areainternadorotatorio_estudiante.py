# Generated by Django 5.1.2 on 2024-10-23 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internado_rotatorio', '0002_areainternadorotatorio_estudiante_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areainternadorotatorio',
            name='estudiante',
        ),
    ]
