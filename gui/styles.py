"""
Configuración de estilos ttk para la GUI
"""

from tkinter import ttk
from .config import *

def configurar_estilos(root):
    """Configura todos los estilos ttk de la aplicación"""
    
    style = ttk.Style(root)
    style.theme_use(THEME)
    
    # === NOTEBOOK (Pestañas) ===
    style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
    
    style.configure('TNotebook.Tab', 
                    font=FONT_BUTTON, 
                    foreground='white',
                    background=BUTTON_COLOR,
                    bordercolor=BG_COLOR,
                    padding=[15, 5])

    style.map('TNotebook.Tab', 
              background=[('selected', ACCENT_COLOR), ('active', BUTTON_COLOR)],
              foreground=[('selected', 'white')],
              bordercolor=[('selected', FILTER_BG)])

    # === FRAMES ===
    style.configure('Sky.TFrame', background=FILTER_BG)
    
    # === LABELS ===
    style.configure('TLabel', background=FILTER_BG)
    
    # === CHECKBUTTON y RADIOBUTTON ===
    style.configure('TCheckbutton', background=FILTER_BG, foreground=TITLE_COLOR)
    style.configure('TRadiobutton', background=FILTER_BG, foreground=TITLE_COLOR)
    
    # === BUTTONS ===
    style.configure('TButton', 
                    font=FONT_BUTTON, 
                    foreground='white', 
                    background=BUTTON_COLOR, 
                    padding=6, 
                    relief='flat')
    style.map('TButton', background=[('active', ACCENT_COLOR)])
    
    return style