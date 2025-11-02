"""
Pestaña de Rutas Óptimas
"""

import tkinter as tk
from tkinter import ttk, messagebox
# Importaciones requeridas de tu estructura
from gui.config import TITLE_COLOR, FILTER_BG, FONT_TITLE_MEDIUM, ACCENT_COLOR, DASH_CARD_BG 
# Se asume que estos objetos/métodos existen en el ámbito de tu proyecto.

class BusquedaTab:
    """Controlador de la pestaña de Rutas"""
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.ruta_resultado_label = None
        
        # Variables de entrada de Ruta
        self.ruta_origen_var = tk.StringVar()
        self.ruta_destino_var = tk.StringVar()
        self.criterio_var = tk.StringVar(value="tiempo")
        
        # Almacenamiento de Comboboxes de Ruta
        self.ruta_origen_combo: ttk.Combobox | None = None
        self.ruta_destino_combo: ttk.Combobox | None = None
    
    def actualizar_comboboxes_rutas(self, origen_combo, destino_combo):
        """Actualiza comboboxes de bibliotecas para rutas"""
        bibliotecas_ids = list(self.red_bibliotecas.bibliotecas.keys())
        
        if bibliotecas_ids:
            origen_combo['values'] = bibliotecas_ids
            destino_combo['values'] = bibliotecas_ids
            
            # Asignar un valor inicial
            if not self.ruta_origen_var.get() and bibliotecas_ids:
                 self.ruta_origen_var.set(bibliotecas_ids[0])
            if not self.ruta_destino_var.get() and len(bibliotecas_ids) > 1:
                 # Seleccionar una biblioteca diferente para el destino si es posible
                 self.ruta_destino_var.set(bibliotecas_ids[1])

    def refrescar_datos(self):
        """Actualiza comboboxes después de cambios en red_bibliotecas"""
        if self.ruta_origen_combo and self.ruta_destino_combo:
            self.actualizar_comboboxes_rutas(self.ruta_origen_combo, self.ruta_destino_combo)

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
            # Asumiendo que self.red_bibliotecas.grafo existe y tiene los métodos dijkstra_tiempo/dijkstra_costo
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
    """Crear y retornar la pestaña de Rutas Óptimas"""
    
    tab_busqueda_rutas = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_busqueda_rutas, text="🗺️ Rutas Óptimas") 
    
    # Grid principal: 1 columna, 2 filas. Fila 0 para el formulario de ruta, Fila 1 para la visualización.
    tab_busqueda_rutas.grid_columnconfigure(0, weight=1)
    tab_busqueda_rutas.grid_rowconfigure(1, weight=1)
    
    ctrl = BusquedaTab(red_bibliotecas)
    
    # === FRAME RUTAS (OPTIMIZADO CON GRID) ===
    rutas_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
    # Ubicación: Fila 0, Columna 0. 
    rutas_frame.grid(row=0, column=0, sticky="new", padx=10, pady=10)
    rutas_frame.grid_columnconfigure((0, 1), weight=1) # Dos columnas para campos

    
    tk.Label(rutas_frame, text="🗺️ CÁLCULO DE RUTA ÓPTIMA", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky='w')
    
    current_row = 1
    
    # Biblioteca Origen
    tk.Label(rutas_frame, text="Biblioteca Origen:", bg=FILTER_BG).grid(row=current_row, column=0, sticky='w', padx=5, pady=2)
    ruta_origen_combo = ttk.Combobox(rutas_frame, textvariable=ctrl.ruta_origen_var, state="readonly")
    ruta_origen_combo.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
    current_row += 1
    
    # Biblioteca Destino
    tk.Label(rutas_frame, text="Biblioteca Destino:", bg=FILTER_BG).grid(row=current_row, column=0, sticky='w', padx=5, pady=2)
    ruta_destino_combo = ttk.Combobox(rutas_frame, textvariable=ctrl.ruta_destino_var, state="readonly")
    ruta_destino_combo.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
    current_row += 1
    
    # Criterio de Optimización
    tk.Label(rutas_frame, text="Criterio:", bg=FILTER_BG).grid(row=current_row, column=0, sticky='w', padx=5, pady=2)
    criterio_options = ttk.Frame(rutas_frame, style='Sky.TFrame')
    criterio_options.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
    ttk.Radiobutton(criterio_options, text="Tiempo", 
                    variable=ctrl.criterio_var, value="tiempo").pack(side='left', padx=5)
    ttk.Radiobutton(criterio_options, text="Costo", 
                    variable=ctrl.criterio_var, value="costo").pack(side='left', padx=5)
    current_row += 1
    
    # Botón Calcular
    ttk.Button(rutas_frame, text="🧮 Calcular Ruta Óptima", 
               command=ctrl.calcular_ruta_optima).grid(row=current_row, column=0, columnspan=2, pady=(15, 5), sticky='ew', padx=5)
    current_row += 1
    
    # Etiqueta de Resultado
    ctrl.ruta_resultado_label = tk.Label(rutas_frame, text="Ruta: [No calculada]", 
                                         bg=FILTER_BG, fg=ACCENT_COLOR)
    ctrl.ruta_resultado_label.grid(row=current_row, column=0, columnspan=2, sticky='w', padx=5, pady=5)
    current_row += 1
    
    # === FRAME VISUALIZACIÓN RUTAS ===
    results_busqueda_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=10)
    results_busqueda_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    tk.Label(results_busqueda_frame, text="VISUALIZACIÓN DE RUTA (Grafo)", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    ruta_canvas = tk.Canvas(results_busqueda_frame, bg=DASH_CARD_BG, 
                           highlightthickness=1, highlightbackground=TITLE_COLOR)
    ruta_canvas.pack(fill='both', expand=True)
    
    # Almacenar referencias para refrescar_datos()
    ctrl.ruta_origen_combo = ruta_origen_combo
    ctrl.ruta_destino_combo = ruta_destino_combo

    # Actualizar comboboxes de ruta
    ctrl.actualizar_comboboxes_rutas(ruta_origen_combo, ruta_destino_combo)
    
    return tab_busqueda_rutas, ctrl