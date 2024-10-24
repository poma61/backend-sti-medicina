# Generated by Django 5.1.2 on 2024-10-23 07:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0003_rename_obervaciones_estudiante_observaciones'),
        ('internado_rotatorio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='areainternadorotatorio',
            name='estudiante',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='area_internado_rotatorio', to='estudiante.estudiante'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tema',
            name='area_internado_rotatorio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tema', to='internado_rotatorio.areainternadorotatorio'),
            preserve_default=False,
        ),
    ]
