# MÓDULO: vistas.py
# RESPONSABILIDAD: Interfaz de Usuario (UI).
# Es el ÚNICO archivo que puede usar 'print()' para mostrar
# menús, tablas o resultados. No contiene lógica de negocio.

# NOTA: No necesita importar 'os' ni 'csv'.

def mostrar_menu():
    """(VISTA) Muestra el menú principal de opciones del sistema."""

    # Estética del menú
    borde_sup = "╭" + "─" * 53 + "╮"
    borde_inf = "╰" + "─" * 53 + "╯"
    borde_medio = "├" + "─" * 53 + "┤"
    linea_vacia = "│" + " " * 53 + "│"

    print("\n" + borde_sup)
    print(linea_vacia)

    # .center() se usa para alinear el texto
    print("│" + "🗃️  GESTIÓN JERÁRQUICA DE DATOS 🗃️".center(51) + "    │")
    print("│" + "UTN - Programación 1 (Parcial 2)".center(53) + "│")
    print(linea_vacia)
    print(borde_medio)

    # El f-string con :<"n" alinea el texto a la izquierda rellenando
    # con espacios hasta "n" caracteres.
    print(f"│ {'[1] 🔄  Cargar/Recargar Datos ':<50} │")
    print(f"│ {'[2] ➕  Alta de Ítem ':<49}  │")
    print(f"│ {'[3] 📚  Mostrar Ítems Totales ':<49}  │")
    print(f"│ {'[4] 🔎  Filtrar Ítems ':<49}  │")
    print(f"│ {'[5] ✏️   Modificar Ítem ':<51}  │")
    print(f"│ {'[6] ❌  Eliminar Ítem ':<49}  │")
    print(f"│ {'[7] 🔀  Ordenar Ítems ':<49}  │")
    print(f"│ {'[8] 📊  Ver Estadísticas ':<49}  │")
    print(borde_medio)

    print(f"│ {'[0] 🚪  Salir del Programa':<49}  │")
    print(borde_inf)


def mostrar_items(lista_items, niveles_jerarquia):
    
    """
    (VISTA) Muestra una lista de items formateada como tabla.
    """
    if not lista_items:
        print("ℹ️ No hay ítems para mostrar.")
        return

    # Construimos la cabecera de la tabla dinámicamente
    cabecera_jerarquia = " | ".join(
        [n.capitalize() for n in niveles_jerarquia])
    print(f"\n--- LISTADO DE {len(lista_items)} ÍTEMS ---")
    print()
    print(
        f"| {cabecera_jerarquia:<35} | {'Nombre':<30} | {'Población (hab)':>15} | {'Superficie (km²)':>18} |")
    print("-" * 111)

    for item in lista_items:

        # Mostramos la jerarquía (requisito Fase 3)
        jerarquia_str = " / ".join([item.get(n, 'N/A')
                                      for n in niveles_jerarquia])
        
        # Formateamos los números para que sean legibles
        # :, -> agrega separador de miles (1000000 -> 1,000,000)
        # :.2f -> formatea como flotante con 2 decimales
        pob_fmt = f"{item['poblacion']:,}"
        sup_fmt = f"{item['superficie']:,.2f}"

        # :<30 -> alinear a la izquierda, 30 espacios
        # :>15 -> alinear a la derecha, 15 espacios
        print(
            f"| {jerarquia_str:<35} | {item['nombre']:<30} | {pob_fmt:>15} | {sup_fmt:>18} |")

    print("-" * 111)


def mostrar_menu_filtro():
    """(VISTA) Muestra las sub-opciones de filtrado."""
    print("\n--- 🔎 Filtrar Ítems ---")
    print("[1] Filtrar por Nombre (parcial)")
    print("[2] Filtrar por Continente (1er nivel)")
    print("[3] Filtrar por Rango de Población")
    return


def mostrar_resultados_filtro(resultados, niveles_jerarquia):
    """(VISTA) Muestra el resultado de un filtro."""
    if resultados:
        print(f"✅ Se encontraron {len(resultados)} resultados:")
        # Reutilizamos la función mostrar_items, ¡buena práctica!
        mostrar_items(resultados, niveles_jerarquia)
    else:
        print("ℹ️ No se encontraron ítems que coincidan con el filtro.")


def mostrar_tabla_simple_ordenada(items_ordenados, clave_ordenamiento):
    """(VISTA) Muestra una tabla simplificada para la Opción 7."""
    print(f"\n✅ Ítems ordenados por '{clave_ordenamiento}':")
    print(f"| {'Nombre':<35} | {clave_ordenamiento.capitalize():>20} |")
    print("-" * 60)
    for item in items_ordenados:
        valor = item[clave_ordenamiento]
        # Formateo especial si es número
        if isinstance(valor, (int, float)):
            valor_fmt = f"{valor:,.2f}" if isinstance(
                valor, float) else f"{valor:,}"
            print(f"| {item['nombre']:<35} | {valor_fmt:>20} |")
        else:
            print(f"| {item['nombre']:<35} | {str(valor):>20} |")
    print("-" * 60)


def imprimir_estadisticas(stats_dict):
    """
    (VISTA) Recibe el diccionario de estadísticas de la lógica
    y lo "traduce" a un formato legible.
    """
    if not stats_dict:
        print("ℹ️ No hay datos cargados para calcular estadísticas.")
        return

    print("\n--- 📊 ESTADÍSTICAS GLOBALES ---")
    print(
        f"🌎 Total de ítems (países) registrados: {stats_dict['cantidad_total']}")
    print("-" * 40)
    print(
        f"📊 Promedio de Población: {stats_dict['promedio_poblacion']:,.0f} hab.")
    print(
        f"🗺️ Promedio de Superficie: {stats_dict['promedio_superficie']:,.2f} km²")
    print(f"Suma Total Población: {stats_dict['total_poblacion']:,} hab.")
    print("-" * 40)
    print(
        f"🥇 Mayor Población: {stats_dict['pais_mayor_pob']['nombre']} ({stats_dict['pais_mayor_pob']['poblacion']:,} hab.)")
    print(
        f"🥉 Menor Población: {stats_dict['pais_menor_pob']['nombre']} ({stats_dict['pais_menor_pob']['poblacion']:,} hab.)")
    print(
        f"🏞️ Mayor Superficie: {stats_dict['pais_mayor_sup']['nombre']} ({stats_dict['pais_mayor_sup']['superficie']:,.2f} km²)")
    print("-" * 40)
    print(f"🌍 Conteo por {stats_dict['primer_nivel_jerarquia'].capitalize()}:")
    # Usamos sorted() para que la lista de continentes salga ordenada
    for valor, cantidad in sorted(stats_dict['conteo_primer_nivel'].items()):
        print(f" - {valor}: {cantidad} ítems")
    print("-" * 40)
