
# Funciona para formdata anidados
def process_nested_form_data(data):
    # Inicializa el diccionario resultante
    result = {
        "usuario": {},
    }

    # Procesar todos los datos del formulario
    for key, value in data.items():
        if key.startswith('usuario['):
            # Limpiar la clave para obtener el nombre del campo
            field_name = key[len('usuario['):-1]  # quita 'usuario[' y ']'
            if 'permiso' in field_name:  # Manejo especial para permisos
                # Inicializar la lista de permisos si no existe
                if 'permiso' not in result['usuario']:
                    result['usuario']['permiso'] = []
                # Extraer el índice y el valor del permiso
                result['usuario']['permiso'].append(int(value)) # los valores seran en str convertir a int
            else:
                # si no es permiso, agregamos normal
                result['usuario'][field_name] = value
        else:
            # Para los otros campos, se añaden directamente al diccionario
            result[key] = value

    return result

    