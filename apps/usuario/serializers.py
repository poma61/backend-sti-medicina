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
        instance.email = validated_data.get("email", instance.email)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.user_type = validated_data.get("user_type", instance.user_type)

        if 'picture' in validated_data:
            # Evitamos que elimine la imagen de usuario por defecto
            if instance.picture.name != "usuario/default_profile.png":
                # Eliminación de la imagen anterior
                previous_picture_path = os.path.join(settings.MEDIA_ROOT, instance.picture.name)
                if os.path.exists(previous_picture_path):
                    os.remove(previous_picture_path)
                # Cargamos la nueva imagen    
                instance.picture = validated_data.get('picture')
           
        # Solo actualizar la contraseña si se proporciona
        if "password" in validated_data:
            instance.password = Auth.encrypt_password(
                validated_data.get("password")
            )  # Encriptar y establecer

        instance.save()
        return instance
