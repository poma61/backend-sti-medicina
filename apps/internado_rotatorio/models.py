from django.db import models
import uuid
from django.utils.crypto import get_random_string
import os

def pdf_directory_path(instance, filename):
    # Limpia el nombre del archivo para evitar path traversal, conserva el nombre del archivo
    filename = os.path.basename(filename)

    unique_filename = (
        f"{get_random_string(length=10)}_{get_random_string(length=10)}_{filename}"
    )
    pdf_directory = f"internado-rotatorio/{instance.area.name}/"

    # Devuelve la ruta donde se guardará la nueva imagen
    return os.path.join(pdf_directory, unique_filename)

class Area(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True, null=True)
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Tema(models.Model):
    title = models.CharField(max_length=100)
    short_title= models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    description = models.CharField(max_length=300)
    contenido = models.TextField()
    archivo_pdf = models.FileField(upload_to=pdf_directory_path) 
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="tema")
    is_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


