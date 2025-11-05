# MÓDULO: funciones.py
# RESPONSABILIDAD: Lógica de Negocio (Business Logic). El "motor".
# Orquesta las operaciones. Llama a 'persistencia.py' para datos
# y a 'validaciones.py' para la entrada.
# NO imprime menús ni tablas (eso lo hace 'vistas.py').

import os
# Importamos nuestros propios módulos
import persistencia as db
import validaciones as val

# --- Fase 2: Implementación Técnica Centralizada ---


def cargar_datos_recursivo(ruta_base, niveles_jerarquia, ruta_relativa=""):
    
    """
    (LÓGICA) REQUISITO OBLIGATORIO (Fase 2 - Recursividad).
    Recorre la estructura de carpetas y recolecta todos los ítems.
    """
    items_globales = []

    # os.path.join es crucial para compatibilidad (Linux/Windows)
    ruta_actual = os.path.join(ruta_base, ruta_relativa)

    try:

        # Iteramos sobre todo lo que hay en la carpeta actual
        for entry in os.listdir(ruta_actual):
            path_completo_abs = os.path.join(ruta_actual, entry)
            path_completo_rel = os.path.join(ruta_relativa, entry)

            # --- PASO RECURSIVO ---
            # Si es un directorio, nos volvemos a llamar a nosotros mismos
            # para "meternos" en esa subcarpeta.
            if os.path.isdir(path_completo_abs):
                items_globales.extend(
                    cargar_datos_recursivo(
                        ruta_base, niveles_jerarquia, path_completo_rel)
                )

            # --- CASO BASE ---
            # Si es un archivo .csv, dejamos de "bajar" y leemos el contenido.
            elif entry.endswith('.csv'):
                # Creamos el dict de jerarquía basado en la ruta de carpetas
                partes_ruta = ruta_relativa.split(os.sep)
                jerarquia_info = {}

                if len(partes_ruta) == len(niveles_jerarquia):
                    jerarquia_info = dict(zip(niveles_jerarquia, partes_ruta))

                # Llamamos a la capa de persistencia para leer el archivo
                items_globales.extend(
                    db.leer_csv_items(path_completo_abs, jerarquia_info)
                )

    except FileNotFoundError:

        # Manejo de error si la carpeta 'datos_paises' no existe la primera vez
        if not ruta_relativa:
            print(
                f"ℹ️ Directorio base '{ruta_base}' no existe. Se creará al agregar datos.")
    except Exception as e:
        print(f"❌ Error al escanear directorio {ruta_actual}: {e}")

    return items_globales

# --- Fase 3: Funcionalidades Mínimas (CRUD) ---


def alta_item(ruta_base, niveles_jerarquia, campos_item_csv):

    """
    (LÓGICA - CREATE) Pide datos, crea la estructura de carpetas
    y llama a persistencia para guardar.
    """
    print("\n--- ➕ Alta de Nuevo Ítem ---")
    nuevo_item_memoria = {}
    jerarquia_valores = []

    # 1. Pedir los 3 niveles de jerarquía
    for nivel in niveles_jerarquia:
        valor = val.validar_string_alfabetico(f"Ingrese {nivel}: ")
        jerarquia_valores.append(valor)
        nuevo_item_memoria[nivel] = valor

    # 2. Pedir atributos del ítem (Validaciones Estrictas)
    nuevo_item_memoria['nombre'] = val.validar_string_alfabetico(
        "Ingrese Nombre del país: ")
    nuevo_item_memoria['poblacion'] = val.validar_entero_positivo(
        "Ingrese Población: ")
    nuevo_item_memoria['superficie'] = val.validar_flotante_positivo(
        "Ingrese Superficie (km²): ")

    try:
        # 3. Crear estructura de carpetas (Requisito Fase 3)
        # ej: ['America', 'Sur', 'Republica'] -> 'datos_paises/America/Sur/Republica'
        ruta_directorio_final = os.path.join(ruta_base, *jerarquia_valores)

        # os.makedirs crea todas las carpetas necesarias. exist_ok=True
        # evita que crashee si las carpetas ya existen.
        os.makedirs(ruta_directorio_final, exist_ok=True)
        ruta_archivo_csv = os.path.join(ruta_directorio_final, "items.csv")

        # 4. Preparar el dict que se enviará al CSV
        item_para_csv = {
            campo: nuevo_item_memoria[campo] for campo in campos_item_csv
        }

        # 5. Llamar a persistencia para guardar (modo 'a')
        if db.agregar_item_csv(ruta_archivo_csv, item_para_csv, campos_item_csv):
            print(
                f"✅ Ítem '{nuevo_item_memoria['nombre']}' agregado exitosamente en:")
            print(f"   {ruta_archivo_csv}")
            return True
        else:
            print("❌ Fallo al guardar el ítem en el archivo CSV.")
            return False

    except OSError as e:
        print(f"❌ Error de Sistema Operativo al crear directorios: {e}")
    except Exception as e:
        print(f"❌ Error inesperado durante el alta: {e}")

    return False


def filtrar_items(items_globales, niveles_jerarquia, opcion, primer_nivel_key):

    """
    (LÓGICA - READ) Filtra la lista global en memoria.
    No necesita llamar a persistencia, solo procesa la lista.
    """
    resultados = []

    if opcion == 1:  # Por nombre
        busqueda = val.validar_string_no_vacio(
            "Ingrese el nombre (o parte) a buscar: ")
        busqueda_norm = val.normalizar_texto(busqueda)
        resultados = [
            item for item in items_globales
            if busqueda_norm in val.normalizar_texto(item['nombre'])
        ]

    elif opcion == 2:  # Por 1er Nivel (Continente)
        busqueda = val.validar_string_alfabetico(
            f"Ingrese {primer_nivel_key} a filtrar: ")
        busqueda_norm = val.normalizar_texto(busqueda)
        resultados = [
            item for item in items_globales
            if val.normalizar_texto(item[primer_nivel_key]) == busqueda_norm
        ]

    elif opcion == 3:  # Por Rango de Población
        print("Ingrese el rango de población:")
        min_pob = val.validar_entero_positivo("Valor mínimo: ")
        max_pob = val.validar_entero_positivo("Valor máximo: ")

        if min_pob > max_pob:
            print("❌ El valor mínimo no puede ser mayor que el máximo.")
            return []

        resultados = [
            item for item in items_globales
            if min_pob <= item['poblacion'] <= max_pob
        ]

    return resultados


def _buscar_item_unico(items_globales, niveles_jerarquia):

    """
    Helper (LÓGICA): Función interna para U/D (Update/Delete).
    Permite al usuario encontrar un ítem específico por nombre exacto.
    Maneja el caso de nombres duplicados en diferentes jerarquías.
    """
    busqueda = val.validar_string_no_vacio(
        "Ingrese el nombre exacto del ítem: ")
    busqueda_norm = val.normalizar_texto(busqueda)

    # Busca en la lista global en memoria
    resultados = [
        item for item in items_globales
        if val.normalizar_texto(item['nombre']) == busqueda_norm
    ]

    if not resultados:
        print(f"ℹ️ No se encontró ningún ítem con el nombre '{busqueda}'.")
        return None

    if len(resultados) == 1:
        return resultados[0]  # Se encontró uno solo, perfecto.

    # Si hay > 1, le pedimos al usuario que desambigüe.
    print("⚠️ Se encontraron múltiples ítems con ese nombre. Seleccione el correcto:")
    for i, item in enumerate(resultados):
        jerarquia_str = " / ".join([item.get(n, 'N/A')
                                      for n in niveles_jerarquia])
        print(f"  [{i+1}] {item['nombre']} (Ubicación: {jerarquia_str})")

    opcion = val.validar_opcion_menu(
        "Seleccione el número de ítem: ", 1, len(resultados))
    return resultados[opcion - 1]  # Devuelve el ítem elegido


def modificar_item(items_globales, niveles_jerarquia, campos_item_csv):

    """
    (LÓGICA - UPDATE) Modifica un ítem.
    1. Busca en memoria. 2. Modifica en memoria. 3. Llama a persistencia.
    """
    if not items_globales:
        print("ℹ️ No hay datos cargados para modificar.")
        return False

    print("\n--- ✏️ Modificar Ítem ---")

    # 1. Identificar el ítem
    item_a_modificar = _buscar_item_unico(items_globales, niveles_jerarquia)
    if not item_a_modificar:
        return False  # No se encontró

    print(f"Modificando: {item_a_modificar['nombre']}")
    print("[1] Nombre\n[2] Población\n[3] Superficie")
    opcion = val.validar_opcion_menu("Seleccione atributo: ", 1, 3)

    atributo_key = ""
    nuevo_valor = None

    try:
        # 2. Pedir y validar nuevo valor (Validaciones Estrictas)
        if opcion == 1:
            atributo_key = "nombre"
            nuevo_valor = val.validar_string_alfabetico(
                "Ingrese nuevo nombre: ")
        elif opcion == 2:
            atributo_key = "poblacion"
            nuevo_valor = val.validar_entero_positivo(
                "Ingrese nueva población: ")
        elif opcion == 3:
            atributo_key = "superficie"
            nuevo_valor = val.validar_flotante_positivo(
                "Ingrese nueva superficie: ")

        # 3. Modificar el ítem en la lista de memoria
        item_a_modificar[atributo_key] = nuevo_valor
        print("Ítem actualizado en memoria.")

        # 4. Preparar datos para persistencia
        # Necesitamos la ruta del archivo que vamos a sobrescribir
        ruta_archivo = item_a_modificar['ruta_archivo']

        # Creamos una lista solo con los ítems que pertenecen a ESE MISMO archivo
        items_del_mismo_archivo = [
            item for item in items_globales
            if item['ruta_archivo'] == ruta_archivo
        ]

        # 5. Llamar a persistencia para re-escribir (modo 'w')
        print(f"Re-escribiendo archivo: {ruta_archivo}...")
        if db.reescribir_csv_especifico(ruta_archivo, items_del_mismo_archivo, campos_item_csv):
            print("✅ Modificación guardada exitosamente en disco.")
            return True
        else:
            print("❌ Fallo al guardar en disco.")
            return False

    except Exception as e:
        print(f"❌ Error durante la modificación: {e}")
        return False


def eliminar_item(items_globales, niveles_jerarquia, campos_item_csv):

    """
    (LÓGICA - DELETE) Elimina un ítem.
    1. Busca en memoria. 2. Elimina de memoria. 3. Llama a persistencia.
    """
    if not items_globales:
        print("ℹ️ No hay datos cargados para eliminar.")
        return False

    print("\n--- ❌ Eliminar Ítem ---")

    # 1. Identificar el ítem
    item_a_eliminar = _buscar_item_unico(items_globales, niveles_jerarquia)
    if not item_a_eliminar:
        return False

    # Confirmación de seguridad
    confirmacion = input(
        f"¿Está seguro de eliminar '{item_a_eliminar['nombre']}'? (S/N): ").strip().upper()
    if confirmacion != 'S':
        print("Cancelado. No se eliminó el ítem.")
        return False

    try:
        # Guardamos la ruta ANTES de borrar el ítem
        ruta_archivo = item_a_eliminar['ruta_archivo']
        
        # 2. Eliminar el ítem de la lista de memoria
        items_globales.remove(item_a_eliminar)
        print("Ítem eliminado de la memoria.")

        # 3. Preparar datos para persistencia
        # Buscamos los ítems *restantes* de ese mismo archivo
        items_restantes_del_archivo = [
            item for item in items_globales
            if item['ruta_archivo'] == ruta_archivo
        ]

        # 4. Llamar a persistencia (modo 'w')
        print(f"Re-escribiendo archivo: {ruta_archivo}...")
        if db.reescribir_csv_especifico(ruta_archivo, items_restantes_del_archivo, campos_item_csv):
            print("✅ Eliminación guardada exitosamente en disco.")
            return True
        else:
            print("❌ Fallo al guardar en disco.")
            return False

    except ValueError:
        print("❌ Error: No se pudo remover el ítem de la lista.")
        return False
    except Exception as e:
        print(f"❌ Error inesperado during la eliminación: {e}")
        return False

# --- Funciones de Lógica Pura (Adicionales) ---


def ordenar_items(items_globales, clave_ordenamiento, reverso):

    """
    (LÓGICA) Ordena la lista global en memoria usando sorted().
    """
    if not items_globales:
        return []

    # sorted() es una función muy potente. Le decimos que ordene la lista
    # usando como "llave" (key) el valor de cada diccionario para
    # la clave_ordenamiento (ej. 'poblacion').
    items_ordenados = sorted(
        items_globales, key=lambda item: item[clave_ordenamiento], reverse=reverso)
    return items_ordenados


def calcular_estadisticas(items_globales, primer_nivel_jerarquia):

    """
    (LÓGICA) Calcula todas las estadísticas y devuelve un diccionario.
    Esto es lógica pura, solo procesa la lista global.
    """
    if not items_globales:
        return None  # No hay datos para calcular

    # 1. Cantidad total
    cantidad_total = len(items_globales)

    # 2. Sumas y Promedios
    total_poblacion = sum(item['poblacion'] for item in items_globales)
    total_superficie = sum(item['superficie'] for item in items_globales)

    promedio_poblacion = total_poblacion / cantidad_total
    promedio_superficie = total_superficie / cantidad_total

    # 3. Máximos y Mínimos (usando 'max' con una 'key')
    pais_mayor_pob = max(items_globales, key=lambda p: p['poblacion'])
    pais_menor_pob = min(items_globales, key=lambda p: p['poblacion'])
    pais_mayor_sup = max(items_globales, key=lambda p: p['superficie'])

    # 4. Conteo por 1er Nivel (Requisito Fase 3)
    conteo_primer_nivel = {}
    for item in items_globales:
        valor_nivel = item.get(primer_nivel_jerarquia, 'Sin Categoría')
        
        # .get(valor, 0) + 1 es un truco para contar:
        # "Obtén el conteo actual (o 0 si no existe) y súmale 1"
        conteo_primer_nivel[valor_nivel] = conteo_primer_nivel.get(
            valor_nivel, 0) + 1

    # 5. Empaquetamos todo en un solo diccionario para enviarlo a la VISTA
    stats_dict = {
        'cantidad_total': cantidad_total,
        'total_poblacion': total_poblacion,
        'promedio_poblacion': promedio_poblacion,
        'promedio_superficie': promedio_superficie,
        'pais_mayor_pob': pais_mayor_pob,
        'pais_menor_pob': pais_menor_pob,
        'pais_mayor_sup': pais_mayor_sup,
        'conteo_primer_nivel': conteo_primer_nivel,
        'primer_nivel_jerarquia': primer_nivel_jerarquia
    }
    return stats_dict
