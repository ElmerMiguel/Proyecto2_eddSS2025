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
    
    title = tk.Label(root, text="✨ Sistema de Gestión BibMagic ✨", 
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
        if ctrl_busqueda and hasattr(ctrl_busqueda, "refrescar_datos"):
            ctrl_busqueda.refrescar_datos()
    
    ctrl_pruebas.on_datos_actualizados = actualizar_ui
    
    actualizar_ui()
    
    root.mainloop()

if __name__ == "__main__":
    iniciar_gui()