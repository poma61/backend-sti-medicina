from rest_framework import serializers


def custom_number_validator(value):
    if not value.isdigit():
        raise serializers.ValidationError('Este campo debe contener solo números.')
    return value



