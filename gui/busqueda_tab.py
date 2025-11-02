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
        self._on_criterio_cambiado() 
        
    def refrescar_datos(self):
        """Actualiza comboboxes después de cambios en red_bibliotecas"""
        if hasattr(self, 'ruta_origen_combo') and hasattr(self, 'ruta_destino_combo'):
            self.actualizar_comboboxes_rutas(self.ruta_origen_combo, self.ruta_destino_combo)
        self._obtener_generos_disponibles()

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