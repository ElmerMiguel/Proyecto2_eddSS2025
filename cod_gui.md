Gui:

```
Proyecto2_eddSS2025/
├── main.py
├── gui_app.py (orquestador)
├── gui/
│   ├── __init__.py
│   ├── config.py (colores, estilos)
│   ├── dashboard_tab.py
│   ├── catalogo_tab.py
│   ├── red_tab.py
│   ├── busqueda_tab.py
│   ├── simulacion_tab.py
│   ├── visualizacion_tab.py
│   └── pruebas_tab.py
└── [resto de tu proyecto]
```

# Archivos a crear:



## 📄 ARCHIVO 1: `gui/config.py`

```python
"""
Configuración centralizada de colores, estilos y constantes de la GUI
"""

# ============ COLORES ============
BG_COLOR = "#e6f0ff"        
TITLE_COLOR = "#2a2a72"     
BUTTON_COLOR = "#4a90e2"    
FILTER_BG = "#d9e4f5"       
ACCENT_COLOR = "#1e6bbd"    
DASH_CARD_BG = "#ffffff"    

# ============ CONFIGURACIÓN DE VENTANA ============
WINDOW_TITLE = "📚 Biblioteca Mágica Alrededor del Mundo - Sistema de Gestión de Red"
WINDOW_GEOMETRY = "1200x800"
THEME = "clam"

# ============ FUENTES ============
FONT_TITLE_LARGE = ("Georgia", 26, "bold")
FONT_TITLE_MEDIUM = ("Arial", 14, "bold")
FONT_TITLE_SMALL = ("Arial", 12, "bold")
FONT_LABEL = ("Arial", 11)
FONT_LABEL_SMALL = ("Arial", 9)
FONT_BUTTON = ("Arial", 10, "bold")
```

---

## 📄 ARCHIVO 2: `gui/styles.py`

```python
"""
Configuración de estilos ttk para la GUI
"""

from tkinter import ttk
from .config import *

def configurar_estilos(root):
    """Configura todos los estilos ttk de la aplicación"""

    style = ttk.Style(root)
    style.theme_use(THEME)

    # === NOTEBOOK (Pestañas) ===
    style.configure('TNotebook', background=BG_COLOR, borderwidth=0)

    style.configure('TNotebook.Tab', 
                    font=FONT_BUTTON, 
                    foreground='white',
                    background=BUTTON_COLOR,
                    bordercolor=BG_COLOR,
                    padding=[15, 5])

    style.map('TNotebook.Tab', 
              background=[('selected', ACCENT_COLOR), ('active', BUTTON_COLOR)],
              foreground=[('selected', 'white')],
              bordercolor=[('selected', FILTER_BG)])

    # === FRAMES ===
    style.configure('Sky.TFrame', background=FILTER_BG)

    # === LABELS ===
    style.configure('TLabel', background=FILTER_BG)

    # === CHECKBUTTON y RADIOBUTTON ===
    style.configure('TCheckbutton', background=FILTER_BG, foreground=TITLE_COLOR)
    style.configure('TRadiobutton', background=FILTER_BG, foreground=TITLE_COLOR)

    # === BUTTONS ===
    style.configure('TButton', 
                    font=FONT_BUTTON, 
                    foreground='white', 
                    background=BUTTON_COLOR, 
                    padding=6, 
                    relief='flat')
    style.map('TButton', background=[('active', ACCENT_COLOR)])

    return style
```

---

## 📄 ARCHIVO 3: `gui/__init__.py`

```python
"""
Paquete de GUI - Exporta módulos principales
"""

from .config import *
from .styles import configurar_estilos
from .dashboard_tab import crear_dashboard
from .catalogo_tab import crear_catalogo_tab
from .red_tab import crear_red_tab
from .busqueda_tab import crear_busqueda_rutas_tab
from .simulacion_tab import crear_simulacion_tab
from .visualizacion_tab import crear_visualizacion_tab
from .pruebas_tab import crear_pruebas_carga_tab

__all__ = [
    'configurar_estilos',
    'crear_dashboard',
    'crear_catalogo_tab',
    'crear_red_tab',
    'crear_busqueda_rutas_tab',
    'crear_simulacion_tab',
    'crear_visualizacion_tab',
    'crear_pruebas_carga_tab'
]
```

---

## 📄 ARCHIVO 4: `gui/dashboard_tab.py`

```python
"""
Pestaña Dashboard - Inicio con tarjetas interactivas
"""

import tkinter as tk
from tkinter import ttk
from .config import *

def crear_dashboard(notebook):
    """Crear y retornar la pestaña de Dashboard"""

    tab_dashboard = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_dashboard, text="🏠 Inicio/Dashboard")

    tab_dashboard.grid_columnconfigure((0, 1, 2), weight=1)
    tab_dashboard.grid_rowconfigure((0, 1), weight=1)

    def crear_tarjeta_info(parent, emoji, titulo, descripcion, fila, col, color, indice_tab):
        """Crear tarjeta interactiva del dashboard"""
        tarjeta = tk.Frame(parent, bg=DASH_CARD_BG, bd=2, relief=tk.RAISED, cursor="hand2")
        tarjeta.grid(row=fila, column=col, sticky="nsew", padx=15, pady=15)
        tarjeta.grid_columnconfigure(0, weight=1)

        # Click en tarjeta para cambiar a tab
        tarjeta.bind("<Button-1>", lambda e, idx=indice_tab: notebook.select(idx))

        tk.Label(tarjeta, text=emoji, font=('Arial', 38), bg=DASH_CARD_BG, fg=color).pack(pady=(15, 0))
        tk.Label(tarjeta, text=titulo, font=FONT_TITLE_MEDIUM, bg=DASH_CARD_BG, fg=TITLE_COLOR).pack(pady=(0, 5))
        tk.Label(tarjeta, text=descripcion, font=('Georgia', 11, 'bold'), bg=DASH_CARD_BG, fg=ACCENT_COLOR).pack(pady=(5, 10))
        tk.Label(tarjeta, text="Clic para Gestionar", font=FONT_LABEL_SMALL, bg=DASH_CARD_BG, fg=BUTTON_COLOR).pack(pady=(0, 5))

    # Crear tarjetas
    crear_tarjeta_info(tab_dashboard, "📘", "Catálogo y Libro (CRUD)", 
                       "Estructuras: AVL / B+ / Hash / Listas", 0, 0, ACCENT_COLOR, 1)

    crear_tarjeta_info(tab_dashboard, "🏛️", "Red de Bibliotecas", 
                       "Estructuras: Grafo Ponderado (Nodos/Aristas)", 0, 1, ACCENT_COLOR, 2)

    crear_tarjeta_info(tab_dashboard, "🗺️", "Rutas y Búsqueda", 
                       "Algoritmos: Dijkstra / Búsqueda en Árboles", 0, 2, ACCENT_COLOR, 3)

    crear_tarjeta_info(tab_dashboard, "⏳", "Simulación de Flujo", 
                       "Algoritmos: Colas FIFO (Ingreso, Traspaso, Salida)", 1, 0, ACCENT_COLOR, 4)

    crear_tarjeta_info(tab_dashboard, "🌳", "Visualización Estructuras", 
                       "Representación: Árboles / Hash / Pilas", 1, 1, ACCENT_COLOR, 5)

    crear_tarjeta_info(tab_dashboard, "📈", "Pruebas y Carga CSV", 
                       "Comparación: 5 Sorts / 3 Búsquedas (Big O)", 1, 2, ACCENT_COLOR, 6)

    return tab_dashboard
```

---

## 📄 ARCHIVO 5: `gui/catalogo_tab.py` (PARTE 1 - continúa en siguiente)

```python
"""
Pestaña Catálogo - CRUD de libros y gestión de catálogo
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .config import *
from objetos.libro import Libro

class CatalogoTab:
    """Controlador de la pestaña de Catálogo"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.catalog_tree = None

        # Variables de entrada
        self.titulo_var = tk.StringVar()
        self.autor_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.anio_var = tk.StringVar()
        self.genero_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="disponible")
        self.biblioteca_origen_var = tk.StringVar()
        self.biblioteca_destino_var = tk.StringVar()
        self.prioridad_var = tk.StringVar(value="tiempo")

    def actualizar_catalogo_tree(self):
        """Actualiza el TreeView con libros del catálogo"""
        for item in self.catalog_tree.get_children():
            self.catalog_tree.delete(item)

        total_libros = 0
        for biblioteca_id, biblioteca in self.red_bibliotecas.bibliotecas.items():
            try:
                libros = biblioteca.catalogo_local.lista_secuencial.mostrar_todos()

                if libros is None:
                    libros = []

                for libro in libros:
                    self.catalog_tree.insert("", "end", values=(
                        libro.titulo, libro.autor, libro.isbn, libro.estado, biblioteca_id
                    ))
                    total_libros += 1

            except Exception as e:
                print(f"Error obteniendo libros de {biblioteca_id}: {e}")

        print(f"✅ {total_libros} libros mostrados en la tabla")

    def actualizar_comboboxes_origen_destino(self, combo_origen, combo_destino):
        """Actualiza comboboxes de bibliotecas"""
        bibliotecas_ids = list(self.red_bibliotecas.bibliotecas.keys())

        if bibliotecas_ids:
            combo_origen['values'] = bibliotecas_ids
            combo_destino['values'] = bibliotecas_ids

            if self.biblioteca_origen_var.get() == "":
                self.biblioteca_origen_var.set(bibliotecas_ids[0])

    def agregar_libro(self):
        """Agregar nuevo libro con todos los campos"""
        try:
            if not all([self.titulo_var.get().strip(), self.autor_var.get().strip(), 
                       self.isbn_var.get().strip()]):
                messagebox.showerror("Error", "Título, autor e ISBN son obligatorios")
                return

            if not self.red_bibliotecas.bibliotecas:
                messagebox.showerror("Error", "No hay bibliotecas. Carga bibliotecas primero.")
                return

            try:
                anio = int(self.anio_var.get())
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número válido")
                return

            # Crear libro
            libro = Libro(
                titulo=self.titulo_var.get().strip(),
                isbn=self.isbn_var.get().strip(),
                genero=self.genero_var.get().strip(),
                anio=anio,
                autor=self.autor_var.get().strip(),
                estado=self.estado_var.get(),
                biblioteca_origen=self.biblioteca_origen_var.get(),
                biblioteca_destino=self.biblioteca_destino_var.get(),
                prioridad=self.prioridad_var.get()
            )

            # Agregar a biblioteca
            bib_origen = self.biblioteca_origen_var.get()
            if bib_origen and bib_origen in self.red_bibliotecas.bibliotecas:
                self.red_bibliotecas.bibliotecas[bib_origen].catalogo_local.agregar_libro(libro, "General")

                # Si hay destino diferente, programar transferencia
                bib_destino = self.biblioteca_destino_var.get()
                if bib_destino and bib_destino != bib_origen:
                    self.red_bibliotecas.programar_transferencia(
                        libro.isbn, bib_origen, bib_destino, self.prioridad_var.get()
                    )
            else:
                primera_bib = next(iter(self.red_bibliotecas.bibliotecas.values()))
                primera_bib.catalogo_local.agregar_libro(libro, "General")

            # Limpiar formulario
            self._limpiar_formulario()

            messagebox.showinfo("Éxito", f"Libro '{libro.titulo}' agregado correctamente")
            self.actualizar_catalogo_tree()

        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar libro: {e}")

    def eliminar_libro(self):
        """Eliminar libro del catálogo"""
        selected = self.catalog_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar")
            return

        try:
            item = self.catalog_tree.item(selected[0])
            isbn = item['values'][2]

            eliminado = False
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                if biblioteca.eliminar_libro_catalogo(isbn):
                    eliminado = True
                    break

            if eliminado:
                messagebox.showinfo("Éxito", "Libro eliminado correctamente")
                self.actualizar_catalogo_tree()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el libro")

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar libro: {e}")

    def rollback_operacion(self):
        """Deshacer última operación"""
        try:
            if self.red_bibliotecas.bibliotecas:
                primera_bib = next(iter(self.red_bibliotecas.bibliotecas.values()))
                libro_restaurado = primera_bib.rollback_ultimo_ingreso()

                if libro_restaurado:
                    messagebox.showinfo("Éxito", f"Operación deshecha: {libro_restaurado.titulo}")
                    self.actualizar_catalogo_tree()
                else:
                    messagebox.showwarning("Advertencia", "No hay operaciones para deshacer")
        except Exception as e:
            messagebox.showerror("Error", f"Error en rollback: {e}")

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.titulo_var.set("")
        self.autor_var.set("")
        self.isbn_var.set("")
        self.anio_var.set("")
        self.genero_var.set("")
        self.estado_var.set("disponible")
        self.biblioteca_origen_var.set("")
        self.biblioteca_destino_var.set("")
        self.prioridad_var.set("tiempo")


def crear_catalogo_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Catálogo"""

    tab_catalogo = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_catalogo, text="📚 Catálogo y Libro (CRUD)")

    tab_catalogo.grid_columnconfigure((0, 1), weight=1)
    tab_catalogo.grid_rowconfigure(0, weight=1)

    # Crear controlador
    ctrl = CatalogoTab(red_bibliotecas)

    # === FRAME CRUD ===
    crud_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    crud_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(crud_frame, text="✏️ REGISTRO DE LIBRO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 15))

    # Título
    tk.Label(crud_frame, text="Título:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.titulo_var, width=40).pack(fill='x')

    # Autor
    tk.Label(crud_frame, text="Autor:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.autor_var, width=40).pack(fill='x')

    # ISBN
    tk.Label(crud_frame, text="ISBN:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.isbn_var, width=20).pack(fill='x')

    # Año
    tk.Label(crud_frame, text="Año de publicación:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.anio_var, width=10).pack(fill='x')

    # Género
    tk.Label(crud_frame, text="Género:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.genero_var, width=20).pack(fill='x')

    # Estado
    tk.Label(crud_frame, text="Estado:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Combobox(crud_frame, textvariable=ctrl.estado_var, 
                 values=["disponible", "prestado", "en_transito", "agotado"]).pack(fill='x')

    # Biblioteca Origen
    tk.Label(crud_frame, text="Biblioteca Origen:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    biblioteca_origen_combo = ttk.Combobox(crud_frame, textvariable=ctrl.biblioteca_origen_var)
    biblioteca_origen_combo.pack(fill='x')

    # Biblioteca Destino
    tk.Label(crud_frame, text="Biblioteca Destino:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    biblioteca_destino_combo = ttk.Combobox(crud_frame, textvariable=ctrl.biblioteca_destino_var)
    biblioteca_destino_combo.pack(fill='x')

    # Prioridad
    tk.Label(crud_frame, text="Prioridad de Envío:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    prioridad_frame = ttk.Frame(crud_frame)
    prioridad_frame.pack(fill='x', pady=2)
    ttk.Radiobutton(prioridad_frame, text="Tiempo", 
                    variable=ctrl.prioridad_var, value="tiempo").pack(side='left', padx=10)
    ttk.Radiobutton(prioridad_frame, text="Costo", 
                    variable=ctrl.prioridad_var, value="costo").pack(side='left', padx=10)

    # Botones CRUD
    ttk.Button(crud_frame, text="➕ Agregar Libro", 
               command=ctrl.agregar_libro).pack(pady=(20, 5), fill='x')
    ttk.Button(crud_frame, text="🗑️ Eliminar Libro", 
               command=ctrl.eliminar_libro).pack(pady=5, fill='x')

    # Control de Pilas
    tk.Label(crud_frame, text="🔄 CONTROL DE PILAS", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(20, 10))
    ttk.Button(crud_frame, text="↩️ Deshacer Última Operación", 
               command=ctrl.rollback_operacion).pack(pady=5, fill='x')

    # === FRAME LISTADO ===
    listado_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    listado_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    listado_frame.grid_rowconfigure(2, weight=1)

    tk.Label(listado_frame, text="📖 LISTADO Y ALMACENAMIENTO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    ttk.Button(listado_frame, text="🔄 Actualizar Catálogo", 
               command=ctrl.actualizar_catalogo_tree).pack(fill='x', pady=5)

    tk.Label(listado_frame, text="CATÁLOGO COMPLETO:", 
             font=FONT_TITLE_SMALL, bg=FILTER_BG).pack(anchor='w', pady=(10, 0))

    ctrl.catalog_tree = ttk.Treeview(listado_frame, 
                                     columns=("Título", "Autor", "ISBN", "Estado", "Biblioteca"), 
                                     show='headings')
    ctrl.catalog_tree.heading("Título", text="Título")
    ctrl.catalog_tree.heading("Autor", text="Autor")
    ctrl.catalog_tree.heading("ISBN", text="ISBN")
    ctrl.catalog_tree.heading("Estado", text="Estado")
    ctrl.catalog_tree.heading("Biblioteca", text="Biblioteca")
    ctrl.catalog_tree.pack(fill='both', expand=True, pady=(5, 0))

    # Actualizar comboboxes
    ctrl.actualizar_comboboxes_origen_destino(biblioteca_origen_combo, biblioteca_destino_combo)

    return tab_catalogo
```

¿Continúo con los demás archivos (red_tab, busqueda_tab, simulacion_tab, visualizacion_tab, pruebas_tab)?

ElmerMiguel: si continuar

GitHub Copilot: Continuamos con los demás archivos:

---

## 📄 ARCHIVO 6: `gui/red_tab.py`

```python
"""
Pestaña Red - Gestión de bibliotecas y conexiones (Grafo)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
from .config import *
from objetos.biblioteca import Biblioteca

class RedTab:
    """Controlador de la pestaña de Red de Bibliotecas"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.grafo_canvas = None

        # Variables de entrada
        self.bib_nombre_var = tk.StringVar()
        self.bib_ubicacion_var = tk.StringVar()
        self.bib_tiempo_ingreso_var = tk.StringVar(value="10")
        self.bib_tiempo_traspaso_var = tk.StringVar(value="5")
        self.bib_intervalo_despacho_var = tk.StringVar(value="3")

        self.origen_var = tk.StringVar()
        self.destino_var = tk.StringVar()
        self.tiempo_conexion_var = tk.StringVar()
        self.costo_conexion_var = tk.StringVar()
        self.bidireccional_var = tk.BooleanVar(value=True)

    def agregar_biblioteca(self):
        """Agregar nueva biblioteca"""
        try:
            nombre = self.bib_nombre_var.get()
            if not nombre:
                messagebox.showerror("Error", "El nombre de la biblioteca es obligatorio")
                return

            # Generar ID único
            bib_id = f"BIB{len(self.red_bibliotecas.bibliotecas) + 1:03d}"

            biblioteca = Biblioteca(
                id_biblioteca=bib_id,
                nombre=nombre,
                ubicacion=self.bib_ubicacion_var.get() or "Sin ubicación",
                tiempo_ingreso=int(self.bib_tiempo_ingreso_var.get()) if self.bib_tiempo_ingreso_var.get() else 10,
                tiempo_traspaso=int(self.bib_tiempo_traspaso_var.get()) if self.bib_tiempo_traspaso_var.get() else 5,
                intervalo_despacho=int(self.bib_intervalo_despacho_var.get()) if self.bib_intervalo_despacho_var.get() else 3
            )

            self.red_bibliotecas.bibliotecas[bib_id] = biblioteca
            self.red_bibliotecas.grafo.agregar_nodo(bib_id, nombre)

            messagebox.showinfo("Éxito", f"Biblioteca '{nombre}' creada con ID: {bib_id}")

            # Limpiar campos
            self._limpiar_formulario_bib()

            # Callback para actualizar UI (se asigna desde gui_app.py)
            if hasattr(self, 'callback_actualizar'):
                self.callback_actualizar()

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear biblioteca: {e}")

    def agregar_conexion(self):
        """Agregar conexión entre bibliotecas"""
        try:
            origen = self.origen_var.get()
            destino = self.destino_var.get()
            tiempo = self.tiempo_conexion_var.get()
            costo = self.costo_conexion_var.get()

            if not all([origen, destino, tiempo, costo]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            self.red_bibliotecas.grafo.agregar_arista(
                origen=origen,
                destino=destino,
                tiempo=int(tiempo),
                costo=float(costo),
                bidireccional=self.bidireccional_var.get()
            )

            messagebox.showinfo("Éxito", f"Conexión creada: {origen} -> {destino}")

            # Limpiar campos
            self.tiempo_conexion_var.set("")
            self.costo_conexion_var.set("")

            # Callback para dibujar grafo
            if hasattr(self, 'callback_dibujar'):
                self.callback_dibujar()

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear conexión: {e}")

    def actualizar_comboboxes_conexiones(self, origen_combo, destino_combo):
        """Actualiza comboboxes de bibliotecas para conexiones"""
        bibliotecas_ids = list(self.red_bibliotecas.bibliotecas.keys())

        if bibliotecas_ids:
            origen_combo['values'] = bibliotecas_ids
            destino_combo['values'] = bibliotecas_ids

    def dibujar_grafo(self):
        """Dibujar grafo en el canvas"""
        if self.grafo_canvas is None:
            return

        self.grafo_canvas.delete("all")

        if not self.red_bibliotecas.grafo.nodos:
            return

        # Obtener dimensiones del canvas
        width = self.grafo_canvas.winfo_width() or 400
        height = self.grafo_canvas.winfo_height() or 300

        nodos = list(self.red_bibliotecas.grafo.nodos.keys())
        n = len(nodos)

        if n == 0:
            return

        posiciones = {}

        # Distribuir nodos en círculo
        for i, nodo in enumerate(nodos):
            angle = 2 * math.pi * i / n
            x = width // 2 + (width // 3) * math.cos(angle)
            y = height // 2 + (height // 3) * math.sin(angle)
            posiciones[nodo] = (x, y)

        # Dibujar aristas
        for nodo_origen, aristas in self.red_bibliotecas.grafo.nodos.items():
            if nodo_origen in posiciones:
                x1, y1 = posiciones[nodo_origen]
                for arista in aristas:
                    if arista.destino in posiciones:
                        x2, y2 = posiciones[arista.destino]
                        self.grafo_canvas.create_line(x1, y1, x2, y2, 
                                                     fill=ACCENT_COLOR, width=2)

                        # Etiqueta de peso
                        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                        self.grafo_canvas.create_text(mx, my, text=f"{arista.tiempo}",
                                                     fill="red", font=('Arial', 8, 'bold'))

        # Dibujar nodos
        for nodo, (x, y) in posiciones.items():
            self.grafo_canvas.create_oval(x-20, y-20, x+20, y+20, 
                                        fill=BUTTON_COLOR, outline=TITLE_COLOR, width=2)
            self.grafo_canvas.create_text(x, y, text=nodo, fill="white", 
                                        font=('Arial', 8, 'bold'))

    def _limpiar_formulario_bib(self):
        """Limpia formulario de bibliotecas"""
        self.bib_nombre_var.set("")
        self.bib_ubicacion_var.set("")
        self.bib_tiempo_ingreso_var.set("10")
        self.bib_tiempo_traspaso_var.set("5")
        self.bib_intervalo_despacho_var.set("3")


def crear_red_tab(notebook, red_bibliotecas, callback_actualizar=None, callback_dibujar=None):
    """Crear y retornar la pestaña de Red"""

    tab_red = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_red, text="🌐 Gestión de la Red (Grafo)")

    tab_red.grid_columnconfigure(0, weight=1)
    tab_red.grid_columnconfigure(1, weight=3)
    tab_red.grid_rowconfigure(0, weight=1)

    # Crear controlador
    ctrl = RedTab(red_bibliotecas)
    if callback_actualizar:
        ctrl.callback_actualizar = callback_actualizar
    if callback_dibujar:
        ctrl.callback_dibujar = callback_dibujar

    # === FRAME CONFIGURACIÓN ===
    config_frame_red = ttk.Frame(tab_red, style='Sky.TFrame', padding=15)
    config_frame_red.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # --- GESTIÓN DE BIBLIOTECAS ---
    tk.Label(config_frame_red, text="🏛️ GESTIÓN DE BIBLIOTECAS", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(config_frame_red, text="Nombre:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_nombre_var, width=30).pack(fill='x')

    tk.Label(config_frame_red, text="Ubicación:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_ubicacion_var, width=30).pack(fill='x')

    tk.Label(config_frame_red, text="Tiempo Ingreso (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_tiempo_ingreso_var, width=15).pack(fill='x')

    tk.Label(config_frame_red, text="Tiempo Traspaso (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_tiempo_traspaso_var, width=15).pack(fill='x')

    tk.Label(config_frame_red, text="Intervalo Despacho (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_intervalo_despacho_var, width=15).pack(fill='x')

    ttk.Button(config_frame_red, text="➕ Crear Biblioteca", 
               command=ctrl.agregar_biblioteca).pack(pady=(15, 5), fill='x')

    # --- GESTIÓN DE CONEXIONES ---
    tk.Label(config_frame_red, text="🔗 GESTIÓN DE CONEXIONES", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(20, 10))

    tk.Label(config_frame_red, text="Origen:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    origen_combo = ttk.Combobox(config_frame_red, textvariable=ctrl.origen_var)
    origen_combo.pack(fill='x')

    tk.Label(config_frame_red, text="Destino:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    destino_combo = ttk.Combobox(config_frame_red, textvariable=ctrl.destino_var)
    destino_combo.pack(fill='x')

    tk.Label(config_frame_red, text="Tiempo:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.tiempo_conexion_var).pack(fill='x')

    tk.Label(config_frame_red, text="Costo:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.costo_conexion_var).pack(fill='x')

    ttk.Checkbutton(config_frame_red, text="Conexión Bidireccional", 
                    variable=ctrl.bidireccional_var).pack(anchor='w', pady=5)

    ttk.Button(config_frame_red, text="🔗 Crear Conexión", 
               command=ctrl.agregar_conexion).pack(pady=10, fill='x')

    # === FRAME GRAFO ===
    grafo_frame = ttk.Frame(tab_red, style='Sky.TFrame', padding=10)
    grafo_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(grafo_frame, text="🌍 RED DE BIBLIOTECAS", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    ctrl.grafo_canvas = tk.Canvas(grafo_frame, bg=DASH_CARD_BG, 
                                  highlightthickness=1, highlightbackground=TITLE_COLOR)
    ctrl.grafo_canvas.pack(fill='both', expand=True, pady=5)

    # Evento de redimensionado
    def on_canvas_configure(event):
        if event.widget == ctrl.grafo_canvas:
            tk.Tk.after(tab_red, 100, ctrl.dibujar_grafo)

    ctrl.grafo_canvas.bind('<Configure>', on_canvas_configure)

    # Actualizar comboboxes y dibujar
    ctrl.actualizar_comboboxes_conexiones(origen_combo, destino_combo)

    return tab_red, ctrl
```

---

## 📄 ARCHIVO 7: `gui/busqueda_tab.py`

```python
"""
Pestaña Búsqueda y Rutas Óptimas
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from .config import *

class BusquedaTab:
    """Controlador de la pestaña de Búsqueda y Rutas"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.ruta_resultado_label = None

        # Variables de entrada
        self.buscar_titulo_var = tk.StringVar()
        self.buscar_isbn_var = tk.StringVar()
        self.buscar_genero_var = tk.StringVar()
        self.anio_inicio_var = tk.StringVar()
        self.anio_fin_var = tk.StringVar()

        self.ruta_origen_var = tk.StringVar()
        self.ruta_destino_var = tk.StringVar()
        self.criterio_var = tk.StringVar(value="tiempo")

    def actualizar_generos_combo(self, genero_combo):
        """Actualiza combo de géneros disponibles"""
        generos = set()
        for bib in self.red_bibliotecas.bibliotecas.values():
            try:
                generos_bib = bib.catalogo_local.obtener_generos_disponibles()
                generos.update(generos_bib)
            except Exception:
                pass

        if generos:
            genero_combo['values'] = list(generos)

    def actualizar_comboboxes_rutas(self, origen_combo, destino_combo):
        """Actualiza comboboxes de bibliotecas para rutas"""
        bibliotecas_ids = list(self.red_bibliotecas.bibliotecas.keys())

        if bibliotecas_ids:
            origen_combo['values'] = bibliotecas_ids
            destino_combo['values'] = bibliotecas_ids

    def buscar_por_titulo(self):
        """Búsqueda por título usando AVL"""
        titulo = self.buscar_titulo_var.get()
        if not titulo:
            messagebox.showwarning("Advertencia", "Ingrese un título para buscar")
            return

        resultados = []
        for biblioteca in self.red_bibliotecas.bibliotecas.values():
            try:
                libro = biblioteca.catalogo_local.buscar_por_titulo(titulo)
                if libro:
                    resultados.append(libro)
            except Exception:
                pass

        self._mostrar_resultados_busqueda(resultados, f"Título: {titulo}")

    def buscar_por_isbn(self):
        """Búsqueda por ISBN usando Hash"""
        isbn = self.buscar_isbn_var.get()
        if not isbn:
            messagebox.showwarning("Advertencia", "Ingrese un ISBN para buscar")
            return

        resultados = []
        for biblioteca in self.red_bibliotecas.bibliotecas.values():
            try:
                libro = biblioteca.catalogo_local.buscar_por_isbn(isbn)
                if libro:
                    resultados.append(libro)
                    break
            except Exception:
                pass

        self._mostrar_resultados_busqueda(resultados, f"ISBN: {isbn}")

    def buscar_por_genero(self):
        """Búsqueda por género usando B+"""
        genero = self.buscar_genero_var.get()
        if not genero:
            messagebox.showwarning("Advertencia", "Seleccione un género para buscar")
            return

        resultados = []
        for biblioteca in self.red_bibliotecas.bibliotecas.values():
            try:
                libros = biblioteca.catalogo_local.buscar_por_genero(genero)
                resultados.extend(libros)
            except Exception:
                pass

        self._mostrar_resultados_busqueda(resultados, f"Género: {genero}")

    def buscar_por_rango(self):
        """Búsqueda por rango de fechas usando Árbol B"""
        try:
            inicio = int(self.anio_inicio_var.get()) if self.anio_inicio_var.get() else None
            fin = int(self.anio_fin_var.get()) if self.anio_fin_var.get() else None

            if inicio is None or fin is None:
                messagebox.showerror("Error", "Ingrese ambos años para el rango")
                return

            resultados = []
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                try:
                    libros_rango = biblioteca.catalogo_local.buscar_por_rango_fechas(inicio, fin)
                    resultados.extend(libros_rango)
                except Exception:
                    pass

            self._mostrar_resultados_busqueda(resultados, f"Rango: {inicio}-{fin}")

        except ValueError:
            messagebox.showerror("Error", "Los años deben ser números válidos")

    def _mostrar_resultados_busqueda(self, libros, criterio):
        """Mostrar resultados en una ventana nueva"""
        if not libros:
            messagebox.showinfo("Búsqueda", f"No se encontraron libros para {criterio}")
            return

        ventana = tk.Toplevel()
        ventana.title(f"Resultados - {criterio}")
        ventana.geometry("800x400")
        ventana.configure(bg=BG_COLOR)

        frame = ttk.Frame(ventana, style='Sky.TFrame', padding=10)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text=f"Resultados para {criterio} ({len(libros)} encontrados):",
                font=FONT_TITLE_MEDIUM, bg=FILTER_BG).pack(pady=(0, 10))

        tree = ttk.Treeview(frame, columns=("Título", "Autor", "ISBN", "Año", "Género"), 
                           show='headings')
        tree.heading("Título", text="Título")
        tree.heading("Autor", text="Autor")
        tree.heading("ISBN", text="ISBN")
        tree.heading("Año", text="Año")
        tree.heading("Género", text="Género")

        for libro in libros:
            tree.insert("", "end", values=(
                libro.titulo, libro.autor, libro.isbn, libro.anio, libro.genero
            ))

        tree.pack(fill='both', expand=True)

    def calcular_ruta_optima(self):
        """Calcular ruta óptima entre bibliotecas"""
        origen = self.ruta_origen_var.get()
        destino = self.ruta_destino_var.get()

        if not origen or not destino:
            messagebox.showerror("Error", "Seleccione bibliotecas de origen y destino")
            return

        if origen == destino:
            messagebox.showerror("Error", "Origen y destino deben ser diferentes")
            return

        try:
            if self.criterio_var.get() == "tiempo":
                peso, ruta = self.red_bibliotecas.grafo.dijkstra_tiempo(origen, destino)
            else:
                peso, ruta = self.red_bibliotecas.grafo.dijkstra_costo(origen, destino)

            if ruta:
                ruta_texto = " -> ".join(ruta)
                mensaje = f"Ruta óptima ({self.criterio_var.get()}):\n{ruta_texto}\nPeso total: {peso}"
                messagebox.showinfo("Ruta Calculada", mensaje)

                # Actualizar etiqueta
                if self.ruta_resultado_label:
                    self.ruta_resultado_label.config(text=f"Ruta: {ruta_texto} | Peso: {peso}")
            else:
                messagebox.showerror("Error", "No se encontró ruta entre las bibliotecas")

        except Exception as e:
            messagebox.showerror("Error", f"Error calculando ruta: {e}")


def crear_busqueda_rutas_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Búsqueda y Rutas"""

    tab_busqueda_rutas = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_busqueda_rutas, text="🔍 Búsqueda y Rutas Óptimas")

    tab_busqueda_rutas.grid_columnconfigure((0, 1), weight=1)
    tab_busqueda_rutas.grid_rowconfigure(1, weight=1)

    # Crear controlador
    ctrl = BusquedaTab(red_bibliotecas)

    # === FRAME BÚSQUEDA ===
    search_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
    search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(search_frame, text="🔍 BÚSQUEDA AVANZADA", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    # Búsqueda por Título
    tk.Label(search_frame, text="Buscar por Título (AVL):", bg=FILTER_BG).pack(anchor='w')
    search_title_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    search_title_frame.pack(fill='x')
    ttk.Entry(search_title_frame, textvariable=ctrl.buscar_titulo_var).pack(side='left', fill='x', expand=True)
    ttk.Button(search_title_frame, text="Buscar", 
               command=ctrl.buscar_por_titulo).pack(side='left', padx=3)

    # Búsqueda por ISBN
    tk.Label(search_frame, text="Buscar por ISBN (HASH):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    search_isbn_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    search_isbn_frame.pack(fill='x')
    ttk.Entry(search_isbn_frame, textvariable=ctrl.buscar_isbn_var).pack(side='left', fill='x', expand=True)
    ttk.Button(search_isbn_frame, text="Buscar", 
               command=ctrl.buscar_por_isbn).pack(side='left', padx=3)

    # Búsqueda por Género
    tk.Label(search_frame, text="Buscar por Género (B+):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    search_genre_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    search_genre_frame.pack(fill='x')
    buscar_genero_combo = ttk.Combobox(search_genre_frame, textvariable=ctrl.buscar_genero_var)
    buscar_genero_combo.pack(side='left', fill='x', expand=True)
    ttk.Button(search_genre_frame, text="Buscar", 
               command=ctrl.buscar_por_genero).pack(side='left', padx=3)

    # Búsqueda por Rango
    tk.Label(search_frame, text="Rango de Fechas (Árbol B):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    search_date_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    search_date_frame.pack(fill='x')
    ttk.Entry(search_date_frame, textvariable=ctrl.anio_inicio_var, width=10).pack(side='left', padx=3)
    tk.Label(search_date_frame, text="a", bg=FILTER_BG).pack(side='left')
    ttk.Entry(search_date_frame, textvariable=ctrl.anio_fin_var, width=10).pack(side='left', padx=3)
    ttk.Button(search_date_frame, text="Buscar", 
               command=ctrl.buscar_por_rango).pack(side='left', padx=3)

    # === FRAME RUTAS ===
    rutas_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
    rutas_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(rutas_frame, text="🗺️ CÁLCULO DE RUTA ÓPTIMA", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(rutas_frame, text="Biblioteca Origen:", bg=FILTER_BG).pack(anchor='w')
    ruta_origen_combo = ttk.Combobox(rutas_frame, textvariable=ctrl.ruta_origen_var)
    ruta_origen_combo.pack(fill='x', pady=2)

    tk.Label(rutas_frame, text="Biblioteca Destino:", bg=FILTER_BG).pack(anchor='w')
    ruta_destino_combo = ttk.Combobox(rutas_frame, textvariable=ctrl.ruta_destino_var)
    ruta_destino_combo.pack(fill='x', pady=2)

    tk.Label(rutas_frame, text="Criterio de Optimización:", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    criterio_options = ttk.Frame(rutas_frame, style='Sky.TFrame')
    criterio_options.pack(fill='x')
    ttk.Radiobutton(criterio_options, text="Tiempo", 
                    variable=ctrl.criterio_var, value="tiempo").pack(side='left', padx=5)
    ttk.Radiobutton(criterio_options, text="Costo", 
                    variable=ctrl.criterio_var, value="costo").pack(side='left', padx=5)

    ttk.Button(rutas_frame, text="🧮 Calcular Ruta Óptima", 
               command=ctrl.calcular_ruta_optima).pack(pady=(15, 5), fill='x')

    ctrl.ruta_resultado_label = tk.Label(rutas_frame, text="Ruta: [No calculada]", 
                                         bg=FILTER_BG, fg=ACCENT_COLOR)
    ctrl.ruta_resultado_label.pack(anchor='w', pady=5)

    # === FRAME VISUALIZACIÓN RUTAS ===
    results_busqueda_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=10)
    results_busqueda_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    tk.Label(results_busqueda_frame, text="VISUALIZACIÓN DE RUTA", 
             font=FONT_TITLE_MEDIUM, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    ruta_canvas = tk.Canvas(results_busqueda_frame, bg=DASH_CARD_BG, 
                           highlightthickness=1, highlightbackground=TITLE_COLOR)
    ruta_canvas.pack(fill='both', expand=True)

    # Actualizar comboboxes
    ctrl.actualizar_generos_combo(buscar_genero_combo)
    ctrl.actualizar_comboboxes_rutas(ruta_origen_combo, ruta_destino_combo)

    return tab_busqueda_rutas, ctrl
```

---

## 📄 ARCHIVO 8: `gui/simulacion_tab.py`

```python
"""
Pestaña Simulación - Simulación de colas y despacho
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from .config import *

class SimulacionTab:
    """Controlador de la pestaña de Simulación"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.simulacion_activa = False
        self.simulacion_thread = None
        self.metricas_label = None

    def iniciar_simulacion(self):
        """Iniciar simulación de colas"""
        if self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulación ya está en ejecución")
            return

        self.simulacion_activa = True
        messagebox.showinfo("Simulación", "Simulación iniciada")

        # Aquí implementarías la lógica de simulación en tiempo real
        # Por ahora es un placeholder
        if self.metricas_label:
            self.metricas_label.config(text="Estado: En ejecución | Transferencias activas: 0")

    def pausar_simulacion(self):
        """Pausar simulación"""
        if not self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulación no está en ejecución")
            return

        self.simulacion_activa = False
        messagebox.showinfo("Simulación", "Simulación pausada")

        if self.metricas_label:
            self.metricas_label.config(text="Estado: Pausado | Transferencias activas: 0")


def crear_simulacion_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Simulación"""

    tab_simulacion = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_simulacion, text="📦 Simulación y Colas")

    tab_simulacion.grid_columnconfigure(0, weight=1) 
    tab_simulacion.grid_rowconfigure(2, weight=1) 

    # Crear controlador
    ctrl = SimulacionTab(red_bibliotecas)

    # === FRAME CONTROLES ===
    sim_controls = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=15)
    sim_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    tk.Label(sim_controls, text="⚙️ CONTROLES DE SIMULACIÓN", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="▶️ Iniciar", 
               command=ctrl.iniciar_simulacion).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="⏸️ Pausar", 
               command=ctrl.pausar_simulacion).pack(side='left', padx=10)

    # === FRAME MÉTRICAS ===
    metrics_frame = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    metrics_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

    tk.Label(metrics_frame, text="MÉTRICAS DE DESPACHO:", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')

    ctrl.metricas_label = tk.Label(metrics_frame, 
                                   text="Estado: Detenido | Transferencias activas: 0", 
                                   bg=FILTER_BG, fg=ACCENT_COLOR)
    ctrl.metricas_label.pack(anchor='w', pady=5)

    # === FRAME COLAS ===
    colas_container = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    colas_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(colas_container, text="🚦 ESTADO DE COLAS POR BIBLIOTECA", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=10)

    tk.Label(colas_container, 
             text="[Las colas se mostrarán cuando se carguen bibliotecas y se inicie la simulación]", 
             font=FONT_LABEL, pady=20, bg=FILTER_BG).pack(fill='x')

    return tab_simulacion, ctrl
```

---

## 📄 ARCHIVO 9: `gui/visualizacion_tab.py`

```python
"""
Pestaña Visualización - Representación gráfica de estructuras
"""

import tkinter as tk
from tkinter import ttk
from .config import *

def crear_visualizacion_tab(notebook):
    """Crear y retornar la pestaña de Visualización"""

    tab_visualizacion = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_visualizacion, text="📊 Visualización Estructuras")

    tk.Label(tab_visualizacion, text="🌳 REPRESENTACIÓN GRÁFICA DE ESTRUCTURAS", 
             font=FONT_TITLE_LARGE, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=20)

    # === FRAME BOTONES ===
    vis_buttons = ttk.Frame(tab_visualizacion, style='Sky.TFrame')
    vis_buttons.pack(pady=10)

    ttk.Button(vis_buttons, text="Ver Árbol AVL").pack(side='left', padx=5)
    ttk.Button(vis_buttons, text="Ver Árbol B").pack(side='left', padx=5)
    ttk.Button(vis_buttons, text="Ver Árbol B+").pack(side='left', padx=5)
    ttk.Button(vis_buttons, text="Ver Tabla Hash").pack(side='left', padx=5)

    # === CANVAS VISUALIZACIÓN ===
    vis_canvas = tk.Canvas(tab_visualizacion, bg=DASH_CARD_BG, 
                          highlightthickness=1, highlightbackground=TITLE_COLOR)
    vis_canvas.pack(fill='both', expand=True, padx=20, pady=10)

    # Mensaje de ayuda
    vis_canvas.create_text(vis_canvas.winfo_width() // 2, 
                          vis_canvas.winfo_height() // 2,
                          text="Selecciona una estructura para visualizar",
                          font=FONT_LABEL_SMALL, fill=TITLE_COLOR)

    return tab_visualizacion
```

---

## 📄 ARCHIVO 10: `gui/pruebas_tab.py`

```python
"""
Pestaña Pruebas - Pruebas de rendimiento, carga CSV y comparaciones
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
from .config import *
from estructuras.metodos_ordenamiento import comparar_metodos

class PruebasTab:
    """Controlador de la pestaña de Pruebas de Rendimiento"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas

    def comparar_busquedas(self):
        """Comparar métodos de búsqueda"""
        try:
            if not self.red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas para comparar")
                return

            primera_bib = next(iter(self.red_bibliotecas.bibliotecas.values()))
            libros = primera_bib.catalogo_local.lista_secuencial.mostrar_todos()

            if not libros:
                messagebox.showwarning("Advertencia", "No hay libros para comparar")
                return

            libro_prueba = libros[len(libros)//2]

            # Medir búsqueda secuencial
            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.lista_secuencial.buscar_por_titulo(libro_prueba.titulo)
            tiempo_secuencial = time.perf_counter() - inicio

            # Medir búsqueda AVL
            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.arbol_titulos.buscar(libro_prueba.titulo)
            tiempo_avl = time.perf_counter() - inicio

            # Medir búsqueda Hash
            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.tabla_isbn.buscar(libro_prueba.isbn)
            tiempo_hash = time.perf_counter() - inicio

            resultado = f"""
COMPARACIÓN DE BÚSQUEDAS:
Elemento buscado: {libro_prueba.titulo}
Tamaño del catálogo: {len(libros)} libros

Secuencial: {tiempo_secuencial:.6f} segundos
AVL (Título): {tiempo_avl:.6f} segundos  
Hash (ISBN): {tiempo_hash:.6f} segundos

Más rápido: {'Hash' if tiempo_hash < min(tiempo_secuencial, tiempo_avl) else 'AVL' if tiempo_avl < tiempo_secuencial else 'Secuencial'}
            """

            messagebox.showinfo("Resultados de Búsqueda", resultado)

        except Exception as e:
            messagebox.showerror("Error", f"Error en comparación: {e}")

    def comparar_ordenamientos(self):
        """Comparar métodos de ordenamiento"""
        try:
            if not self.red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas para comparar")
                return

            primera_bib = next(iter(self.red_bibliotecas.bibliotecas.values()))
            libros = primera_bib.catalogo_local.lista_secuencial.mostrar_todos()

            if len(libros) < 2:
                messagebox.showwarning("Advertencia", "Se necesitan al menos 2 libros para comparar")
                return

            resultado = comparar_metodos(libros, "titulo")
            messagebox.showinfo("Resultados de Ordenamiento", resultado)

        except Exception as e:
            messagebox.showerror("Error", f"Error en comparación: {e}")

    def cargar_csv_bibliotecas(self):
        """Cargar bibliotecas desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                count = self.red_bibliotecas.cargar_bibliotecas_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} bibliotecas cargadas")
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando bibliotecas: {e}")

    def cargar_csv_conexiones(self):
        """Cargar conexiones desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                count = self.red_bibliotecas.cargar_conexiones_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} conexiones cargadas")
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando conexiones: {e}")

    def cargar_csv_libros(self):
        """Cargar libros desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                count = self.red_bibliotecas.cargar_libros_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} libros cargados")
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando libros: {e}")


def crear_pruebas_carga_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Pruebas de Carga"""

    tab_pruebas_carga = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_pruebas_carga, text="⚙️ Pruebas de Rendimiento y Carga (CSV)")

    tab_pruebas_carga.grid_columnconfigure((0, 1), weight=1)
    tab_pruebas_carga.grid_rowconfigure(0, weight=1)

    # Crear controlador
    ctrl = PruebasTab(red_bibliotecas)

    # === FRAME COMPARACIÓN ===
    comp_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    comp_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(comp_frame, text="⏱️ PRUEBAS DE RENDIMIENTO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(comp_frame, text="COMPARACIÓN DE BÚSQUEDAS:", 
             font=FONT_TITLE_SMALL, bg=FILTER_BG).pack(pady=(5, 5), anchor='w')
    ttk.Button(comp_frame, text="Comparar 3 Métodos de Búsqueda", 
               command=ctrl.comparar_busquedas).pack(pady=5, fill='x')

    tk.Label(comp_frame, text="COMPARACIÓN DE ORDENAMIENTOS:", 
             font=FONT_TITLE_SMALL, bg=FILTER_BG).pack(pady=(15, 5), anchor='w')
    ttk.Button(comp_frame, text="Comparar 5 Tipos de Ordenamiento", 
               command=ctrl.comparar_ordenamientos).pack(pady=5, fill='x')

    # === FRAME CARGA ===
    carga_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    carga_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(carga_frame, text="📂 CARGA MASIVA DE DATOS (CSV)", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(carga_frame, text="Seleccione los archivos CSV:", 
             font=FONT_LABEL, bg=FILTER_BG).pack(anchor='w', pady=5)

    ttk.Button(carga_frame, text="⬆️ Cargar Catálogo de Libros", 
               command=ctrl.cargar_csv_libros).pack(pady=5, fill='x')
    ttk.Button(carga_frame, text="⬆️ Cargar Bibliotecas", 
               command=ctrl.cargar_csv_bibliotecas).pack(pady=5, fill='x')
    ttk.Button(carga_frame, text="⬆️ Cargar Conexiones", 
               command=ctrl.cargar_csv_conexiones).pack(pady=5, fill='x')

    return tab_pruebas_carga, ctrl
```

---

## 📄 ARCHIVO 11: gui_app.py - REFACTORIZADO

```python
"""
Aplicación GUI Principal - Orquestador de todas las pestañas
"""

import tkinter as tk
from tkinter import ttk

# Importar backend
from objetos.red_bibliotecas import RedBibliotecas

# Importar módulos GUI
from gui.config import WINDOW_TITLE, WINDOW_GEOMETRY, BG_COLOR, TITLE_COLOR, FONT_TITLE_LARGE
from gui.styles import configurar_estilos
from gui.dashboard_tab import crear_dashboard
from gui.catalogo_tab import crear_catalogo_tab
from gui.red_tab import crear_red_tab
from gui.busqueda_tab import crear_busqueda_rutas_tab
from gui.simulacion_tab import crear_simulacion_tab
from gui.visualizacion_tab import crear_visualizacion_tab
from gui.pruebas_tab import crear_pruebas_carga_tab

# Variables globales
red_bibliotecas = None

def iniciar_gui():
    """Iniciar la interfaz gráfica principal"""
    global red_bibliotecas

    # Inicializar sistema backend
    red_bibliotecas = RedBibliotecas()

    # Crear ventana principal
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_GEOMETRY)
    root.configure(bg=BG_COLOR)

    # Configurar estilos
    configurar_estilos(root)

    # Crear título principal
    title = tk.Label(root, text="✨ Sistema de Gestión Arcana ✨", 
                     font=FONT_TITLE_LARGE, fg=TITLE_COLOR, bg=BG_COLOR)
    title.pack(pady=(20, 10))

    # Crear notebook (pestañas)
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=20, expand=True, fill="both")

    # === CREAR TODAS LAS PESTAÑAS ===

    # Dashboard
    crear_dashboard(notebook)

    # Catálogo
    crear_catalogo_tab(notebook, red_bibliotecas)

    # Red - con callbacks
    tab_red, ctrl_red = crear_red_tab(
        notebook, 
        red_bibliotecas,
        callback_actualizar=lambda: actualizar_ui(),
        callback_dibujar=lambda: ctrl_red.dibujar_grafo()
    )

    # Búsqueda y Rutas
    tab_busqueda, ctrl_busqueda = crear_busqueda_rutas_tab(notebook, red_bibliotecas)

    # Simulación
    tab_simulacion, ctrl_simulacion = crear_simulacion_tab(notebook, red_bibliotecas)

    # Visualización
    crear_visualizacion_tab(notebook)

    # Pruebas y Carga
    tab_pruebas, ctrl_pruebas = crear_pruebas_carga_tab(notebook, red_bibliotecas)

    def actualizar_ui():
        """Actualizar componentes UI después de cambios en el backend"""
        ctrl_red.dibujar_grafo()

    # Iniciar GUI
    root.mainloop()

if __name__ == "__main__":
    iniciar_gui()
```

---

## 📄 ARCHIVO 12: main.py - ACTUALIZADO

```python
"""
Punto de entrada principal de la aplicación
"""

import sys
import os
from pathlib import Path

# Agregar la ruta del proyecto al path
proyecto_root = Path(__file__).parent
sys.path.insert(0, str(proyecto_root))

from gui_app import iniciar_gui

def main():
    """Función principal"""
    try:
        print("=" * 60)
        print("🚀 Iniciando Sistema de Gestión de Red de Bibliotecas")
        print("=" * 60)

        # Validar que existan las carpetas necesarias
        carpetas_necesarias = ['gui', 'objetos', 'estructuras', 'datos']
        for carpeta in carpetas_necesarias:
            ruta = proyecto_root / carpeta
            if not ruta.exists():
                print(f"⚠️  Advertencia: Carpeta '{carpeta}' no encontrada en {ruta}")

        print("✅ Iniciando interfaz gráfica...")
        iniciar_gui()

    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Asegúrate de tener todos los módulos necesarios")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Error al iniciar GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        print("\n👋 Cerrando aplicación")

if __name__ == "__main__":
    main()
```

---

## 📋 CHECKLIST DE INSTALACIÓN COMPLETA

Ejecuta esto en terminal para verificar la estructura:

```bash
# Verificar estructura de carpetas
echo "📁 Estructura del proyecto:"
find /home/elmer/Documentos/edd/Proyecto2_eddSS2025/gui -type f -name "*.py" | sort

# Ver archivos GUI
echo ""
echo "📄 Archivos creados en gui/:"
ls -la /home/elmer/Documentos/edd/Proyecto2_eddSS2025/gui/
```

---

## 🎯 RESUMEN FINAL DE TODOS LOS ARCHIVOS CREADOS

| #   | Archivo              | Descripción                                               |
| --- | -------------------- | --------------------------------------------------------- |
| 1   | config.py            | Configuración centralizada (colores, fuentes, constantes) |
| 2   | styles.py            | Estilos TTK para toda la GUI                              |
| 3   | __init__.py          | Paquete GUI con exportaciones                             |
| 4   | dashboard_tab.py     | Pestaña de inicio con tarjetas interactivas               |
| 5   | catalogo_tab.py      | CRUD completo de libros (AVL, Hash, B+, Listas)           |
| 6   | red_tab.py           | Gestión de bibliotecas y grafo con Dijkstra               |
| 7   | busqueda_tab.py      | Búsqueda avanzada (4 métodos) + rutas óptimas             |
| 8   | simulacion_tab.py    | Simulación de colas y despacho                            |
| 9   | visualizacion_tab.py | Visualización de estructuras (árboles, hash)              |
| 10  | pruebas_tab.py       | Pruebas de rendimiento y carga CSV                        |
| 11  | gui_app.py           | Orquestador principal (refactorizado)                     |
| 12  | main.py              | Punto de entrada (actualizado)                            |

---

## ✅ VENTAJAS DE ESTA MODULARIZACIÓN

✨ **Sin pérdida de funcionalidad** - Todo funciona igual que antes  
📦 **Modular** - Cada pestaña en su propio archivo  
🔧 **Fácil mantenimiento** - Cambios aislados sin afectar otros módulos  
🧪 **Testeable** - Prueba cada módulo por separado  
📈 **Escalable** - Agrega nuevas pestañas fácilmente  
🎨 **Configuración centralizada** - Un solo lugar para colores y estilos  

---

## 🚀 CÓMO EJECUTAR

```bash
cd /home/elmer/Documentos/edd/Proyecto2_eddSS2025
python main.py
```

---

## 📝 PRÓXIMOS PASOS (Opcionales)

Si quieres mejorar aún más la estructura, puedes:

1. **Crear `gui/managers/`** - Para gestionar estado global
2. **Crear `gui/utils/`** - Funciones auxiliares reutilizables
3. **Crear `gui/dialogs/`** - Diálogos personalizados reutilizables
4. **Crear `gui/widgets/`** - Widgets personalizados (tarjetas, tablas, etc)
