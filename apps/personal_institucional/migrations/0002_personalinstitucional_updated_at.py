# Generated by Django 5.1.2 on 2024-10-21 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_institucional', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinstitucional',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
