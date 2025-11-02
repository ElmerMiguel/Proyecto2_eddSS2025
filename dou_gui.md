# 📚 Documentación - Módulos GUI

Documentacion gui

---

## 📄 config.py

**Propósito:** Centralizar todas las constantes, colores y configuraciones globales de la GUI.

**Contenido:**

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `BG_COLOR` | Color de fondo principal | `#e6f0ff` (azul claro) |
| `TITLE_COLOR` | Color de títulos | `#2a2a72` (azul oscuro) |
| `BUTTON_COLOR` | Color de botones | `#4a90e2` (azul medio) |
| `FILTER_BG` | Color de filtros/frames | `#d9e4f5` (azul muy claro) |
| `ACCENT_COLOR` | Color de énfasis | `#1e6bbd` (azul intenso) |
| `DASH_CARD_BG` | Color fondo tarjetas | `#ffffff` (blanco) |
| `WINDOW_TITLE` | Título de la ventana | "📚 Biblioteca Mágica..." |
| `WINDOW_GEOMETRY` | Tamaño ventana inicial | `1200x800` |
| `THEME` | Tema TTK | `clam` |

**Funciones:** Ninguna (solo constantes)

**Cómo usarlo:**

```python
from gui.config import BG_COLOR, FONT_TITLE_LARGE
# Usar en labels, frames, etc.
```

**Cuándo modificar:**

- Cambiar esquema de colores
- Ajustar tamaño inicial de ventana
- Modificar fuentes globales

---

## 📄 styles.py

**Propósito:** Configurar todos los estilos TTK (tema, botones, pestañas, etc.) de forma centralizada.

**Funciones principales:**

### `configurar_estilos(root)`

```python
def configurar_estilos(root):
    """
    Configura todos los estilos ttk de la aplicación

    Args:
        root (tk.Tk): Ventana raíz de tkinter

    Returns:
        ttk.Style: Objeto de estilo configurado
    """
```

**Qué configura:**

- Estilo de Notebook (pestañas)
- Estilo de Buttons (botones)
- Estilo de Labels
- Estilo de Checkbuttons y Radiobuttons
- Efectos hover en botones

**Cómo usarlo:**

```python
from gui.styles import configurar_estilos

root = tk.Tk()
configurar_estilos(root)  # Debe llamarse UNA sola vez
```

**Cuándo modificar:**

- Cambiar tamaño de fuentes globales
- Ajustar padding o border en widgets
- Agregar nuevos estilos personalizados

---

## 📄 __init__.py

**Propósito:** Convertir la carpeta gui en un paquete Python y exportar las funciones principales para importarlas fácilmente.

**Exporta:**

```python
from .config import *                    # Todas las constantes
from .styles import configurar_estilos   # Función de estilos
from .dashboard_tab import crear_dashboard
from .catalogo_tab import crear_catalogo_tab
from .red_tab import crear_red_tab
from .busqueda_tab import crear_busqueda_rutas_tab
from .simulacion_tab import crear_simulacion_tab
from .visualizacion_tab import crear_visualizacion_tab
from .pruebas_tab import crear_pruebas_carga_tab
```

**Cómo usarlo:**

```python
# En lugar de: from gui.dashboard_tab import crear_dashboard
# Puedes: from gui import crear_dashboard
```

**Cuándo modificar:**

- Agregar nuevas pestañas
- Cambiar importaciones públicas

---

## 📄 dashboard_tab.py

**Propósito:** Crear la pestaña de inicio (Dashboard) con tarjetas interactivas que redirigen a otras pestañas.

**Funciones principales:**

### `crear_dashboard(notebook)`

```python
def crear_dashboard(notebook):
    """
    Crear y retornar la pestaña de Dashboard

    Args:
        notebook (ttk.Notebook): Widget notebook padre

    Returns:
        ttk.Frame: Frame de la pestaña dashboard
    """
```

**Funciones internas:**

### `crear_tarjeta_info(parent, emoji, titulo, descripcion, fila, col, color, indice_tab)`

Crea una tarjeta visual interactiva con:

- Emoji grande
- Título de sección
- Descripción
- Click para cambiar a tab

**Tarjetas creadas:**

1. 📘 Catálogo y Libro (CRUD)
2. 🏛️ Red de Bibliotecas
3. 🗺️ Rutas y Búsqueda
4. ⏳ Simulación de Flujo
5. 🌳 Visualización Estructuras
6. 📈 Pruebas y Carga CSV

**Cómo usarlo:**

```python
from gui.dashboard_tab import crear_dashboard

notebook = ttk.Notebook(root)
crear_dashboard(notebook)
```

**Cuándo modificar:**

- Agregar nuevas tarjetas
- Cambiar descripciones
- Añadir nuevas funcionalidades al click

---

## 📄 catalogo_tab.py

**Propósito:** Crear la pestaña de gestión de catálogo con operaciones CRUD de libros.

**Clases principales:**

### `CatalogoTab`

Controlador de la pestaña que maneja:

- Variables de entrada (formulario)
- Actualización del árbol de visualización
- Operaciones CRUD

**Métodos principales:**

#### `agregar_libro()`

Agrega un nuevo libro al catálogo con:

- Validación de campos obligatorios
- Creación de objeto Libro
- Asignación a biblioteca
- Programación de transferencias

#### `eliminar_libro()`

Elimina libro seleccionado del árbol y base de datos

#### `actualizar_catalogo_tree()`

Recarga el TreeView mostrando todos los libros de todas las bibliotecas

#### `actualizar_comboboxes_origen_destino(combo_origen, combo_destino)`

Llena los dropdowns con IDs de bibliotecas disponibles

#### `rollback_operacion()`

Deshace la última operación usando pilas

**Función principal:**

### `crear_catalogo_tab(notebook, red_bibliotecas)`

```python
def crear_catalogo_tab(notebook, red_bibliotecas):
    """
    Crear y retornar la pestaña de Catálogo

    Args:
        notebook (ttk.Notebook): Widget notebook padre
        red_bibliotecas (RedBibliotecas): Instancia del backend

    Returns:
        ttk.Frame: Frame de la pestaña catálogo
    """
```

**Campos del formulario:**

- Título (texto)
- Autor (texto)
- ISBN (texto)
- Año (número)
- Género (texto)
- Estado (combo: disponible, prestado, en_transito, agotado)
- Biblioteca Origen (combo)
- Biblioteca Destino (combo)
- Prioridad (radio: tiempo/costo)

**TreeView mostraba:**

| Columna | Descripción |
| --- | --- |
| Título | Nombre del libro |
| Autor | Autor del libro |
| ISBN | Código único |
| Estado | Estado actual |
| Biblioteca | Ubicación |

**Cómo usarlo:**

```python
from gui.catalogo_tab import crear_catalogo_tab

tab_catalogo = crear_catalogo_tab(notebook, red_bibliotecas)
```

**Cuándo modificar:**

- Agregar más campos al formulario
- Cambiar validaciones
- Modificar estructura del árbol

---

## 📄 red_tab.py

**Propósito:** Crear la pestaña de gestión de la red de bibliotecas y conexiones (Grafo).

**Clases principales:**

### `RedTab`

Controlador de la pestaña que maneja:

- Creación de bibliotecas
- Conexiones entre bibliotecas
- Visualización del grafo

**Métodos principales:**

#### `agregar_biblioteca()`

Crea nueva biblioteca con:

- ID automático (BIB001, BIB002, etc)
- Nombre, ubicación, tiempos
- Agrega nodo al grafo

#### `agregar_conexion()`

Crea arista entre dos bibliotecas:

- Tiempo de conexión
- Costo de conexión
- Opción bidireccional

#### `actualizar_comboboxes_conexiones(origen_combo, destino_combo)`

Llena dropdowns con bibliotecas disponibles

#### `dibujar_grafo()`

Dibuja el grafo en el canvas:

- Nodos en círculo
- Aristas con pesos
- Colores personalizados

**Función principal:**

### `crear_red_tab(notebook, red_bibliotecas, callback_actualizar=None, callback_dibujar=None)`

```python
def crear_red_tab(notebook, red_bibliotecas, callback_actualizar=None, callback_dibujar=None):
    """
    Crear y retornar la pestaña de Red

    Args:
        notebook (ttk.Notebook): Widget notebook padre
        red_bibliotecas (RedBibliotecas): Instancia del backend
        callback_actualizar (callable): Función para actualizar UI
        callback_dibujar (callable): Función para redibujar grafo

    Returns:
        tuple: (Frame, RedTab) - Tab y controlador
    """
```

**Campos para biblioteca:**

- Nombre (texto)
- Ubicación (texto)
- Tiempo Ingreso (número)
- Tiempo Traspaso (número)
- Intervalo Despacho (número)

**Campos para conexión:**

- Origen (combo)
- Destino (combo)
- Tiempo (número)
- Costo (número)
- Bidireccional (checkbox)

**Cómo usarlo:**

```python
from gui.red_tab import crear_red_tab

tab_red, ctrl_red = crear_red_tab(
    notebook, 
    red_bibliotecas,
    callback_actualizar=actualizar_func,
    callback_dibujar=dibujar_func
)
```

**Cuándo modificar:**

- Cambiar algoritmo de posicionamiento de nodos
- Agregar nuevas propiedades de bibliotecas
- Mejorar visualización del grafo

---

## 📄 busqueda_tab.py

**Propósito:** Crear la pestaña de búsqueda avanzada y cálculo de rutas óptimas.

**Clases principales:**

### `BusquedaTab`

Controlador que maneja:

- 4 tipos de búsqueda
- Cálculo de rutas óptimas con Dijkstra
- Visualización de resultados

**Métodos de búsqueda:**

#### `buscar_por_titulo()`

Busca usando AVL (árbol binario balanceado)

#### `buscar_por_isbn()`

Busca usando Hash (tabla hash)

#### `buscar_por_genero()`

Busca usando B+ (árbol B+)

#### `buscar_por_rango()`

Busca por rango de años usando Árbol B

#### `calcular_ruta_optima()`

Calcula ruta entre dos bibliotecas usando:

- Dijkstra por tiempo
- Dijkstra por costo

**Función principal:**

### `crear_busqueda_rutas_tab(notebook, red_bibliotecas)`

```python
def crear_busqueda_rutas_tab(notebook, red_bibliotecas):
    """
    Crear y retornar la pestaña de Búsqueda y Rutas

    Args:
        notebook (ttk.Notebook): Widget notebook padre
        red_bibliotecas (RedBibliotecas): Instancia del backend

    Returns:
        tuple: (Frame, BusquedaTab) - Tab y controlador
    """
```

**Secciones:**

**Búsqueda Avanzada:**

- Por Título (AVL)
- Por ISBN (HASH)
- Por Género (B+)
- Por Rango de Fechas (Árbol B)

**Cálculo de Rutas:**

- Biblioteca Origen (combo)
- Biblioteca Destino (combo)
- Criterio (radio: tiempo/costo)

**Cómo usarlo:**

```python
from gui.busqueda_tab import crear_busqueda_rutas_tab

tab_busqueda, ctrl_busqueda = crear_busqueda_rutas_tab(
    notebook, 
    red_bibliotecas
)
```

**Cuándo modificar:**

- Agregar más criterios de búsqueda
- Cambiar algoritmos de ruta
- Mejorar visualización de resultados

---

## 📄 simulacion_tab.py

**Propósito:** Crear la pestaña de simulación de colas y despacho de libros.

**Clases principales:**

### `SimulacionTab`

Controlador que maneja:

- Control de simulación (iniciar, pausar)
- Métricas de despacho
- Estado de colas

**Métodos principales:**

#### `iniciar_simulacion()`

Inicia la simulación de transferencias de libros:

- Colas FIFO por biblioteca
- Despacho según intervalo
- Actualización de métricas

#### `pausar_simulacion()`

Pausa la simulación sin perder estado

**Función principal:**

### `crear_simulacion_tab(notebook, red_bibliotecas)`

```python
def crear_simulacion_tab(notebook, red_bibliotecas):
    """
    Crear y retornar la pestaña de Simulación

    Args:
        notebook (ttk.Notebook): Widget notebook padre
        red_bibliotecas (RedBibliotecas): Instancia del backend

    Returns:
        tuple: (Frame, SimulacionTab) - Tab y controlador
    """
```

**Elementos visuales:**

- Botón Iniciar (▶️)
- Botón Pausar (⏸️)
- Label de métricas
- Sección de colas por biblioteca

**Cómo usarlo:**

```python
from gui.simulacion_tab import crear_simulacion_tab

tab_simulacion, ctrl_simulacion = crear_simulacion_tab(
    notebook, 
    red_bibliotecas
)
```

**Cuándo modificar:**

- Cambiar lógica de colas
- Agregar más métricas
- Mejorar visualización de estado

---

## 📄 visualizacion_tab.py

**Propósito:** Crear la pestaña de visualización gráfica de estructuras de datos.

**Funciones principales:**

### `crear_visualizacion_tab(notebook)`

```python
def crear_visualizacion_tab(notebook):
    """
    Crear y retornar la pestaña de Visualización

    Args:
        notebook (ttk.Notebook): Widget notebook padre

    Returns:
        ttk.Frame: Frame de la pestaña visualización
    """
```

**Elementos visuales:**

- Botones para cada estructura:
  - Ver Árbol AVL
  - Ver Árbol B
  - Ver Árbol B+
  - Ver Tabla Hash
- Canvas para mostrar la visualización

**Cómo usarlo:**

```python
from gui.visualizacion_tab import crear_visualizacion_tab

tab_visualizacion = crear_visualizacion_tab(notebook)
```

**Cuándo modificar:**

- Agregar nuevas estructuras
- Implementar algoritmos de dibujado
- Mejorar interactividad

---

## 📄 pruebas_tab.py

**Propósito:** Crear la pestaña de pruebas de rendimiento y carga masiva de datos.

**Clases principales:**

### `PruebasTab`

Controlador que maneja:

- Comparación de algoritmos de búsqueda
- Comparación de algoritmos de ordenamiento
- Carga de archivos CSV

**Métodos de comparación:**

#### `comparar_busquedas()`

Compara 3 métodos de búsqueda:

- Secuencial (O(n))
- AVL (O(log n))
- Hash (O(1))

Muestra tiempos en segundos

#### `comparar_ordenamientos()`

Compara 5 métodos de ordenamiento:

- Bubble Sort
- Quick Sort
- Merge Sort
- Insertion Sort
- Selection Sort

**Métodos de carga:**

#### `cargar_csv_bibliotecas()`

Carga bibliotecas desde archivo CSV

#### `cargar_csv_conexiones()`

Carga conexiones desde archivo CSV

#### `cargar_csv_libros()`

Carga libros desde archivo CSV

**Función principal:**

### `crear_pruebas_carga_tab(notebook, red_bibliotecas)`

```python
def crear_pruebas_carga_tab(notebook, red_bibliotecas):
    """
    Crear y retornar la pestaña de Pruebas

    Args:
        notebook (ttk.Notebook): Widget notebook padre
        red_bibliotecas (RedBibliotecas): Instancia del backend

    Returns:
        tuple: (Frame, PruebasTab) - Tab y controlador
    """
```

**Secciones:**

**Pruebas de Rendimiento:**

- Comparar 3 Métodos de Búsqueda
- Comparar 5 Tipos de Ordenamiento

**Carga Masiva:**

- Cargar Catálogo de Libros
- Cargar Bibliotecas
- Cargar Conexiones

**Cómo usarlo:**

```python
from gui.pruebas_tab import crear_pruebas_carga_tab

tab_pruebas, ctrl_pruebas = crear_pruebas_carga_tab(
    notebook, 
    red_bibliotecas
)
```

**Cuándo modificar:**

- Agregar más comparaciones
- Cambiar formatos de carga
- Mejorar visualización de resultados

---

## 📊 Diagrama de Relaciones

```
gui/
├── config.py              → Constantes (importadas por todos)
├── styles.py              → Estilos (importado por gui_app.py)
├── __init__.py            → Exportaciones públicas
├── dashboard_tab.py       → Pestaña inicio
├── catalogo_tab.py        → Pestaña CRUD (usa red_bibliotecas)
├── red_tab.py             → Pestaña Grafo (usa red_bibliotecas)
├── busqueda_tab.py        → Pestaña Búsqueda (usa red_bibliotecas)
├── simulacion_tab.py      → Pestaña Simulación (usa red_bibliotecas)
├── visualizacion_tab.py   → Pestaña Visualización
└── pruebas_tab.py         → Pestaña Pruebas (usa red_bibliotecas)
```

---

## 🔄 Flujo de Ejecución

```
main.py
    ↓
gui_app.py (iniciar_gui)
    ↓
    1. RedBibliotecas() - Backend
    2. configurar_estilos() - Estilos globales
    3. Crear Notebook
    4. Agregar pestañas:
       - dashboard_tab
       - catalogo_tab (con ctrl)
       - red_tab (con ctrl)
       - busqueda_tab (con ctrl)
       - simulacion_tab (con ctrl)
       - visualizacion_tab
       - pruebas_tab (con ctrl)
    5. root.mainloop() - Loop principal
```

---

## ✅ Checklist para Desarrollo

Al agregar una nueva característica, asegúrate de:

- [ ] Crear clase Controlador en el archivo tab
- [ ] Implementar métodos de la lógica
- [ ] Crear función `crear_xxxx_tab()`
- [ ] Retornar (tab, controlador) si es necesario
- [ ] Exportar en __init__.py
- [ ] Importar en gui_app.py
- [ ] Agregar tab al notebook
- [ ] Probar funcionalidad completa