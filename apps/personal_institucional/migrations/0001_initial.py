# Generated by Django 5.1.2 on 2024-10-17 05:33

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalInstitucional',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nombres', models.CharField(max_length=255)),
                ('apellido_paterno', models.CharField(max_length=255)),
                ('apellido_materno', models.CharField(max_length=255)),
                ('ci', models.CharField(max_length=100)),
                ('ci_expedido', models.CharField(max_length=20)),
                ('genero', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField()),
                ('numero_contacto', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=300)),
                ('cargo', models.CharField(max_length=225)),
                ('grado_academico', models.CharField(max_length=225)),
                ('obervaciones', models.CharField(blank=True, max_length=400, null=True)),
                ('is_status', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='personal_institucional', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]