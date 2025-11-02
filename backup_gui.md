### Carpeta: ./ (raíz)



**Archivo:** gui_app.py  
**Ruta:** gui_app.py  
**Tamaño:** 2412 bytes  

```py
"""
Aplicación GUI Principal - Orquestador de todas las pestañas
"""

import tkinter as tk
from tkinter import ttk

from objetos.red_bibliotecas import RedBibliotecas

from gui.config import WINDOW_TITLE, WINDOW_GEOMETRY, BG_COLOR, TITLE_COLOR, FONT_TITLE_LARGE
from gui.styles import configurar_estilos
from gui.dashboard_tab import crear_dashboard
from gui.catalogo_tab import crear_catalogo_tab
from gui.red_tab import crear_red_tab
from gui.busqueda_tab import crear_busqueda_rutas_tab
from gui.simulacion_tab import crear_simulacion_tab
from gui.visualizacion_tab import crear_visualizacion_tab
from gui.pruebas_tab import crear_pruebas_carga_tab

red_bibliotecas = None

def iniciar_gui():
    """Iniciar la interfaz gráfica principal"""
    global red_bibliotecas

    red_bibliotecas = RedBibliotecas()

    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_GEOMETRY)
    root.configure(bg=BG_COLOR)

    configurar_estilos(root)

    title = tk.Label(root, text="✨ Sistema de Gestión Arcana ✨", 
                     font=FONT_TITLE_LARGE, fg=TITLE_COLOR, bg=BG_COLOR)
    title.pack(pady=(20, 10))

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=20, expand=True, fill="both")

    crear_dashboard(notebook)

    tab_catalogo, ctrl_catalogo = crear_catalogo_tab(notebook, red_bibliotecas)
    tab_red, ctrl_red = crear_red_tab(notebook, red_bibliotecas)
    tab_busqueda, ctrl_busqueda = crear_busqueda_rutas_tab(notebook, red_bibliotecas)
    tab_simulacion, ctrl_simulacion = crear_simulacion_tab(notebook, red_bibliotecas)
    tab_visualizacion, ctrl_visualizacion = crear_visualizacion_tab(notebook, red_bibliotecas)
    tab_pruebas, ctrl_pruebas = crear_pruebas_carga_tab(notebook, red_bibliotecas)

    def actualizar_ui():
        if ctrl_catalogo:
            ctrl_catalogo.refrescar_datos()
        if ctrl_red and hasattr(ctrl_red, "callback_actualizar") and callable(ctrl_red.callback_actualizar):
            ctrl_red.callback_actualizar()
        if ctrl_simulacion:
            ctrl_simulacion.actualizar_estado()
        if hasattr(ctrl_busqueda, "refrescar_datos") and callable(ctrl_busqueda.refrescar_datos):
            ctrl_busqueda.refrescar_datos()

    ctrl_pruebas.on_datos_actualizados = actualizar_ui

    actualizar_ui()

    root.mainloop()

if __name__ == "__main__":
    iniciar_gui()
```

**Archivo:** main.py  
**Ruta:** main.py  
**Tamaño:** 216 bytes  

```py
import sys
from gui_app import iniciar_gui

def main():
    try:
        iniciar_gui()
    except Exception as e:
        print(f"Error al iniciar GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

### Carpeta: gui

**Archivo:** __init__.py  
**Ruta:** gui/__init__.py  
**Tamaño:** 674 bytes  

```py
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

**Archivo:** busqueda_tab.py  
**Ruta:** gui/busqueda_tab.py  
**Tamaño:** 13823 bytes  

```py
"""
Pestaña Búsqueda y Rutas Óptimas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .config import *

class BusquedaTab:
    """Controlador de la pestaña de Búsqueda y Rutas"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.ruta_resultado_label = None

        # Variables de entrada de Ruta
        self.ruta_origen_var = tk.StringVar()
        self.ruta_destino_var = tk.StringVar()
        self.criterio_var = tk.StringVar(value="tiempo")

        # Búsqueda unificada (NUEVO)
        self.criterio_busqueda_var = tk.StringVar(value="Título (AVL)")
        self.search_text_var = tk.StringVar()
        self.search_aux_var = tk.StringVar()
        self._generos_cache = []
        self.search_entry: ttk.Combobox | None = None
        self.search_aux_entry: ttk.Entry | None = None

    def actualizar_generos_combo(self, genero_combo):
        """Actualiza combo de géneros disponibles"""
        generos = self._obtener_generos_disponibles()
        genero_combo["values"] = generos
        genero_combo.configure(state="readonly" if generos else "disabled")

    def _obtener_generos_disponibles(self):
        """Recopila y retorna la lista de géneros únicos disponibles."""
        generos = set()
        for bib in self.red_bibliotecas.bibliotecas.values():
            try:
                # Asumiendo que catalogo_local tiene el método obtener_generos_unicos()
                generos.update(bib.catalogo_local.obtener_generos_unicos())
            except Exception:
                continue
        self._generos_cache = sorted(generos)
        return self._generos_cache

    def actualizar_comboboxes_rutas(self, origen_combo, destino_combo):
        """Actualiza comboboxes de bibliotecas para rutas"""
        bibliotecas_ids = list(self.red_bibliotecas.bibliotecas.keys())

        if bibliotecas_ids:
            origen_combo['values'] = bibliotecas_ids
            destino_combo['values'] = bibliotecas_ids

    def ejecutar_busqueda(self):
        """Método unificado para realizar la búsqueda según el criterio seleccionado."""
        criterio = self.criterio_busqueda_var.get()
        texto = self.search_text_var.get().strip()
        auxiliar = self.search_aux_var.get().strip()

        if not texto and criterio != "Rango de Fechas (B)":
            messagebox.showwarning("Advertencia", "Ingrese un valor de búsqueda")
            return

        if criterio == "Rango de Fechas (B)" and (not texto or not auxiliar):
             messagebox.showerror("Error", "Ingrese años de inicio y fin")
             return

        resultados = [] # Lista de (Libro, ID_Biblioteca)
        for biblioteca_id, biblioteca in self.red_bibliotecas.bibliotecas.items():
            catalogo = biblioteca.catalogo_local
            try:
                if criterio == "Título (AVL)":
                    libro = catalogo.buscar_por_titulo(texto)
                    if libro:
                        resultados.append((libro, biblioteca_id))
                elif criterio == "ISBN (Hash)":
                    libro = catalogo.buscar_por_isbn(texto)
                    if libro:
                        resultados.append((libro, biblioteca_id))
                        # Si es por ISBN, asumimos unicidad global y terminamos la búsqueda
                        break 
                elif criterio == "Género (B+)":
                    for libro in catalogo.buscar_por_genero(texto):
                        resultados.append((libro, biblioteca_id))
                elif criterio == "Rango de Fechas (B)":
                    try:
                        inicio, fin = int(texto), int(auxiliar)
                    except ValueError:
                        messagebox.showerror("Error", "Los años deben ser números válidos")
                        return
                    for libro in catalogo.buscar_por_rango_fechas(inicio, fin):
                        resultados.append((libro, biblioteca_id))
            except Exception:
                continue

        # Generar texto de criterio para el resultado
        if criterio == "Rango de Fechas (B)":
            criterio_texto = f"{criterio}: {texto} - {auxiliar}"
        else:
            criterio_texto = f"{criterio}: {texto}"

        if not resultados:
            messagebox.showinfo("Búsqueda", f"No se encontraron libros para {criterio_texto}")
            return

        self._mostrar_resultados_busqueda(resultados, criterio_texto)

    def limpiar_busqueda(self):
        """Limpia los campos de búsqueda."""
        self.search_text_var.set("")
        self.search_aux_var.set("")
        self._on_criterio_cambiado() # Opcional: restablecer el estado del combobox/entry

    def _on_criterio_cambiado(self, *args):
        """Maneja el cambio de criterio de búsqueda para actualizar la UI."""
        if not self.search_entry or not self.search_aux_entry:
            return

        criterio = self.criterio_busqueda_var.get()
        self.search_text_var.set("")
        self.search_aux_var.set("") # Limpiar auxiliar al cambiar criterio

        if criterio == "Rango de Fechas (B)":
            # Para rango, ambos son entry de texto (años)
            self.search_entry.configure(values=(), state="normal") 
            self.search_aux_entry.configure(state="normal")
        else:
            self.search_aux_entry.configure(state="disabled")
            if criterio == "Género (B+)":
                # Para género, es un combobox de selección obligatoria (readonly)
                generos = self._obtener_generos_disponibles()
                self.search_entry.configure(values=generos, state="readonly")
            else:
                # Para Título/ISBN, es un entry de texto normal
                self.search_entry.configure(values=(), state="normal")

    def _mostrar_resultados_busqueda(self, resultados, criterio):
        """Mostrar resultados en una ventana nueva"""

        ventana = tk.Toplevel()
        ventana.title(f"Resultados - {criterio}")
        ventana.geometry("900x400")
        ventana.configure(bg=BG_COLOR)

        frame = ttk.Frame(ventana, style='Sky.TFrame', padding=10)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text=f"Resultados para {criterio} ({len(resultados)} encontrados):",
                font=FONT_TITLE_MEDIUM, bg=FILTER_BG).pack(pady=(0, 10))

        # Columna extra para la Biblioteca de Origen (NUEVO)
        tree = ttk.Treeview(frame, columns=("Título", "Autor", "ISBN", "Año", "Género", "Biblioteca"), 
                           show='headings')
        tree.heading("Título", text="Título")
        tree.heading("Autor", text="Autor")
        tree.heading("ISBN", text="ISBN")
        tree.heading("Año", text="Año")
        tree.heading("Género", text="Género")
        tree.heading("Biblioteca", text="Biblioteca Origen")

        for libro, biblioteca_id in resultados:
            tree.insert("", "end", values=(
                libro.titulo, libro.autor, libro.isbn, libro.anio, libro.genero, biblioteca_id
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

    # === FRAME BÚSQUEDA UNIFICADA (NUEVO) ===
    search_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
    search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(search_frame, text="🔍 BÚSQUEDA AVANZADA", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    filtros_container = ttk.Frame(search_frame, style='Sky.TFrame')
    filtros_container.pack(fill='x', pady=5)

    # Criterio
    ttk.Label(filtros_container, text="Criterio:", background=FILTER_BG).grid(row=0, column=0, sticky="w", padx=2, pady=2)
    ttk.Combobox(
        filtros_container,
        textvariable=ctrl.criterio_busqueda_var,
        values=["Título (AVL)", "ISBN (Hash)", "Género (B+)", "Rango de Fechas (B)"],
        state="readonly",
        width=18,
    ).grid(row=0, column=1, padx=4, pady=2, sticky="w")

    # Valor Principal
    ttk.Label(filtros_container, text="Valor:", background=FILTER_BG).grid(row=1, column=0, sticky="w", padx=2, pady=2)
    ctrl.search_entry = ttk.Combobox(filtros_container, textvariable=ctrl.search_text_var, width=28)
    ctrl.search_entry.grid(row=1, column=1, padx=4, pady=2, sticky="ew")

    # Valor Auxiliar (para Rango de Fechas)
    ttk.Label(filtros_container, text="Auxiliar (solo rango):", background=FILTER_BG).grid(row=2, column=0, sticky="w", padx=2, pady=2)
    ctrl.search_aux_entry = ttk.Entry(filtros_container, textvariable=ctrl.search_aux_var, width=18)
    ctrl.search_aux_entry.grid(row=2, column=1, padx=4, pady=2, sticky="w")
    ctrl.search_aux_entry.configure(state="disabled")

    # Botones de Acción
    acciones_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    acciones_frame.pack(fill='x', pady=8)
    ttk.Button(acciones_frame, text="🔍 Buscar", command=ctrl.ejecutar_busqueda).pack(side='left', padx=4)
    ttk.Button(acciones_frame, text="🗑️ Limpiar", command=ctrl.limpiar_busqueda).pack(side='left', padx=4)

    # Enlace de Criterio de Búsqueda
    ctrl.criterio_busqueda_var.trace_add("write", ctrl._on_criterio_cambiado)
    ctrl._on_criterio_cambiado() # Llamada inicial para configurar la UI

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

    # Actualizar comboboxes de ruta y precargar géneros
    ctrl.actualizar_comboboxes_rutas(ruta_origen_combo, ruta_destino_combo)
    ctrl._obtener_generos_disponibles() # Solo cargar el caché al inicio

    return tab_busqueda_rutas, ctrl
```

**Archivo:** catalogo_tab.py  
**Ruta:** gui/catalogo_tab.py  
**Tamaño:** 22316 bytes  

```py
"""
Pestaña Catálogo - CRUD de libros y gestión de catálogo
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .config import *
from objetos.libro import Libro
# Importar métodos de ordenamiento
from estructuras.metodos_ordenamiento import (
    burbuja,
    seleccion,
    insercion,
    shell_sort,
    quick_sort,
)

class CatalogoTab:
    """Controlador de la pestaña de Catálogo"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.catalog_tree = None

        # referencias a comboboxes
        self.combo_origen = None
        self.combo_destino = None

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

        # Búsqueda y ordenamiento (NUEVO)
        self.search_text_var = tk.StringVar()
        self.search_aux_var = tk.StringVar()
        self.criterio_busqueda_var = tk.StringVar(value="Título (AVL)")
        self.campo_orden_var = tk.StringVar(value="titulo")
        self.algoritmo_orden_var = tk.StringVar(value="QuickSort")
        self.resumen_var = tk.StringVar(value="0 libros en catálogo")
        self.search_aux_entry = None # Para manejar la habilitación/deshabilitación

        self._metodos_orden = {
            "Burbuja": burbuja,
            "Selección": seleccion,
            "Inserción": insercion,
            "Shell Sort": shell_sort,
            "QuickSort": quick_sort,
        }

    def configurar_comboboxes(self, combo_origen: ttk.Combobox, combo_destino: ttk.Combobox):
        self.combo_origen = combo_origen
        self.combo_destino = combo_destino
        self.actualizar_comboboxes_origen_destino(combo_origen, combo_destino)

    def refrescar_datos(self):
        self.actualizar_catalogo_tree()
        if self.combo_origen and self.combo_destino:
            self.actualizar_comboboxes_origen_destino(self.combo_origen, self.combo_destino)
        self._actualizar_generos() # NUEVO

    def actualizar_catalogo_tree(self):
        """Actualiza el TreeView con libros del catálogo, aplicando filtros y ordenamiento."""
        if not self.catalog_tree:
            return

        # Usa el método para obtener libros filtrados/ordenados
        libros = self._obtener_libros_filtrados()
        self.catalog_tree.delete(*self.catalog_tree.get_children())

        for libro, biblioteca_id in libros:
            self.catalog_tree.insert("", "end", values=(
                libro.titulo, 
                libro.autor, 
                libro.isbn, 
                libro.estado, 
                biblioteca_id,
                libro.anio, # NUEVO CAMPO
                libro.genero, # NUEVO CAMPO
            ))

        self.resumen_var.set(f"{len(libros)} libros en catálogo") # NUEVO

    def actualizar_comboboxes_origen_destino(self, combo_origen, combo_destino):
        """Actualiza comboboxes de bibliotecas"""
        bibliotecas_ids = list(self.red_bibliotecas.bibliotecas.keys())

        combo_origen['values'] = bibliotecas_ids
        combo_destino['values'] = bibliotecas_ids

        if bibliotecas_ids and not self.biblioteca_origen_var.get():
            self.biblioteca_origen_var.set(bibliotecas_ids[0])

    def agregar_libro(self):
        """Agregar nuevo libro con todos los campos"""
        try:
            if not all([self.titulo_var.get().strip(), self.autor_var.get().strip(), 
                       self.isbn_var.get().strip()]):
                messagebox.showerror("Error", "Título, autor e ISBN son obligatorios")
                return

            if not self.red_bibliotecas.bibliotecas:
                messagebox.showerror("Error", "No hay bibliotecas registradas.")
                return

            try:
                anio = int(self.anio_var.get() or "0")
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número válido")
                return

            libro = Libro(
                titulo=self.titulo_var.get().strip(),
                isbn=self.isbn_var.get().strip(),
                genero=self.genero_var.get().strip(),
                anio=anio,
                autor=self.autor_var.get().strip(),
                estado=self.estado_var.get(),
                biblioteca_origen=self.biblioteca_origen_var.get().strip(),
                biblioteca_destino=self.biblioteca_destino_var.get().strip(),
                prioridad=self.prioridad_var.get()
            )

            bib_origen_id = libro.biblioteca_origen or next(iter(self.red_bibliotecas.bibliotecas.keys()))
            biblioteca_origen = self.red_bibliotecas.bibliotecas.get(bib_origen_id)
            if not biblioteca_origen:
                messagebox.showerror("Error", f"Biblioteca origen '{bib_origen_id}' no existe")
                return

            # Agregar libro al catálogo local de la biblioteca de origen
            biblioteca_origen.agregar_libro_catalogo(libro)

            bib_destino_id = libro.biblioteca_destino
            if bib_destino_id and bib_destino_id != bib_origen_id:
                # Iniciar transferencia si se especificó un destino diferente
                self.red_bibliotecas.iniciar_transferencia(
                    libro.isbn, bib_origen_id, bib_destino_id, libro.prioridad
                )

            self._limpiar_formulario()
            self.refrescar_datos()
            messagebox.showinfo("Éxito", f"Libro '{libro.titulo}' agregado correctamente")

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
                self.refrescar_datos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el libro")

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar libro: {e}")

    def rollback_operacion(self):
        """Deshacer última operación"""
        try:
            if not self.red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas registradas")
                return

            bib_id = self.biblioteca_origen_var.get() or next(iter(self.red_bibliotecas.bibliotecas.keys()))
            biblioteca = self.red_bibliotecas.bibliotecas[bib_id]
            libro_restaurado = biblioteca.rollback_ultimo_ingreso()

            if libro_restaurado:
                messagebox.showinfo("Éxito", f"Operación deshecha: {libro_restaurado.titulo}")
                self.refrescar_datos()
            else:
                messagebox.showwarning("Advertencia", "No hay operaciones para deshacer")
        except Exception as e:
            messagebox.showerror("Error", f"Error en rollback: {e}")

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario y campos de búsqueda"""
        self.titulo_var.set("")
        self.autor_var.set("")
        self.isbn_var.set("")
        self.anio_var.set("")
        self.genero_var.set("")
        self.estado_var.set("disponible")
        self.biblioteca_origen_var.set("")
        self.biblioteca_destino_var.set("")
        self.prioridad_var.set("tiempo")
        self.search_text_var.set("") # NUEVO
        self.search_aux_var.set("") # NUEVO
        self.resumen_var.set("0 libros en catálogo") # NUEVO

    # ---------------------------------
    # Nuevas utilidades de catálogo
    # ---------------------------------
    def _actualizar_generos(self):
        """Recopila y actualiza la lista de géneros únicos disponibles."""
        generos = set()
        for biblioteca in self.red_bibliotecas.bibliotecas.values():
            try:
                # Asumiendo que catalogo_local tiene un método para obtener géneros
                generos.update(biblioteca.catalogo_local.obtener_generos_unicos())
            except Exception:
                continue
        generos_ordenados = sorted(generos)
        # Se asume que el ComboBox de género de búsqueda (si existiera) se actualizaría aquí.
        # Por ahora, solo actualiza la variable de género del formulario si es necesario.
        # if hasattr(self, "genero_busqueda_combo"):
        #     self.genero_busqueda_combo["values"] = generos_ordenados
        # self.genero_var.set(generos_ordenados[0] if generos_ordenados else "") # Mejor no cambiar el valor al azar

    def _obtener_libros_filtrados(self):
        """
        Recopila, filtra (usando la estructura de datos apropiada) y ordena
        la lista total de libros.
        Retorna: Lista de (Libro, ID_Biblioteca)
        """
        libros = []
        criterio = self.criterio_busqueda_var.get()
        texto = self.search_text_var.get().strip()
        auxiliar = self.search_aux_var.get().strip()

        # 1. Recopilar y Filtrar libros
        for biblioteca_id, biblioteca in self.red_bibliotecas.bibliotecas.items():
            catalogo = biblioteca.catalogo_local
            try:
                if not texto: # Si no hay texto de búsqueda, muestra todo (secuencial)
                    for libro in catalogo.lista_secuencial.mostrar_todos() or []:
                        libros.append((libro, biblioteca_id))
                    continue # Pasar a la siguiente biblioteca

                # Búsqueda usando las estructuras correspondientes
                if criterio == "Título (AVL)":
                    libro = catalogo.buscar_por_titulo(texto)
                    if libro:
                        libros.append((libro, biblioteca_id))

                elif criterio == "ISBN (Hash)":
                    libro = catalogo.buscar_por_isbn(texto)
                    if libro:
                        libros.append((libro, biblioteca_id))

                elif criterio == "Género (B+)":
                    # Asumiendo que buscar_por_genero retorna una lista de libros
                    for libro in catalogo.buscar_por_genero(texto):
                        libros.append((libro, biblioteca_id))

                elif criterio == "Rango de Fechas (B)":
                    if not auxiliar: continue
                    try:
                        inicio, fin = int(texto), int(auxiliar)
                    except ValueError:
                        continue
                    # Asumiendo que buscar_por_rango_fechas retorna una lista de libros
                    for libro in catalogo.buscar_por_rango_fechas(inicio, fin):
                        libros.append((libro, biblioteca_id))

            except Exception as e:
                # Ignorar errores de bibliotecas específicas al buscar/filtrar
                print(f"Error al buscar/filtrar en {biblioteca_id}: {e}")
                continue

        # Si hay un criterio de búsqueda activo, solo mostramos los resultados del filtro
        # Si no hay texto, mostramos todos (ya recopilados arriba)

        # 2. Ordenar libros
        metodo = self._metodos_orden.get(self.algoritmo_orden_var.get(), quick_sort)
        campo = self.campo_orden_var.get()

        if libros:
            # Separar los objetos Libro para la ordenación
            solo_libros = [libro for libro, _ in libros]
            ordenados = metodo(solo_libros, campo)

            # Re-asociar los libros ordenados con sus IDs de biblioteca
            # Esto es ineficiente pero necesario para mantener la relación (Libro, ID_Biblioteca)
            ordenados_con_bib = []

            # Usar un mapa de ISBNs a (Libro, ID) para una búsqueda más rápida
            # (aunque el ordenamiento es la parte más lenta)
            libros_map = {original[0].isbn: original for original in libros}

            for libro_ordenado in ordenados:
                original = libros_map.get(libro_ordenado.isbn)
                if original:
                    ordenados_con_bib.append(original)

            libros = ordenados_con_bib

        return libros

    def aplicar_busqueda(self):
        """Botón de Buscar: Refresca el treeview con los criterios actuales."""
        self.actualizar_catalogo_tree()

    def limpiar_busqueda(self):
        """Botón de Limpiar: Restablece campos de búsqueda y refresca."""
        self.search_text_var.set("")
        self.search_aux_var.set("")
        self.actualizar_catalogo_tree()

    def _on_criterio_cambiado(self, *args):
        """Habilita/Deshabilita el campo auxiliar según el criterio de búsqueda."""
        habilitar_rango = self.criterio_busqueda_var.get() == "Rango de Fechas (B)"
        state = "normal" if habilitar_rango else "disabled"
        if self.search_aux_entry:
            self.search_aux_entry.configure(state=state)

        if not habilitar_rango:
            self.search_aux_var.set("")

# ----------------------------------------------------------------------
# Funciones de creación de la UI
# ----------------------------------------------------------------------

def crear_catalogo_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Catálogo"""

    tab_catalogo = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_catalogo, text="📚 Catálogo y Libro (CRUD)")

    # Grid principal (3 filas: Filtros, CRUD, Listado)
    tab_catalogo.grid_columnconfigure((0, 1), weight=1)
    tab_catalogo.grid_rowconfigure(1, weight=1) # El frame de listado es la fila 1, columna 1

    ctrl = CatalogoTab(red_bibliotecas)

    # --- 1. BARRA DE FILTROS Y ORDENAMIENTO (NUEVO) ---
    filtros_frame = ttk.Frame(tab_catalogo, style="Sky.TFrame", padding=10)
    # Colocar en la parte superior, abarcando ambas columnas
    filtros_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
    filtros_frame.grid_columnconfigure(1, weight=1) # El campo de búsqueda principal toma espacio extra

    tk.Label(
        filtros_frame,
        text="🔎 BÚSQUEDA AVANZADA",
        font=FONT_TITLE_SMALL,
        fg=TITLE_COLOR,
        bg=FILTER_BG,
    ).grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 5))

    # Criterio de Búsqueda
    ttk.Combobox(
        filtros_frame,
        textvariable=ctrl.criterio_busqueda_var,
        values=[
            "Título (AVL)",
            "ISBN (Hash)",
            "Género (B+)",
            "Rango de Fechas (B)",
        ],
        state="readonly",
        width=18,
    ).grid(row=1, column=0, padx=3, pady=3, sticky="w")

    # Campo de Búsqueda Principal
    ctrl.search_entry = ttk.Entry(filtros_frame, textvariable=ctrl.search_text_var, width=28)
    ctrl.search_entry.grid(row=1, column=1, padx=3, pady=3, sticky="ew")

    # Campo de Búsqueda Auxiliar (para rangos)
    ctrl.search_aux_entry = ttk.Entry(filtros_frame, textvariable=ctrl.search_aux_var, width=12)
    ctrl.search_aux_entry.grid(row=1, column=2, padx=3, pady=3)

    # Botones de Búsqueda y Limpiar
    ttk.Button(filtros_frame, text="Buscar", command=ctrl.aplicar_busqueda).grid(
        row=1, column=3, padx=3, pady=3
    )
    ttk.Button(filtros_frame, text="Limpiar", command=ctrl.limpiar_busqueda).grid(
        row=1, column=4, padx=3, pady=3
    )

    # --- Controles de Ordenamiento ---
    tk.Label(
        filtros_frame,
        text="Ordenar por:",
        bg=FILTER_BG,
    ).grid(row=2, column=0, sticky="w", pady=(10, 5))

    # Campo de ordenamiento
    ttk.Combobox(
        filtros_frame,
        textvariable=ctrl.campo_orden_var,
        values=["titulo", "autor", "anio"],
        state="readonly",
        width=12,
    ).grid(row=2, column=1, padx=3, pady=(10, 5), sticky="w")

    # Algoritmo de ordenamiento
    ttk.Combobox(
        filtros_frame,
        textvariable=ctrl.algoritmo_orden_var,
        values=list(ctrl._metodos_orden.keys()),
        state="readonly",
        width=14,
    ).grid(row=2, column=2, padx=3, pady=(10, 5), sticky="w")

    # Botón para aplicar ordenamiento
    ttk.Button(
        filtros_frame,
        text="Aplicar Ordenamiento",
        command=ctrl.actualizar_catalogo_tree,
    ).grid(row=2, column=3, padx=3, pady=(10, 5), sticky="w")

    # Resumen de libros
    ttk.Label(
        filtros_frame,
        textvariable=ctrl.resumen_var,
        font=FONT_LABEL_SMALL,
        background=FILTER_BG,
    ).grid(row=2, column=4, padx=6, pady=(10, 5), sticky="e")

    # Enlace del cambio de criterio con el controlador para habilitar/deshabilitar el campo auxiliar
    ctrl.criterio_busqueda_var.trace_add("write", ctrl._on_criterio_cambiado)

    # --- 2. CRUD y Control de Pilas ---
    crud_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    crud_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(crud_frame, text="✏️ REGISTRO DE LIBRO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 15))

    tk.Label(crud_frame, text="Título:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.titulo_var, width=40).pack(fill='x')

    tk.Label(crud_frame, text="Autor:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.autor_var, width=40).pack(fill='x')

    tk.Label(crud_frame, text="ISBN:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.isbn_var, width=20).pack(fill='x')

    tk.Label(crud_frame, text="Año de publicación:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.anio_var, width=10).pack(fill='x')

    tk.Label(crud_frame, text="Género:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=ctrl.genero_var, width=20).pack(fill='x')

    tk.Label(crud_frame, text="Estado:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Combobox(crud_frame, textvariable=ctrl.estado_var, 
                 values=["disponible", "prestado", "en_transito", "agotado"]).pack(fill='x')

    tk.Label(crud_frame, text="Biblioteca Origen:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    biblioteca_origen_combo = ttk.Combobox(crud_frame, textvariable=ctrl.biblioteca_origen_var)
    biblioteca_origen_combo.pack(fill='x')

    tk.Label(crud_frame, text="Biblioteca Destino:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    biblioteca_destino_combo = ttk.Combobox(crud_frame, textvariable=ctrl.biblioteca_destino_var)
    biblioteca_destino_combo.pack(fill='x')

    tk.Label(crud_frame, text="Prioridad de Envío:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    prioridad_frame = ttk.Frame(crud_frame)
    prioridad_frame.pack(fill='x', pady=2)
    ttk.Radiobutton(prioridad_frame, text="Tiempo", 
                    variable=ctrl.prioridad_var, value="tiempo").pack(side='left', padx=10)
    ttk.Radiobutton(prioridad_frame, text="Costo", 
                    variable=ctrl.prioridad_var, value="costo").pack(side='left', padx=10)

    ttk.Button(crud_frame, text="➕ Agregar Libro", 
               command=ctrl.agregar_libro).pack(pady=(20, 5), fill='x')
    ttk.Button(crud_frame, text="🗑️ Eliminar Libro", 
               command=ctrl.eliminar_libro).pack(pady=5, fill='x')

    tk.Label(crud_frame, text="🔄 CONTROL DE PILAS", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(20, 10))
    ttk.Button(crud_frame, text="↩️ Deshacer Última Operación", 
               command=ctrl.rollback_operacion).pack(pady=5, fill='x')

    # --- 3. LISTADO (Treeview) ---
    listado_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    listado_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    listado_frame.grid_rowconfigure(2, weight=1)

    tk.Label(listado_frame, text="📖 LISTADO Y ALMACENAMIENTO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    ttk.Button(listado_frame, text="🔄 Actualizar Catálogo", 
               command=ctrl.refrescar_datos).pack(fill='x', pady=5)

    tk.Label(listado_frame, text="CATÁLOGO COMPLETO:", 
             font=FONT_TITLE_SMALL, bg=FILTER_BG).pack(anchor='w', pady=(10, 0))

    # Columnas del Treeview Actualizadas
    ctrl.catalog_tree = ttk.Treeview(
        listado_frame, 
        columns=("Título", "Autor", "ISBN", "Estado", "Biblioteca", "Año", "Género"), 
        show='headings'
    )
    ctrl.catalog_tree.heading("Título", text="Título")
    ctrl.catalog_tree.heading("Autor", text="Autor")
    ctrl.catalog_tree.heading("ISBN", text="ISBN")
    ctrl.catalog_tree.heading("Estado", text="Estado")
    ctrl.catalog_tree.heading("Biblioteca", text="Biblioteca")
    ctrl.catalog_tree.heading("Año", text="Año")
    ctrl.catalog_tree.heading("Género", text="Género")
    ctrl.catalog_tree.pack(fill='both', expand=True, pady=(5, 0))

    # Configuración final
    ctrl.configurar_comboboxes(biblioteca_origen_combo, biblioteca_destino_combo)
    ctrl._on_criterio_cambiado() # Asegurar que el campo auxiliar esté en el estado inicial correcto
    ctrl.refrescar_datos()

    return tab_catalogo, ctrl
```

**Archivo:** config.py  
**Ruta:** gui/config.py  
**Tamaño:** 736 bytes  

```py
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

**Archivo:** dashboard_tab.py  
**Ruta:** gui/dashboard_tab.py  
**Tamaño:** 2526 bytes  

```py
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

**Archivo:** pruebas_tab.py  
**Ruta:** gui/pruebas_tab.py  
**Tamaño:** 7562 bytes  

```py
"""
Pestaña Pruebas - Pruebas de rendimiento, carga CSV y comparaciones
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
from typing import Callable, Optional
from .config import *
from estructuras.metodos_ordenamiento import comparar_metodos

class PruebasTab:
    """Controlador de la pestaña de Pruebas de Rendimiento"""

    def __init__(self, red_bibliotecas, on_datos_actualizados: Optional[Callable[[], None]] = None):
        self.red_bibliotecas = red_bibliotecas
        self.on_datos_actualizados = on_datos_actualizados

    def _notificar_actualizacion(self):
        if callable(self.on_datos_actualizados):
            self.on_datos_actualizados()

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

            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.lista_secuencial.buscar_por_titulo(libro_prueba.titulo)
            tiempo_secuencial = time.perf_counter() - inicio

            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.arbol_titulos.buscar(libro_prueba.titulo)
            tiempo_avl = time.perf_counter() - inicio

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
                self._notificar_actualizacion()
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
                self._notificar_actualizacion()
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
                self._notificar_actualizacion()
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando libros: {e}")


def crear_pruebas_carga_tab(notebook, red_bibliotecas, on_datos_actualizados: Optional[Callable[[], None]] = None):
    """Crear y retornar la pestaña de Pruebas de Carga"""

    tab_pruebas_carga = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_pruebas_carga, text="⚙️ Pruebas de Rendimiento y Carga (CSV)")

    tab_pruebas_carga.grid_columnconfigure((0, 1), weight=1)
    tab_pruebas_carga.grid_rowconfigure(0, weight=1)

    ctrl = PruebasTab(red_bibliotecas, on_datos_actualizados)

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

**Archivo:** red_tab.py  
**Ruta:** gui/red_tab.py  
**Tamaño:** 12004 bytes  

```py
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
            nombre = self.bib_nombre_var.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre de la biblioteca es obligatorio")
                return

            ubicacion = self.bib_ubicacion_var.get().strip() or "Sin ubicacion"
            try:
                t_ingreso = int(self.bib_tiempo_ingreso_var.get() or 10)
                t_traspaso = int(self.bib_tiempo_traspaso_var.get() or 5)
                intervalo = int(self.bib_intervalo_despacho_var.get() or 3)
            except ValueError:
                messagebox.showerror("Error", "Los tiempos deben ser numeros enteros")
                return

            if any(bib.nombre.lower() == nombre.lower() for bib in self.red_bibliotecas.bibliotecas.values()):
                messagebox.showerror("Error", "Ya existe una biblioteca con ese nombre")
                return

            # Generar ID único
            nuevo_id = f"BIB{len(self.red_bibliotecas.bibliotecas) + 1:03d}"

            self.red_bibliotecas.agregar_biblioteca(
                id_bib=nuevo_id,
                nombre=nombre,
                ubicacion=ubicacion,
                t_ingreso=t_ingreso,
                t_traspaso=t_traspaso,
                intervalo=intervalo
            )

            messagebox.showinfo("Éxito", f"Biblioteca '{nombre}' creada con ID: {nuevo_id}")

            # Limpiar campos
            self._limpiar_formulario_bib()

            # Callback para actualizar UI (se asigna desde gui_app.py)
            if hasattr(self, 'callback_actualizar'):
                self.callback_actualizar()
            if hasattr(self, "callback_dibujar"):
                self.callback_dibujar()

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear biblioteca: {e}")

    def agregar_conexion(self):
        """Agregar conexión entre bibliotecas"""
        try:
            origen = self.origen_var.get().strip()
            destino = self.destino_var.get().strip()

            if not origen or not destino:
                messagebox.showerror("Error", "Debe seleccionar origen y destino")
                return
            if origen == destino:
                messagebox.showerror("Error", "Origen y destino deben ser diferentes")
                return

            try:
                tiempo = int(self.tiempo_conexion_var.get())
                costo = float(self.costo_conexion_var.get())
            except ValueError:
                messagebox.showerror("Error", "Tiempo y costo deben ser numericos")
                return

            creada = self.red_bibliotecas.agregar_conexion(
                origen=origen,
                destino=destino,
                tiempo=tiempo,
                costo=costo,
                bidireccional=self.bidireccional_var.get()
            )

            if creada:
                messagebox.showinfo("Éxito", f"Conexión creada: {origen} -> {destino}")

                # Limpiar campos
                self.tiempo_conexion_var.set("")
                self.costo_conexion_var.set("")

                # Callback para dibujar grafo
                if hasattr(self, 'callback_dibujar'):
                    self.callback_dibujar()
            else:
                messagebox.showwarning("Advertencia", "No se pudo crear la conexion")

        except Exception as e:
            messagebox.showerror("Error", f"Error al crear conexión: {e}")

    def actualizar_comboboxes_conexiones(self, origen_combo, destino_combo):
        """Actualiza comboboxes de bibliotecas para conexiones"""
        ids = list(self.red_bibliotecas.bibliotecas.keys())

        origen_combo['values'] = ids
        destino_combo['values'] = ids

        if ids:
            if not self.origen_var.get():
                self.origen_var.set(ids[0])
            if not self.destino_var.get():
                self.destino_var.set(ids[-1])

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
    notebook.add(tab_red, text="🕸️ Gestión de la Red (Grafo)")

    tab_red.grid_columnconfigure(0, weight=1)
    tab_red.grid_columnconfigure(1, weight=3)
    tab_red.grid_rowconfigure(0, weight=1)

    # Crear controlador
    ctrl = RedTab(red_bibliotecas)

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

    tk.Label(grafo_frame, text="🕸️ RED DE BIBLIOTECAS", 
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

    def refrescar_conexiones():
        ctrl.actualizar_comboboxes_conexiones(origen_combo, destino_combo)
        ctrl.dibujar_grafo()

    ctrl.callback_actualizar = refrescar_conexiones
    ctrl.callback_dibujar = ctrl.dibujar_grafo

    return tab_red, ctrl
```

**Archivo:** simulacion_tab.py  
**Ruta:** gui/simulacion_tab.py  
**Tamaño:** 6743 bytes  

```py
"""
Pestaña Simulacion - Simulacion de colas y despacho
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from .config import *

class SimulacionTab:
    """Controlador de la pestaña de Simulacion"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.simulacion_activa = False
        self.simulacion_thread = None
        self.metricas_label = None
        self.colas_tree = None
        self.tab_root = None
        self._detener_event = threading.Event()
        self.intervalo_tick = 1.0

    def configurar_componentes(self, tab_root, metricas_label, colas_tree):
        self.tab_root = tab_root
        self.metricas_label = metricas_label
        self.colas_tree = colas_tree
        self.actualizar_estado()

    def iniciar_simulacion(self):
        """Iniciar simulacion de colas"""
        if self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulacion ya esta en ejecucion")
            return

        if not self.red_bibliotecas.bibliotecas:
            messagebox.showerror("Error", "No hay bibliotecas cargadas en la red")
            return

        self.simulacion_activa = True
        self._detener_event.clear()
        self.simulacion_thread = threading.Thread(target=self._bucle_simulacion, daemon=True)
        self.simulacion_thread.start()
        messagebox.showinfo("Simulacion", "Simulacion iniciada")
        self.actualizar_estado(texto_estado="Estado: En ejecucion")

    def pausar_simulacion(self):
        """Pausar simulacion"""
        if not self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulacion no esta en ejecucion")
            return

        self._detener_event.set()
        if self.simulacion_thread and self.simulacion_thread.is_alive():
            self.simulacion_thread.join(timeout=1.0)

        self.simulacion_activa = False
        messagebox.showinfo("Simulacion", "Simulacion pausada")
        self.actualizar_estado(texto_estado="Estado: Pausado")

    def _bucle_simulacion(self):
        """Loop en hilo de simulacion"""
        while not self._detener_event.is_set():
            inicio = time.perf_counter()
            try:
                self.red_bibliotecas.simular_tick()
            except Exception as error:
                print(f"Error en simulacion: {error}")
                self._detener_event.set()
                break

            if self.tab_root:
                self.tab_root.after(0, self.actualizar_estado)

            restante = self.intervalo_tick - (time.perf_counter() - inicio)
            if restante > 0:
                self._detener_event.wait(restante)
        self.simulacion_activa = False

    def actualizar_estado(self, texto_estado: str = None):
        """Refresca metricas y tabla de colas"""
        stats = self.red_bibliotecas.obtener_estadisticas_red()
        transferencias = stats.get("transferencias_activas", 0)
        estado = texto_estado or ("Estado: En ejecucion" if self.simulacion_activa else "Estado: Detenido")

        if self.metricas_label:
            self.metricas_label.config(
                text=f"{estado} | Transferencias activas: {transferencias} | Libros en transito: {stats.get('total_en_transito', 0)}"
            )

        if not self.colas_tree:
            return

        self.colas_tree.delete(*self.colas_tree.get_children())
        for bib_id, biblioteca in self.red_bibliotecas.bibliotecas.items():
            estado_colas = biblioteca.obtener_estado_colas()
            self.colas_tree.insert(
                "",
                "end",
                text=bib_id,
                values=(
                    biblioteca.nombre,
                    estado_colas["ingreso"]["cantidad"],
                    estado_colas["traspaso"]["cantidad"],
                    estado_colas["salida"]["cantidad"],
                    estado_colas["ingreso"]["frente"] or "-",
                    estado_colas["traspaso"]["frente"] or "-",
                    estado_colas["salida"]["frente"] or "-"
                )
            )


def crear_simulacion_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Simulacion"""

    tab_simulacion = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_simulacion, text="📦 Simulacion y Colas")

    tab_simulacion.grid_columnconfigure(0, weight=1) 
    tab_simulacion.grid_rowconfigure(2, weight=1) 

    ctrl = SimulacionTab(red_bibliotecas)

    sim_controls = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=15)
    sim_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    tk.Label(sim_controls, text="⚙️ CONTROLES DE SIMULACION", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="▶️ Iniciar", 
               command=ctrl.iniciar_simulacion).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="⏸️ Pausar", 
               command=ctrl.pausar_simulacion).pack(side='left', padx=10)

    metrics_frame = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    metrics_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

    tk.Label(metrics_frame, text="METRICAS DE DESPACHO:", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')

    metricas_label = tk.Label(metrics_frame, 
                              text="Estado: Detenido | Transferencias activas: 0", 
                              bg=FILTER_BG, fg=ACCENT_COLOR)
    metricas_label.pack(anchor='w', pady=5)

    colas_container = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    colas_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(colas_container, text="🚦 ESTADO DE COLAS POR BIBLIOTECA", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=10)

    columnas = ("nombre", "ingreso", "traspaso", "salida", "frente_ing", "frente_tra", "frente_sal")
    colas_tree = ttk.Treeview(
        colas_container,
        columns=columnas,
        show="tree headings",
        height=10
    )
    for col, texto in zip(columnas, ["Nombre", "Ingreso", "Traspaso", "Salida", "Frente ingreso", "Frente traspaso", "Frente salida"]):
        ancho = 140 if col == "nombre" else 110
        colas_tree.heading(col, text=texto)
        colas_tree.column(col, width=ancho, anchor="center")
    colas_tree.pack(fill="both", expand=True, pady=5)

    ctrl.configurar_componentes(tab_simulacion, metricas_label, colas_tree)

    return tab_simulacion, ctrl
```

**Archivo:** styles.py  
**Ruta:** gui/styles.py  
**Tamaño:** 1522 bytes  

```py
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

**Archivo:** visualizacion_tab.py  
**Ruta:** gui/visualizacion_tab.py  
**Tamaño:** 8379 bytes  

```py
"""
Pestaña Visualizacion - Representacion grafica de estructuras
"""

import os
import tempfile
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from .config import *
from objetos.biblioteca import Biblioteca

ESTRUCTURAS_DISPONIBLES = [
    ("Árbol AVL", "avl"),
    ("Árbol B", "b"),
    ("Árbol B+", "bplus"),
    ("Tabla Hash", "hash"),
    ("Grafo de la Red", "grafo"),
    ("Colas de Biblioteca (DOT)", "colas"),
]

class VisualizacionTab:
    """Controlador para la pestaña de visualizacion"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.canvas = None
        self.canvas_imagen_id = None
        self.base_image = None
        self.photo_image = None
        self.zoom_factor = 1.0
        self._drag_data = {"x": 0, "y": 0}
        self._temp_dir = None

    def configurar_canvas(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.canvas.create_text(
            self.canvas.winfo_reqwidth() // 2,
            self.canvas.winfo_reqheight() // 2,
            text="Selecciona una estructura para generar su visualización",
            font=FONT_LABEL_SMALL,
            fill=TITLE_COLOR,
        )
        self._configurar_interacciones()

    def _configurar_interacciones(self):
        if not self.canvas:
            return
        self.canvas.bind("<ButtonPress-1>", self._iniciar_arrastre)
        self.canvas.bind("<B1-Motion>", self._arrastrar)
        self.canvas.bind("<MouseWheel>", self._zoom_rodillo)          # Windows / macOS
        self.canvas.bind("<Button-4>", self._zoom_scroll_arriba)      # Linux scroll up
        self.canvas.bind("<Button-5>", self._zoom_scroll_abajo)       # Linux scroll down

    def _iniciar_arrastre(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _arrastrar(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _zoom_rodillo(self, event):
        delta = 1 if event.delta > 0 else -1
        self._aplicar_zoom(delta, event.x, event.y)

    def _zoom_scroll_arriba(self, event):
        self._aplicar_zoom(1, event.x, event.y)

    def _zoom_scroll_abajo(self, event):
        self._aplicar_zoom(-1, event.x, event.y)

    def _aplicar_zoom(self, delta: int, x: int, y: int):
        if not self.base_image:
            return
        nuevo_zoom = self.zoom_factor + (0.1 * delta)
        nuevo_zoom = max(0.2, min(nuevo_zoom, 3.0))
        if abs(nuevo_zoom - self.zoom_factor) < 1e-6:
            return
        self.zoom_factor = nuevo_zoom
        self._renderizar_imagen()
        self.canvas.scale("all", x, y, 1, 1)  # mantener posición relativa

    def _limpiar_canvas(self):
        if self.canvas:
            self.canvas.delete("all")
            self.canvas_imagen_id = None

    def _crear_directorio_temp(self):
        if self._temp_dir and os.path.exists(self._temp_dir):
            return
        self._temp_dir = tempfile.mkdtemp(prefix="viz_biblioteca_")

    def _generar_dot(self, estructura: str) -> str:
        """Genera archivo DOT temporal y retorna su ruta."""
        self._crear_directorio_temp()
        archivo_dot = os.path.join(self._temp_dir, f"{estructura}.dot")

        try:
            if estructura == "grafo":
                if not self.red_bibliotecas.grafo:
                    raise ValueError("El grafo no está inicializado")
                self.red_bibliotecas.grafo.exportar_dot(archivo_dot)
            elif estructura == "colas":
                if not self.red_bibliotecas.bibliotecas:
                    raise ValueError("No hay bibliotecas cargadas")
                biblioteca = next(iter(self.red_bibliotecas.bibliotecas.values()))
                biblioteca.exportar_colas_dot(self._temp_dir)
                # mostramos solo ingreso por defecto
                archivo_dot = os.path.join(self._temp_dir, f"{biblioteca.id}_cola_ingreso.dot")
            else:
                biblioteca = self._obtener_biblioteca_referencia()
                biblioteca.catalogo_local.exportar_estructura_dot(estructura, archivo_dot)
        except Exception as error:
            raise RuntimeError(f"No se pudo generar DOT: {error}") from error

        return archivo_dot

    def _dot_a_png(self, ruta_dot: str) -> str:
        """Convierte dot -> png usando graphviz (requiere 'dot' en PATH)."""
        ruta_png = ruta_dot.replace(".dot", ".png")
        comando = ["dot", "-Tpng", ruta_dot, "-o", ruta_png]
        try:
            subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            raise FileNotFoundError("No se encontró el comando 'dot'. Instala graphviz.")
        except subprocess.CalledProcessError as error:
            raise RuntimeError(error.stderr.decode("utf-8", errors="ignore") or str(error))
        return ruta_png

    def visualizar_estructura(self, estructura: str):
        if not self.canvas:
            return
        try:
            ruta_dot = self._generar_dot(estructura)
            ruta_png = self._dot_a_png(ruta_dot)
            self._mostrar_imagen(ruta_png)
        except FileNotFoundError as error:
            messagebox.showwarning("Graphviz", str(error))
        except RuntimeError as error:
            messagebox.showerror("Error", error)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo renderizar la estructura: {error}")

    def _mostrar_imagen(self, ruta_png: str):
        self._limpiar_canvas()
        self.base_image = Image.open(ruta_png)
        self.zoom_factor = 1.0
        self._renderizar_imagen()

        if self.canvas:
            bbox = self.canvas.bbox("all")
            if bbox:
                self.canvas.configure(scrollregion=bbox)

    def _renderizar_imagen(self):
        if not self.canvas or not self.base_image:
            return

        ancho = max(1, int(self.base_image.width * self.zoom_factor))
        alto = max(1, int(self.base_image.height * self.zoom_factor))
        imagen_redimensionada = self.base_image.resize((ancho, alto), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(imagen_redimensionada)

        self._limpiar_canvas()
        self.canvas_imagen_id = self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.photo_image,
            anchor="center",
            tags="img"
        )

    def _obtener_biblioteca_referencia(self) -> Biblioteca:
        if not self.red_bibliotecas.bibliotecas:
            raise ValueError("No hay bibliotecas registradas en la red")
        return next(iter(self.red_bibliotecas.bibliotecas.values()))

def crear_visualizacion_tab(notebook, red_bibliotecas):
    tab_visualizacion = ttk.Frame(notebook, style="Sky.TFrame")
    notebook.add(tab_visualizacion, text="📊 Visualización Estructuras")

    tk.Label(
        tab_visualizacion,
        text="🌳 REPRESENTACIÓN GRÁFICA DE ESTRUCTURAS",
        font=FONT_TITLE_LARGE,
        fg=TITLE_COLOR,
        bg=FILTER_BG,
    ).pack(pady=20)

    ctrl = VisualizacionTab(red_bibliotecas)

    vis_buttons = ttk.Frame(tab_visualizacion, style="Sky.TFrame")
    vis_buttons.pack(pady=10)

    for texto, clave in ESTRUCTURAS_DISPONIBLES:
        ttk.Button(
            vis_buttons,
            text=texto,
            command=lambda clave=clave: ctrl.visualizar_estructura(clave),
        ).pack(side="left", padx=6)

    canvas_container = tk.Frame(tab_visualizacion, bg=BG_COLOR)
    canvas_container.pack(fill="both", expand=True, padx=20, pady=10)

    vis_canvas = tk.Canvas(
        canvas_container,
        bg=DASH_CARD_BG,
        highlightthickness=1,
        highlightbackground=TITLE_COLOR,
        width=880,
        height=520,
        scrollregion=(0, 0, 880, 520)
    )
    h_scroll = ttk.Scrollbar(canvas_container, orient="horizontal", command=vis_canvas.xview)
    v_scroll = ttk.Scrollbar(canvas_container, orient="vertical", command=vis_canvas.yview)
    vis_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

    vis_canvas.pack(side="left", fill="both", expand=True)
    v_scroll.pack(side="right", fill="y")
    h_scroll.pack(side="bottom", fill="x")

    ctrl.configurar_canvas(vis_canvas)
    return tab_visualizacion, ctrl
```

---

**Archivos incluidos:** 13  
