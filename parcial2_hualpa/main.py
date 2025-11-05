# Este es el archivo principal (CONTROLADOR).
# Orquesta el flujo: llama a VISTAS para mostrar y a FUNCIONES para procesar.

import funciones as fn
import vistas as vw
import validaciones as val
import os

def main():

    """Función principal: Controla el flujo de la aplicación."""

    # --- Definición del Dominio y Estructura (en español) ---
    DIRECTORIO_DATOS = "datos_paises"
    NIVELES_JERARQUIA = ['continente', 'region', 'gobierno']
    CAMPOS_CSV_ITEM = ['nombre', 'poblacion', 'superficie']
    # --- Fin Definición ---

    items_globales = []
    datos_cargados = False

    while True:

        # 1. Llamar a la VISTA para mostrar el menú
        vw.mostrar_menu()

        # 2. Llamar a VALIDACIONES para obtener la opción
        opcion = val.validar_opcion_menu(
            "➡️  Seleccione una opción (0-8): ", 0, 8)
        print()

        if opcion == 0:
            print("👋 Saliendo del sistema de Gestión Jerárquica... ¡Hasta pronto!")
            break

        elif opcion == 1:
            
            # 3. Llamar a FUNCIONES para la lógica (Lectura Recursiva)
            print(f"Leyendo datos desde '{DIRECTORIO_DATOS}'...")
            items_globales = fn.cargar_datos_recursivo(
                DIRECTORIO_DATOS, NIVELES_JERARQUIA)
            datos_cargados = True
            print(
                f"✅ Lectura completada. Se encontraron {len(items_globales)} ítems en total.")

        elif not datos_cargados and opcion not in [0, 2]:
            print("⚠️ Debe ejecutar la opción 1 (Cargar/Recargar Datos) primero.")

        elif opcion == 2:

            # Alta de Ítem
            if fn.alta_item(DIRECTORIO_DATOS, NIVELES_JERARQUIA, CAMPOS_CSV_ITEM):
                datos_cargados = False  # Forzar recarga

        elif opcion == 3:

            # Mostrar Ítems Totales
            vw.mostrar_items(items_globales, NIVELES_JERARQUIA)

        elif opcion == 4:

            # Filtrado
            vw.mostrar_menu_filtro()
            opcion_filtro = val.validar_opcion_menu(
                "Seleccione un filtro: ", 1, 3)
            
            # Llama a LÓGICA para filtrar (pasando el 1er nivel de la jerarquía)
            resultados = fn.filtrar_items(
                items_globales, NIVELES_JERARQUIA, opcion_filtro, NIVELES_JERARQUIA[0])
            
            # Llama a VISTA para mostrar
            vw.mostrar_resultados_filtro(resultados, NIVELES_JERARQUIA)

        elif opcion == 5:

            # Modificación
            if fn.modificar_item(items_globales, NIVELES_JERARQUIA, CAMPOS_CSV_ITEM):
                datos_cargados = False

        elif opcion == 6:

            # Eliminación
            if fn.eliminar_item(items_globales, NIVELES_JERARQUIA, CAMPOS_CSV_ITEM):
                datos_cargados = False

        elif opcion == 7:

            # Ordenamiento Global
            print("\n--- 🔀 Ordenar Ítems ---")
            while True:
                clave_in = input(
                    "Ordenar por (N)ombre, (P)oblación, (S)uperficie: ").strip().upper()
                if clave_in in ('N', 'P', 'S'):
                    break
                print("❌ Opción inválida.")

            clave_ordenamiento = {
                'N': 'nombre', 'P': 'poblacion', 'S': 'superficie'}.get(clave_in)

            while True:
                orden_in = input(
                    "Orden (A)scendente o (D)escendente: ").strip().upper()
                if orden_in in ('A', 'D'):
                    break
                print("❌ Opción inválida.")

            reverso = (orden_in == 'D')

            items_ordenados = fn.ordenar_items(
                items_globales, clave_ordenamiento, reverso)
            vw.mostrar_tabla_simple_ordenada(
                items_ordenados, clave_ordenamiento)

        elif opcion == 8:
            
            # Estadísticas
            stats_dict = fn.calcular_estadisticas(
                items_globales, NIVELES_JERARQUIA[0])
            vw.imprimir_estadisticas(stats_dict)


if __name__ == "__main__":
    main()