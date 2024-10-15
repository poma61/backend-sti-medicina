from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.hashers import make_password
from apps.authentication.utils import Auth
from .validators import custom_password_validator, custom_email_validator

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"  # Todos los campos que se van a serializar
        read_only_fields = (
            "created_at",
        )  # campos de solo lectura que no pueden actualizar

        # Ejemplos
        #  extra_kwargs = {
        #     'password': {'write_only': True},  # La contraseña no se devuelve en las respuestas
        #     'user_type': {'default': 'estudiante'},  # Valor por defecto
        #     'created_at': {'read_only': True},  # Solo se puede leer
        #     'email': {'required': True},  # Este campo es obligatorio
        # }

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
            # Validaciones personalizadas
            "email": {
                "validators": [custom_email_validator],
            },
        }

    def create(self, validated_data):
        user = Usuario(**validated_data)
        # Establecer la contraseña de manera segura
        user.password = Auth.encrypt_password(validated_data["password"])
        user.save()
        
        return user

    def update(self, instance, validated_data):
        # validated_data.get('user', instance.user) => Intenta obtener el nuevo valor para el campo user desde validated_data.
        # Si el campo no está presente en validated_data, mantendrá el valor actual de instance.user.
        instance.user = validated_data.get("user", instance.user)
        instance.user = validated_data.get("user", instance.user)
        instance.email = validated_data.get("email", instance.email)
        instance.user_type = validated_data.get("user_type", instance.user_type)
        
        # Solo actualizar la contraseña si se proporciona
        # Porque si no  lo verificamos podriamos encriptar otra vez algo que ya fue encryptado
        if "password" in validated_data:
            instance.password = Auth.encrypt_password(
                validated_data["password"]
            )  # Encriptar y establecer

        instance.save()
        return instance

