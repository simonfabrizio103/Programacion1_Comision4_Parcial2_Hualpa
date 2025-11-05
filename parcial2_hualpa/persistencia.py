# MÓDULO: persistencia.py
# RESPONSABILIDAD: Capa de Acceso a Datos (Data Access Layer).
# Es el ÚNICO archivo que sabe cómo leer y escribir en el disco.
# No contiene lógica de negocio, solo operaciones de I/O (Input/Output).
# Importa csv y os.

import csv
import os


def leer_csv_items(ruta_archivo_csv, jerarquia_info):
    
    """
    (PERSISTENCIA) Lee un archivo CSV específico.
    Recibe la ruta completa del archivo y el diccionario de jerarquía
    (ej: {'continente': 'America'}) y los fusiona con los datos del CSV.
    Maneja excepciones de archivos corruptos.
    """
    items = []
    try:
        # Usamos 'with open' para garantizar que el archivo se cierre
        # automáticamente, incluso si hay un error. (Requisito Fase 2)
        with open(ruta_archivo_csv, 'r', encoding='utf-8', newline='') as f:

            # DictReader es ideal porque lee directo a diccionarios.
            reader = csv.DictReader(f)
            for fila in reader:
                try:
                    # Convertimos los tipos de datos leídos (que son strings)
                    # a los tipos correctos (int, float).
                    item = {
                        'nombre': fila['nombre'],
                        'poblacion': int(fila['poblacion']),
                        'superficie': float(fila['superficie']),
                        **jerarquia_info,  # Desempaqueta el dict de jerarquía
                        'ruta_archivo': ruta_archivo_csv  # Guardamos la ruta para Modificar/Eliminar
                    }
                    items.append(item)
                except (ValueError, KeyError, TypeError) as e:

                    # Si una fila está mal (ej. "poblacion": "abc"), la saltamos.
                    print(
                        f"⚠️ Fila corrupta en {ruta_archivo_csv} omitida: {e}")
    except FileNotFoundError:

        # Manejo de excepción obligatorio (Requisito Fase 2)
        print(f"❌ Error: No se encontró el archivo {ruta_archivo_csv}")
    except Exception as e:
        print(f"❌ Error inesperado al leer {ruta_archivo_csv}: {e}")
    return items


def reescribir_csv_especifico(ruta_archivo, items_del_archivo, campos_item_csv):

    """
    (PERSISTENCIA) Sobrescribe (modo 'w') un archivo CSV.
    Se usa para Modificar y Eliminar. Recibe la lista COMPLETA de ítems
    que deben quedar en ese archivo y lo re-escribe desde cero.
    """
    try:
        # Usamos modo 'w' (write/escribir) para borrar el contenido
        # anterior y escribir el nuevo. (Requisito Fase 3 - Update/Delete)
        with open(ruta_archivo, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=campos_item_csv)
            writer.writeheader()  # Siempre escribimos la cabecera

            for item in items_del_archivo:
                
                # Nos aseguramos de escribir solo los campos del CSV,
                # no los de jerarquía (ej. 'continente').
                item_para_csv = {campo: item[campo]
                                 for campo in campos_item_csv}
                writer.writerow(item_para_csv)
        return True

    except (OSError, csv.Error) as e:
        print(
            f"❌ Error Crítico: No se pudo sobrescribir el archivo {ruta_archivo}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al reescribir {ruta_archivo}: {e}")
        return False


def agregar_item_csv(ruta_archivo_csv, item_para_csv, campos_item_csv):

    """
    (PERSISTENCIA) Agrega una nueva fila a un CSV (modo 'a').
    Se usa para el Alta.
    """
    try:
        # Comprobamos si el archivo existe para decidir si escribimos
        # la cabecera (nombre,poblacion,superficie) o no.
        archivo_existe = os.path.exists(ruta_archivo_csv)

        # Usamos modo 'a' (append/agregar) para añadir una línea al final
        # sin borrar lo que ya existe. (Requisito Fase 3 - Create)
        with open(ruta_archivo_csv, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=campos_item_csv)

            if not archivo_existe:
                writer.writeheader()  # Escribir cabecera solo si es un archivo nuevo

            writer.writerow(item_para_csv)
        return True

    except OSError as e:
        print(
            f"❌ Error de Sistema Operativo al escribir en {ruta_archivo_csv}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado durante la escritura: {e}")
        return False
