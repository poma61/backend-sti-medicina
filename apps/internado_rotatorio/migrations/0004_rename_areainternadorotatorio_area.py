# Generated by Django 5.1.2 on 2024-10-23 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internado_rotatorio', '0003_remove_areainternadorotatorio_estudiante'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AreaInternadoRotatorio',
            new_name='Area',
        ),
    ]