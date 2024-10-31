from rest_framework import serializers

from .models import Area, Tema


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"
        extra_kwargs = {
            # write_only => El campo NO se devuelve en las respuestas
            "is_status": {"write_only": True},

        }


class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = "__all__"
        read_only_fields = ("uuid",)  # Campo de solo lectura
        extra_kwargs = {
            # write_only => El campo NO se devuelve en las respuestas
            "is_status": {"write_only": True},
        }
    

class AreaAndTemaSerializer(serializers.ModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Tema
        fields = "__all__"
        read_only_fields = ("uuid",)  # Campo de solo lectura
        extra_kwargs = {
            # write_only => El campo NO se devuelve en las respuestas
            "is_status": {"write_only": True},
        }
