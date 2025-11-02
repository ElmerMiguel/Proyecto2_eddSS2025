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