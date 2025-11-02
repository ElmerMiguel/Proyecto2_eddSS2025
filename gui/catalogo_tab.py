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
    
    def configurar_comboboxes(self, combo_origen: ttk.Combobox, combo_destino: ttk.Combobox):
        self.combo_origen = combo_origen
        self.combo_destino = combo_destino
        self.actualizar_comboboxes_origen_destino(combo_origen, combo_destino)
    
    def refrescar_datos(self):
        self.actualizar_catalogo_tree()
        if self.combo_origen and self.combo_destino:
            self.actualizar_comboboxes_origen_destino(self.combo_origen, self.combo_destino)
    
    def actualizar_catalogo_tree(self):
        """Actualiza el TreeView con libros del catálogo"""
        if not self.catalog_tree:
            return
        
        self.catalog_tree.delete(*self.catalog_tree.get_children())
        
        total_libros = 0
        for biblioteca_id, biblioteca in self.red_bibliotecas.bibliotecas.items():
            try:
                libros = biblioteca.catalogo_local.lista_secuencial.mostrar_todos() or []
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
    
    ctrl = CatalogoTab(red_bibliotecas)
    
    crud_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    crud_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
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
    
    listado_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    listado_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    listado_frame.grid_rowconfigure(2, weight=1)
    
    tk.Label(listado_frame, text="📖 LISTADO Y ALMACENAMIENTO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    ttk.Button(listado_frame, text="🔄 Actualizar Catálogo", 
               command=ctrl.refrescar_datos).pack(fill='x', pady=5)
    
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
    
    ctrl.configurar_comboboxes(biblioteca_origen_combo, biblioteca_destino_combo)
    
    return tab_catalogo, ctrl