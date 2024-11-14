from rest_framework import serializers
import re
from PIL import Image
from django.core.exceptions import ValidationError


def custom_password_validator(value):
    # Validar que la contraseña tenga al menos 8 caracteres
    if len(value) < 8:
        raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")

    # Validar que la contraseña tenga al menos una letra mayúscula
    if not re.search(r'[A-Z]', value):
        raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")

    # Validar que la contraseña tenga al menos un número
    if not re.search(r'\d', value):
        raise serializers.ValidationError("La contraseña debe contener al menos un número.")

    # Validar que la contraseña tenga al menos un carácter especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial.")
    return value
    
def custom_email_validator(value):
    # Lista de extensiones de correo válidas
    valid_extensions = [".com", ".net", ".bo", ".org", ".info", ".edu"]

    # Verificar si el correo electrónico termina con alguna de las extensiones válidas
    if not any(value.endswith(ext) for ext in valid_extensions):
        raise serializers.ValidationError(
            f"El email debe terminar con una de las siguientes extensiones: {', '.join(valid_extensions)}."
        )
    return value
    
def custom_picture_validator(value):
    if value:
        try:
            # Abre la imagen con Pillow y verifica el formato
            img = Image.open(value)
            if img.format.lower() not in ['jpeg', 'png', 'jpg']:
                raise ValidationError("Solo se permiten imágenes JPEG, JPG y PNG.")
        except IOError:
            raise ValidationError("El archivo no es una imagen válida.")
        
        # Verifica el tamaño máximo de la imagen (2MB)
        if value.size > 2 * 1024 * 1024:
            raise ValidationError("La imagen no debe superar los 2MB.")
    
    return value
