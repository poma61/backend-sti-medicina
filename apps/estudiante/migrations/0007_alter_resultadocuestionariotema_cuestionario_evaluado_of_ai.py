# Generated by Django 5.1.2 on 2024-11-02 21:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0006_remove_cuestionarioevaluadoofai_resultado_cuestionario_estudiante_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultadocuestionariotema',
            name='cuestionario_evaluado_of_ai',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultado_cuestionario_tema', to='estudiante.cuestionarioevaluadoofai'),
        ),
    ]
