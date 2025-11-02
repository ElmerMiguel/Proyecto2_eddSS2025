"""
Pestaña Catálogo - CRUD de libros y gestión de catálogo
"""

import tkinter as tk
from tkinter import ttk, messagebox
# Importaciones requeridas de tu estructura
from gui.config import TITLE_COLOR, FILTER_BG, FONT_TITLE_SMALL, FONT_TITLE_MEDIUM, FONT_LABEL_SMALL
from objetos.libro import Libro
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
        
        # Búsqueda y ordenamiento
        self.search_text_var = tk.StringVar()
        self.search_aux_var = tk.StringVar()
        self.criterio_busqueda_var = tk.StringVar(value="Título (AVL)")
        self.campo_orden_var = tk.StringVar(value="titulo")
        self.algoritmo_orden_var = tk.StringVar(value="QuickSort")
        self.resumen_var = tk.StringVar(value="0 libros en catálogo")
        self.search_aux_entry = None
        
        self._metodos_orden = {
            "Burbuja": burbuja,
            "Selección": seleccion,
            "Insercion": insercion,
            "Shell Sort": shell_sort,
            "QuickSort": quick_sort,
        }
    
    # -----------------------------------------------------
    # MÉTODOS DEL CONTROLADOR (SIN CAMBIOS EN LA LÓGICA)
    # -----------------------------------------------------
    
    def configurar_comboboxes(self, combo_origen: ttk.Combobox, combo_destino: ttk.Combobox):
        self.combo_origen = combo_origen
        self.combo_destino = combo_destino
        self.actualizar_comboboxes_origen_destino(combo_origen, combo_destino)
    
    def refrescar_datos(self):
        self.actualizar_catalogo_tree()
        if self.combo_origen and self.combo_destino:
            self.actualizar_comboboxes_origen_destino(self.combo_origen, self.combo_destino)
        self._actualizar_generos()

    def actualizar_catalogo_tree(self):
        """Actualiza el TreeView con libros del catálogo, aplicando filtros y ordenamiento."""
        if not self.catalog_tree:
            return
        
        libros = self._obtener_libros_filtrados()
        self.catalog_tree.delete(*self.catalog_tree.get_children())
        
        for libro, biblioteca_id in libros:
            self.catalog_tree.insert("", "end", values=(
                libro.titulo, 
                libro.autor, 
                libro.isbn, 
                libro.estado, 
                biblioteca_id,
                libro.anio,
                libro.genero,
            ))
            
        self.resumen_var.set(f"{len(libros)} libros en catálogo")
    
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

            biblioteca_origen.agregar_libro_catalogo(libro)

            bib_destino_id = libro.biblioteca_destino
            if bib_destino_id and bib_destino_id != bib_origen_id:
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
            resultado = biblioteca.rollback_ultima_operacion()  # Cambiar de rollback_ultimo_ingreso()

            if resultado and not resultado.startswith("No hay"):
                messagebox.showinfo("Éxito", resultado)
                self.refrescar_datos()
            else:
                messagebox.showwarning("Advertencia", resultado or "No hay operaciones para deshacer")
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
        self.search_text_var.set("")
        self.search_aux_var.set("")
        self.resumen_var.set("0 libros en catálogo")

    def _actualizar_generos(self):
        """Recopila y actualiza la lista de géneros únicos disponibles."""
        generos = set()
        for biblioteca in self.red_bibliotecas.bibliotecas.values():
            try:
                generos.update(biblioteca.catalogo_local.obtener_generos_unicos())
            except Exception:
                continue
        sorted(generos)

    def _obtener_libros_filtrados(self):
        """
        Recopila, filtra (usando la estructura de datos apropiada) y ordena
        la lista total de libros. Retorna: Lista de (Libro, ID_Biblioteca)
        """
        libros = []
        criterio = self.criterio_busqueda_var.get()
        texto = self.search_text_var.get().strip()
        auxiliar = self.search_aux_var.get().strip()
        
        # 1. Recopilar y Filtrar libros (Simplificado para el ejemplo)
        for biblioteca_id, biblioteca in self.red_bibliotecas.bibliotecas.items():
            catalogo = biblioteca.catalogo_local
            try:
                # Simulación de mostrar todos si no hay búsqueda
                if not texto or criterio == "Rango de Fechas (B)":
                    # Usar el método correcto de tu estructura: catalogo.lista_secuencial.mostrar_todos()
                    libros_en_catalogo = catalogo.lista_secuencial.mostrar_todos() if hasattr(catalogo, 'lista_secuencial') else []
                    for libro in libros_en_catalogo or []:
                        libros.append((libro, biblioteca_id))
                    continue

                # Búsqueda usando las estructuras correspondientes (asumiendo que los métodos existen)
                if criterio == "Título (AVL)":
                    libro = catalogo.buscar_por_titulo(texto)
                    if libro: libros.append((libro, biblioteca_id))
                        
                elif criterio == "ISBN (Hash)":
                    libro = catalogo.buscar_por_isbn(texto)
                    if libro: libros.append((libro, biblioteca_id))
                        
                elif criterio == "Género (B+)":
                    for libro in catalogo.buscar_por_genero(texto):
                        libros.append((libro, biblioteca_id))

            except Exception as e:
                print(f"Error al buscar/filtrar en {biblioteca_id}: {e}")
                continue
        
        # 2. Ordenar libros
        metodo = self._metodos_orden.get(self.algoritmo_orden_var.get(), quick_sort)
        campo = self.campo_orden_var.get()

        if libros:
            solo_libros = [libro for libro, _ in libros]
            ordenados = metodo(solo_libros, campo)
            
            # Re-asociar los libros ordenados con sus IDs de biblioteca
            libros_map = {original[0].isbn: original for original in libros}
            ordenados_con_bib = []
            
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
# Funciones de creación de la UI (Optimización UX/UI aplicada aquí)
# ----------------------------------------------------------------------

def crear_catalogo_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Catálogo con un diseño mejorado."""
    
    tab_catalogo = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_catalogo, text="📚 Catálogo y Libro (CRUD)")
    
    # Grid principal (3 filas: Filtros, CRUD, Listado)
    # Columna 0 (CRUD) se hace de tamaño fijo. Columna 1 (Listado) toma el resto del espacio.
    tab_catalogo.grid_columnconfigure(0, weight=0, uniform="cols") 
    tab_catalogo.grid_columnconfigure(1, weight=1, uniform="cols") 
    tab_catalogo.grid_rowconfigure(1, weight=1) 
    
    ctrl = CatalogoTab(red_bibliotecas)
    
    # --- 1. BARRA DE FILTROS Y ORDENAMIENTO (SIN CAMBIOS) ---
    filtros_frame = ttk.Frame(tab_catalogo, style="Sky.TFrame", padding=10)
    filtros_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
    filtros_frame.grid_columnconfigure(1, weight=1)

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
        values=[ "Título (AVL)", "ISBN (Hash)", "Género (B+)", "Rango de Fechas (B)", ],
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

    # Controles de Ordenamiento
    tk.Label( filtros_frame, text="Ordenar por:", bg=FILTER_BG, ).grid(row=2, column=0, sticky="w", pady=(10, 5))
    ttk.Combobox( filtros_frame, textvariable=ctrl.campo_orden_var, values=["titulo", "autor", "anio"], state="readonly", width=12, ).grid(row=2, column=1, padx=3, pady=(10, 5), sticky="w")
    ttk.Combobox( filtros_frame, textvariable=ctrl.algoritmo_orden_var, values=list(ctrl._metodos_orden.keys()), state="readonly", width=14, ).grid(row=2, column=2, padx=3, pady=(10, 5), sticky="w")
    ttk.Button( filtros_frame, text="Aplicar Ordenamiento", command=ctrl.actualizar_catalogo_tree, ).grid(row=2, column=3, padx=3, pady=(10, 5), sticky="w")

    # Resumen de libros
    ttk.Label( filtros_frame, textvariable=ctrl.resumen_var, font=FONT_LABEL_SMALL, background=FILTER_BG, ).grid(row=2, column=4, padx=6, pady=(10, 5), sticky="e")

    ctrl.criterio_busqueda_var.trace_add("write", ctrl._on_criterio_cambiado)
    
    # --- 2. CRUD y Control de Pilas (OPTIMIZADO CON GRID) ---
    crud_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    # sticky="nsw" asegura que se pegue arriba, a la izquierda y no intente expandirse
    crud_frame.grid(row=1, column=0, sticky="nsw", padx=10, pady=10) 
    
    tk.Label(crud_frame, text="✏️ REGISTRO DE LIBRO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")
    
    # Configuración del grid interno para el formulario (2 columnas)
    crud_frame.grid_columnconfigure(0, weight=1)
    crud_frame.grid_columnconfigure(1, weight=1)

    # Contador de filas para la sección CRUD
    current_row = 1 
    
    # Función auxiliar para añadir campos en el grid de dos columnas
    def add_field_to_grid(parent, label_text, textvariable, is_combo=False, values=None):
        nonlocal current_row
        tk.Label(parent, text=label_text, bg=FILTER_BG).grid(row=current_row, column=0, sticky='w', padx=5, pady=2)
        if is_combo:
            widget = ttk.Combobox(parent, textvariable=textvariable, values=values, state="readonly")
        else:
            widget = ttk.Entry(parent, textvariable=textvariable)
        widget.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
        current_row += 1
        return widget

    # Creación de campos
    add_field_to_grid(crud_frame, "Título:", ctrl.titulo_var)
    add_field_to_grid(crud_frame, "Autor:", ctrl.autor_var)
    add_field_to_grid(crud_frame, "ISBN:", ctrl.isbn_var)
    add_field_to_grid(crud_frame, "Año:", ctrl.anio_var)
    add_field_to_grid(crud_frame, "Género:", ctrl.genero_var)
    
    add_field_to_grid(crud_frame, "Estado:", ctrl.estado_var, is_combo=True, 
                      values=["disponible", "prestado", "en_transito", "agotado"])
    
    biblioteca_origen_combo = add_field_to_grid(crud_frame, "Bib. Origen:", ctrl.biblioteca_origen_var, is_combo=True)
    biblioteca_destino_combo = add_field_to_grid(crud_frame, "Bib. Destino:", ctrl.biblioteca_destino_var, is_combo=True)
    
    # Prioridad de Envío (manteniendo el diseño horizontal)
    tk.Label(crud_frame, text="Prioridad:", bg=FILTER_BG).grid(row=current_row, column=0, sticky='w', padx=5, pady=2)
    prioridad_frame = ttk.Frame(crud_frame)
    prioridad_frame.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
    ttk.Radiobutton(prioridad_frame, text="Tiempo", 
                    variable=ctrl.prioridad_var, value="tiempo").pack(side='left', padx=10)
    ttk.Radiobutton(prioridad_frame, text="Costo", 
                    variable=ctrl.prioridad_var, value="costo").pack(side='left', padx=10)
    current_row += 1

    # Botones CRUD (Abarcan dos columnas)
    ttk.Button(crud_frame, text="➕ Agregar Libro", 
               command=ctrl.agregar_libro).grid(row=current_row, column=0, columnspan=2, pady=(20, 5), sticky='ew', padx=5)
    current_row += 1

    ttk.Button(crud_frame, text="🗑️ Eliminar Libro", 
               command=ctrl.eliminar_libro).grid(row=current_row, column=0, columnspan=2, pady=5, sticky='ew', padx=5)
    current_row += 1

    # CONTROL DE PILAS
    tk.Label(crud_frame, text="🔄 CONTROL DE PILAS", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).grid(row=current_row, column=0, columnspan=2, pady=(20, 10), sticky='w')
    current_row += 1
    
    ttk.Button(crud_frame, text="↩️ Deshacer Última Operación", 
               command=ctrl.rollback_operacion).grid(row=current_row, column=0, columnspan=2, pady=5, sticky='ew', padx=5)
    current_row += 1
    
    # --- 3. LISTADO (Treeview) ---
    listado_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    # sticky="nsew" asegura que se pegue a todas las esquinas y se expanda
    listado_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10) 
    listado_frame.grid_rowconfigure(2, weight=1) # Permite que el Treeview se estire verticalmente
    listado_frame.grid_columnconfigure(0, weight=1) # Permite que el Treeview se estire horizontalmente

    tk.Label(listado_frame, text="📖 LISTADO Y ALMACENAMIENTO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).grid(row=0, column=0, sticky="w", pady=(0, 10))
    
    ttk.Button(listado_frame, text="🔄 Actualizar Catálogo", 
               command=ctrl.refrescar_datos).grid(row=1, column=0, sticky="ew", pady=5)
    
    # Contenedor para Treeview y Scrollbar
    tree_container = ttk.Frame(listado_frame)
    tree_container.grid(row=2, column=0, columnspan=2, sticky='nsew', pady=(5, 0))
    tree_container.grid_columnconfigure(0, weight=1)
    tree_container.grid_rowconfigure(0, weight=1)

    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
    
    # Columnas del Treeview Actualizadas
    ctrl.catalog_tree = ttk.Treeview(
        tree_container, 
        columns=("Título", "Autor", "ISBN", "Estado", "Biblioteca", "Año", "Género"), 
        show='headings',
        yscrollcommand=scrollbar.set # Conectar scrollbar
    )
    
    scrollbar.config(command=ctrl.catalog_tree.yview) # Conectar scrollbar
    
    # Configuración de headings y columnas (el Treeview necesita ser parte del grid del contenedor)
    for col in ("Título", "Autor", "ISBN", "Estado", "Biblioteca", "Año", "Género"):
        ctrl.catalog_tree.heading(col, text=col)
        ctrl.catalog_tree.column(col, anchor='center', width=50) # El width es inicial, se ajusta al expandir

    ctrl.catalog_tree.grid(row=0, column=0, sticky='nsew')
    scrollbar.grid(row=0, column=1, sticky='ns')

    
    # Configuración final
    ctrl.configurar_comboboxes(biblioteca_origen_combo, biblioteca_destino_combo)
    ctrl._on_criterio_cambiado()
    ctrl.refrescar_datos()
    
    return tab_catalogo, ctrl