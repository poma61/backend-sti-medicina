# Generated by Django 5.1.2 on 2024-11-29 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultadocuestionariotema',
            name='pregunta',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='resultadocuestionariotema',
            name='respuesta',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
