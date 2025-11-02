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