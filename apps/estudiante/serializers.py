from rest_framework import serializers
from .models import (
    Estudiante,
    ProgresoEstudio,
    ResultadoCuestionarioTema,
    CuestionarioEvaluadoOfAI,
)
from apps.usuario.serializers import UsuarioSerializer
from apps.usuario.models import Usuario
from django.db.models import QuerySet
from .validators import custom_number_validator, custom_ci_complemento_validator
from apps.internado_rotatorio.serializers import TemaSerializer


class UsuarioEstudianteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Estudiante
        fields = "__all__"  # serializar todos
        # solo lectura
        read_only_fields = (
            "created_at",
            "uuid",
        )
        extra_kwargs = {
            # write_only => El campo NO se devuelve en las respuestas
            "is_status": {"write_only": True},
            "numero_contacto": {"validators": [custom_number_validator]},
            "matricula_univ": {"validators": [custom_number_validator]},
            "ci": {"validators": [custom_number_validator]},
            "ci_complemento": {"validators": [custom_ci_complemento_validator]},
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


class ProgresoEstudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgresoEstudio
        fields = "__all__"
        # write_only_fields= ("is_status", )
        read_only_fields = ("created_at",)


class CuestionarioEvaluadoOfAISerializer(serializers.ModelSerializer):
    class Meta:
        model = CuestionarioEvaluadoOfAI
        fields = "__all__"
        # campos que no se devuelven en las respuestas
        write_only_fields = ("is_status",)
        # campos de solo lectura
        read_only_fields = ("created_at",)

class ResultadoCuestionarioTemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoCuestionarioTema
        fields = "__all__"
        # campos que no se devuelven en las respuestas
        write_only_fields = ("is_status",)
        read_only_fields = ("created_at",)

class ProgresoEstudioTemaSerializer(serializers.ModelSerializer):
    tema = TemaSerializer(read_only=True)
    class Meta:
        model = ProgresoEstudio
        fields = "__all__"
        # campos que no se devuelven en las respuestas
        write_only_fields = ("is_status",)
        # Campos de solo lectura
        read_only_fields = ("created_at",)

