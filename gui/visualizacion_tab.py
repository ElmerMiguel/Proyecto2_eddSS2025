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