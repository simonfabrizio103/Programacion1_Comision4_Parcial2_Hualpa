# MÓDULO: validaciones.py
# RESPONSABILIDAD: Contener todas las funciones que interactúan con el
# ingreso de datos del usuario (input) y aseguran que sean correctos.
# Mantenemos funciones separadas (ej. _entero vs _entero_positivo)
# para cumplir con el Principio de Responsabilidad Única (SRP).

def validar_entero(mensaje):

    """
    Función base de validación numérica.
    Asegura que la entrada sea SÍ O SÍ un número entero (positivo, negativo o cero).
    """
    while True:
        try:
            entrada = input(mensaje)
            return int(entrada)
        except ValueError:
            print("❌ Entrada inválida. Se esperaba un valor numérico entero❗")


def validar_entero_positivo(mensaje):
    
    """
    Validación estricta de lógica de negocio (requisito Fase 3).
    Reutiliza validar_entero() y añade la restricción de que sea > 0.
    """
    while True:
        num = validar_entero(mensaje)
        if num > 0:
            return num
        else:
            print("❌ El valor debe ser positivo y mayor a cero.")


def validar_flotante_positivo(mensaje):
    
    """
    Validación estricta de lógica de negocio (requisito Fase 3).
    Asegura que sea un float y que sea > 0.
    """
    while True:
        try:
            entrada = input(mensaje)
            num = float(entrada)
            if num > 0:
                return num
            else:
                print("❌ El valor debe ser positivo y mayor a cero.")
        except ValueError:
            print("❌ Entrada inválida. Se esperaba un valor numérico (ej: 150.75)❗")


def validar_opcion_menu(mensaje, min_val, max_val):

    """
    Validación específica para menús.
    Reutiliza validar_entero() y añade la restricción de rango [min, max].
    Permite el 0 para la opción de "Salir".
    """
    while True:
        num = validar_entero(mensaje)
        if min_val <= num <= max_val:
            return num
        else:
            print(
                f"❌ Opción inválida. El número debe estar entre {min_val} y {max_val}.")


def validar_string_alfabetico(mensaje):

    """
    Validación estricta (requisito Fase 3).
    Asegura que la entrada no esté vacía (not entrada) y que no
    contenga números (any(char.isdigit())).
    Ideal para nombres de carpetas o ítems.
    """
    while True:
        entrada = input(mensaje).strip()

        if not entrada:
            print("❌ La entrada no puede estar vacía.")
        elif any(char.isdigit() for char in entrada):
            print("❌ La entrada no puede contener números.")
        else:
            return entrada


def validar_string_no_vacio(mensaje):

    """
    Validación genérica para campos de búsqueda.
    Solo valida que no esté vacío. Permite números y símbolos.
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        else:
            print("❌ La entrada no puede estar vacía.")


def normalizar_texto(texto):

    """
    Función de utilidad para búsquedas y filtros.
    Pasa a minúsculas y quita acentos para que las
    comparaciones no fallen (ej: "America" == "américa").
    """
    texto = texto.lower()
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'
    }
    for acento, sin_acento in reemplazos.items():
        texto = texto.replace(acento, sin_acento)
    return texto
