from rest_framework import serializers
from .models import Usuario, Permiso
from django.contrib.auth.hashers import make_password
from apps.authentication.utils import Auth
from .validators import (
    custom_password_validator,
    custom_email_validator,
    custom_picture_validator,
)
import os
from django.conf import settings

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    # Campo solo para recibir los permisos en una lista
    permisos = serializers.ListField(
        child=serializers.CharField(), write_only=True , required=False
    )

    class Meta:
        model = Usuario
        fields = "__all__"  # Todos los campos que se van a serializar
        read_only_fields = (
            "created_at",
            "uuid",
        )  # campos de solo lectura que no pueden actualizar

        extra_kwargs = {
            "is_status": {
                "write_only": True  # El campo NO se devuelve en las respuestas0
            },
            "last_login": {
                "write_only": True  # El campo NO se devuelve en las respuestas
            },
            "password": {
                "write_only": True,
                # Validaciones personalizadas
                "validators": [custom_password_validator],
            },
            "email": {
                "validators": [custom_email_validator],
            },
            "picture": {"validators": [custom_picture_validator]},
        }

    def create(self, validated_data):
        # pop => obtiene el valor y  remueve el campo permisos
        # permisos es una lista de ids
        permiso_data = validated_data.pop("permisos", [])
        user = Usuario(**validated_data)

        user.password = Auth.encrypt_password(validated_data["password"])
        user.save()

        if permiso_data and validated_data.get("user_type") != "estudiante":
             # SELECT * FROM permiso WHERE code IN (1, 3, 5)
            permisos = Permiso.objects.filter(code__in=permiso_data)
            user.permisos.set(permisos)  # Agregamos los permisos

        return user

    def update(self, instance, validated_data):
        permiso_data = validated_data.pop("permisos", [])
        # cargamos otros campos
        for attr, value in validated_data.items():
            # Excluir los campos "password" y "picture"
            if attr not in ["password", "picture"]:
                setattr(instance, attr, value)
                
        if permiso_data and validated_data.get("user_type") != "estudiante":
            # SELECT * FROM permiso WHERE code IN (1, 3, 5)
            permisos = Permiso.objects.filter(code__in=permiso_data)
            instance.permisos.set(permisos)
        else:
            # si no hay permisos eliminamos
             instance.permisos.clear()

        if validated_data.get("picture"):
            if instance.picture.name == "usuario/default_profile.png":
                # si es la imagen por defecto asignamos la imagen y NO se elimina la imagen por defecto
                instance.picture = validated_data.get("picture")
            else:
                # Eliminación de la imagen anterior
                previous_picture_path = os.path.join(
                    settings.MEDIA_ROOT, instance.picture.name
                )
                if os.path.exists(previous_picture_path):
                    os.remove(previous_picture_path)
                # Cargamos la nueva imagen
                instance.picture = validated_data.get("picture")

        # Solo actualizar la contraseña si se proporciona
        if validated_data.get("password"):
            instance.password = Auth.encrypt_password(validated_data.get("password"))

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        #Aregamos los permisos
        representation['permisos'] = [permiso.code for permiso in instance.permisos.all()]
        return representation


