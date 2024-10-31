from rest_framework import serializers

def custom_number_validator(value):
    # debe ser numeros
    if not value.isdigit():
        raise serializers.ValidationError('Este campo debe contener solo números.')

    #  entre 5 y 12 dígitos, incluidos ellos mismos (5 y 12)
    if len(value) < 5 or len(value) > 12:
        raise serializers.ValidationError('Este campo debe contener entre 5 y 12 dígitos.')

    return value

def custom_ci_complemento_validator(value):
     # valor tenga 4 caracteres o menos
    if len(value) > 4:
        raise serializers.ValidationError('Este campo debe contener menos de 4 dígitos.')

    #  valor no contenga el carácter '-'
    if '-' in value:
        raise serializers.ValidationError('Este campo no debe contener el carácter "-"')

    return value

    