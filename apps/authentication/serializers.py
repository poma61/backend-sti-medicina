from rest_framework import serializers
from apps.usuario.models import Usuario
from .utils import Auth
from .validators import custom_password_validator, custom_email_validator
from PIL import Image
import os
from django.conf import settings

class AuthUsuarioSerializer(serializers.ModelSerializer):
    confirm_new_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = "__all__"  # Todos los campos que se van a serializar
        read_only_fields = (
            "created_at",
        )  # campos de solo lectura que no pueden actualizar

        extra_kwargs = {
            "is_status": {
                "write_only": True  # El campo NO se devuelve en las respuestas
            },
            "last_login": {
                "write_only": True  # El campo NO se devuelve en las respuestas
            },
            # Validaciones personalizadas
            "email": { 
                "validators": [custom_email_validator],
            },
        }

    def update(self, instance, validated_data):
        instance.user = validated_data.get("user", instance.user)
        instance.email = validated_data.get("email", instance.email)
        
        if 'picture' in validated_data:
           if  instance.picture.name == "usuario/default_profile.png":
                # si es la imagen por defecto asignamos la imagen y NO se elimina la imagen por defecto
                instance.picture = validated_data.get('picture')
           else:
                # Eliminación de la imagen anterior
                previous_picture_path = os.path.join(settings.MEDIA_ROOT, instance.picture.name)
                if os.path.exists(previous_picture_path):
                    os.remove(previous_picture_path)
                    # Cargamos la nueva imagen    
                    instance.picture = validated_data.get('picture')
           
        instance.password = Auth.encrypt_password(
            validated_data.get("new_password")
        )  # Encriptar y establecer
        instance.save()
        return instance

    def validate_new_password(self, value):
        return custom_password_validator(value)

    def custom_picture_validator(value):
        if value:
            try:
                # Abre la imagen con Pillow y verifica el formato
                img = Image.open(value)
                if img.format.lower() not in ['jpeg', 'png', 'jpg']:
                    raise serializers.ValidationError("Solo se permiten imágenes JPEG, JPG y PNG.")
            except IOError:
                raise serializers.ValidationError("El archivo no es una imagen válida.")
        
        # Verifica el tamaño máximo de la imagen (2MB)
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("La imagen no debe superar los 2MB.")
        return value

    # Validación general
    def validate(self, data):
        confirm_new_password = data.get("confirm_new_password")
        new_password = data.get("new_password")
        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                {"confirm_new_password": "Las contraseñas no coinciden."}
            )
        return data

