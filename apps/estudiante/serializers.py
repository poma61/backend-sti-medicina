from rest_framework import serializers
from .models import Estudiante
from apps.usuario.serializers import UsuarioSerializer
from apps.usuario.models import Usuario
from django.db.models import QuerySet
from .validators import custom_number_validator


class UsuarioEstudianteSerializer(serializers.ModelSerializer):
    # usuario =  UsuarioSerializer(many=True) # => Espera una lista de usuarios
    usuario = UsuarioSerializer()  # => Espera solo un usuario

    class Meta:
        model = Estudiante
        fields = "__all__"  # serializar todos
        # solo lectura
        read_only_fields = (
            "created_at",
            "uuid",
        )
        extra_kwargs = {
            #write_only => El campo NO se devuelve en las respuestas
            "is_status": {"write_only": True},
            "numero_contacto": {"validators": [custom_number_validator]},
            "matricula_univ": {"validators": [custom_number_validator]},
        }
        

    # # Aseguramos que UsuarioSerializer es una instancia al momento de actualizar datos
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Verificar si 'self.instance' es un solo objeto o un QuerySet
    #     if (
    #         self.instance
    #         and not isinstance(self.instance, list)
    #         and not isinstance(self.instance, QuerySet)
    #     ):
    #         self.fields["usuario"] = UsuarioSerializer(instance=self.instance.usuario)

    def to_internal_value(self, data):
        """
        Sobrescribe el método to_internal_value para pasar la instancia de usuarioc para la actualizacion
        """
        if self.instance and hasattr(self.instance, "usuario"):
            self.fields["usuario"] = UsuarioSerializer(instance=self.instance.usuario)
        return super().to_internal_value(data)

    def create(self, validated_data):
        # Extraer los datos de usuario
        usuario_data = validated_data.pop("usuario")

        # crear el nuevo usuario
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        if usuario_serializer.is_valid():
            usuario = usuario_serializer.save()

        # Crear  el estudiante con el usuario relacionado
        estudiante = Estudiante.objects.create(usuario=usuario, **validated_data)
        return estudiante

    def update(self, instance, validated_data):
        # Extraer los datos del usuario anidado
        usuario_data = validated_data.pop("usuario", None)

        # Actualizar el usuario si los datos están presentes
        if usuario_data:
            usuario_instance = (
                instance.usuario
            )  # Relacionar con el usuario actual del estudiante
            usuario_serializer = UsuarioSerializer(
                instance=usuario_instance, data=usuario_data, partial=True
            )
            if usuario_serializer.is_valid():
                usuario_serializer.save()

        # Actualizar los campos del estudiante
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
