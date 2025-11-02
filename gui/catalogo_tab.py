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
            isbn = str(item['values'][2])
            
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
                    resultado_libros = catalogo.buscar_por_rango_fechas(inicio, fin)
                    for libro in resultado_libros:
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