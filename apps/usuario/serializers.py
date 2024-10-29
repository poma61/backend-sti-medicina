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
    # Campo para recibir los IDs de permisos
    # write_only = True => si o si debe para que funcione una relacion ManyToMany
    permiso = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    # Devuelve los datos completos de los permisos
    # permisos_asignados = PermisoSerializer(many=True, read_only=True, source='permiso')

    # Campo de solo lectura para devolver únicamente los IDs de permisos
    permisos_asignados = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source="permiso"
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

    def get_permisos_asignados(self, instance):
        # Devolver una lista de los IDs de permisos asignados al usuario
        return list(instance.permiso.values_list("id", flat=True))

    def create(self, validated_data):
        # pop => obtiene el valor y  remueve el campo permiso
        # permiso es una lista de ids
        permiso_data = validated_data.pop("permiso")
        user = Usuario(**validated_data)

        user.password = Auth.encrypt_password(validated_data["password"])
        user.save()

        if permiso_data and validated_data.get("user_type") != "estudiante":
            # SELECT * FROM permiso WHERE id IN (1, 3, 5);
            permisos = Permiso.objects.filter(id__in=permiso_data)
            user.permiso.set(permisos)  # Agregamos los permiso

        return user

    def update(self, instance, validated_data):
        permiso_data =  validated_data.pop("permiso")
         # cargamos otros campos
        for attr, value in validated_data.items():
            # Excluir los campos "password" y "picture"
            if attr not in ["password", "picture"]:
                setattr(instance, attr, value)

        if permiso_data and validated_data.get("user_type") != "estudiante":
            # SELECT * FROM permiso WHERE id IN (1, 3, 5)
            permisos = Permiso.objects.filter(id__in=permiso_data)
            instance.permiso.set(permisos) # Agregamos los permiso 
            
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
            instance.password = Auth.encrypt_password(
                validated_data.get("password")
            )  

        instance.save()
        return instance
