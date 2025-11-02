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
    
    crear_tarjeta_info(tab_dashboard, "🗺️", "Rutas Optimas", 
                       "Algoritmos: Dijkstra", 0, 2, ACCENT_COLOR, 3)
    
    crear_tarjeta_info(tab_dashboard, "⏳", "Simulación de Flujo", 
                       "Algoritmos: Colas FIFO (Ingreso, Traspaso, Salida)", 1, 0, ACCENT_COLOR, 4)
    
    crear_tarjeta_info(tab_dashboard, "🌳", "Visualización Estructuras", 
                       "Representación: Árboles / Hash / Pilas", 1, 1, ACCENT_COLOR, 5)
    
    crear_tarjeta_info(tab_dashboard, "📈", "Pruebas y Carga CSV", 
                       "Comparación: 5 Sorts / 3 Búsquedas (Big O)", 1, 2, ACCENT_COLOR, 6)
    
    return tab_dashboard