# Generated by Django 5.1.2 on 2024-11-02 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0004_resultadocuestionariotema_cuestionarioevaluadoofai_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuestionarioevaluadoofai',
            old_name='result_cuestionario_estudiante',
            new_name='resultado_cuestionario_estudiante',
        ),
    ]
