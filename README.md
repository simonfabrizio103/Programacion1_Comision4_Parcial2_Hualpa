# Programacion1_Comision4_Parcial2_Hualpa

## Video Explicativo (Entregable Fase 1)

Aquí puedes ver la presentación y explicación del proyecto, cumpliendo con el requisito de la Fase 1.

* **Enlace al video:** [Ver Video en Google Drive](https://drive.google.com/file/d/16KbXzNVso0jqRdE6VfxP7MIPAo3uC6Os/view?usp=drive_link)

---

## 1. Diseño y Estructura de Datos (Fase 1)

El diseño se basa en mapear una estructura de datos lógica a una estructura física de carpetas en el sistema de archivos.

### Dominio y Jerarquía

* **Dominio Elegido:** Gestión de Países.
* **Niveles de Jerarquía (3):**
    1.  `continente`
    2.  `region`
    3.  `gobierno` (Tipo de Gobierno)

### Lógica de Almacenamiento (Basada en Directorios)

La lógica consiste en que la ruta de carpetas *representa* los metadatos de los ítems que contiene. Los ítems (países) se almacenan en un archivo `items.csv` al final de la ruta jerárquica.

**Ejemplo de Estructura de Directorios:**
```
datos_paises/
└── America/
    ├── Norte/
    │   └── Republica/
    │       └── items.csv
    └── Sur/
        ├── Monarquia/
        │   └── items.csv
        └── Republica/
            └── items.csv
└── Europa/
    └── Occidental/
        └── Republica/
            └── items.csv
```

### Formato de Almacenamiento (CSV)

El archivo `items.csv` al final de cada ruta contiene **solo los atributos del ítem**, definidos en `main.py` como `CAMPOS_CSV_ITEM`:
* `nombre`
* `poblacion`
* `superficie`

**Ejemplo (`.../America/Sur/Republica/items.csv`):**
```csv
nombre,poblacion,superficie
Argentina,47000000,2780400
Chile,19000000,756102
```

### Estructura Interna (Diccionario Python)

Cuando la **función recursiva (Opción 1)** lee el sistema de archivos, consolida cada país en un único diccionario de Python. Este diccionario fusiona los datos del CSV con los datos de la jerarquía (la ruta) y añade la ruta del archivo para futuras modificaciones.
```python
{
    # Atributos del CSV
    'nombre': 'Argentina',
    'poblacion': 47000000,
    'superficie': 2780400,
    
    # Atributos de la Jerarquía (de la ruta)
    'continente': 'America',
    'region': 'Sur',
    'gobierno': 'Republica',
    
    # Metadato clave para Modificar/Eliminar
    'ruta_archivo': 'datos_paises/America/Sur/Republica/items.csv'
}
```

## 2. Arquitectura del Software (Modularización)

Para cumplir con las buenas prácticas, el proyecto está modularizado en **5 archivos** con responsabilidades claramente definidas:

* `main.py` (**Controlador**): Define las constantes globales (`DIRECTORIO_DATOS`, `NIVELES_JERARQUIA`, etc.) y contiene el bucle principal del menú. Orquesta las llamadas a las otras capas.
* `vistas.py` (**Vista**): Es el único archivo que usa `print()` para mostrar menús, tablas y resultados.
* `funciones.py` (**Lógica de Negocio**): El "motor" del programa. Contiene la función `cargar_datos_recursivo`, `alta_item`, `filtrar_items`, `calcular_estadisticas`, etc. Llama a `persistencia` y `validaciones`.
* `persistencia.py` (**Acceso a Datos**): Es el único archivo que sabe leer (`csv.DictReader`) y escribir (`csv.DictWriter`) archivos CSV. Usa `with open` y maneja los modos `'a'` (append) y `'w'` (write).
* `validaciones.py` (**Utilidades**): Contiene todas las funciones de validación de entrada (`validar_entero_positivo`, `validar_string_alfabetico`, etc.) para cumplir con las **Validaciones Estrictas** de la Fase 3.

## 3. Instrucciones de Uso

### Prerrequisitos

* Tener **Python 3.x** instalado.

### Ejecución

1.  Descargar o clonar el repositorio (asegúrate de incluir la carpeta `datos_paises`).
2.  Colocar los 5 archivos `.py` y la carpeta `datos_paises` en la misma ubicación.
3.  Abrir una terminal (como PowerShell o CMD) en esa carpeta.
4.  Ejecutar el programa con el siguiente comando:
    ```bash
    python main.py
    ```
    (o `py main.py` si `python` no está en tu PATH)

### Primeros Pasos

El repositorio ya incluye una carpeta `datos_paises` con datos de ejemplo.

1.  **Use la Opción [1] (Cargar/Recargar Datos)** primero.
    * Esto ejecutará la función recursiva para leer toda la estructura de carpetas y archivos CSV que ya están en el repositorio.
2.  **Use la Opción [3] (Mostrar Ítems Totales)**.
    * Podrá ver inmediatamente todos los países de ejemplo cargados.
3.  **¡Listo!** Ahora puede probar las demás opciones:
    * Use la **Opción [2] (Alta de Ítem)** para agregar un nuevo país (ej. "Argentina").
    * Use el resto de opciones (Filtrar, Modificar, Eliminar, etc.) sobre los datos ya cargados.
