from rest_framework import serializers
from .models import Estudiante
from apps.usuario.serializers import UsuarioSerializer


class UsuarioPersonalInstSerializer(serializers.ModelSerializer):
    # Anidamos serializadores
    usuario = UsuarioSerializer()

    class Meta:
        model = Estudiante
        fields = "__all__"
        # campos de solo lectura
        read_only_fields = (
            "created_at",
            "uuid",
        )
        extra_kwargs = {
            ""
        }
    def to_internal_value(self, data):
        """
        Sobreescribir el metodo para pasar la instancia de usuario
        """
        if self.instance["usuario"] and hasattr(self.instance, "usuario"):
            self.fields["usuario"] = UsuarioSerializer(instance=self.instance.usuario)
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        # Extrer los datos del usuario
        usuario_data = validated_data.pop("usuario")

        # crear nuevo usuario
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        if usuario_serializer.is_valid():
            usuario = usuario_serializer.save()
            
        # Crear el estudiante
        estudiante = Estudiante.objects.create(usuario = usuario, **validated_data)
        return estudiante
    
    def update (self, instance, validated_data):
        # Extraer datos del usuario
        usuario_data = validated_data,pop("usuario", None)

        # Actualizar datos del usuario solo si tenemos
        if usuario_data:
            usuario_serializer = UsuarioSerializer(instance = instance.usuario, data=usuario_data, partial=True)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
        
        # Actualizar campos del usuario
        for attr, value  in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance





