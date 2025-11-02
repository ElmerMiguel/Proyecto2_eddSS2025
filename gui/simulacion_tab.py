"""
Pestaña Simulación - Simulación de colas y despacho
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from .config import *

class SimulacionTab:
    """Controlador de la pestaña de Simulación"""
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.simulacion_activa = False
        self.simulacion_thread = None
        self.metricas_label = None
    
    def iniciar_simulacion(self):
        """Iniciar simulación de colas"""
        if self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulación ya está en ejecución")
            return
        
        self.simulacion_activa = True
        messagebox.showinfo("Simulación", "Simulación iniciada")
        
        # Aquí implementarías la lógica de simulación en tiempo real
        # Por ahora es un placeholder
        if self.metricas_label:
            self.metricas_label.config(text="Estado: En ejecución | Transferencias activas: 0")
    
    def pausar_simulacion(self):
        """Pausar simulación"""
        if not self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulación no está en ejecución")
            return
        
        self.simulacion_activa = False
        messagebox.showinfo("Simulación", "Simulación pausada")
        
        if self.metricas_label:
            self.metricas_label.config(text="Estado: Pausado | Transferencias activas: 0")


def crear_simulacion_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Simulación"""
    
    tab_simulacion = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_simulacion, text="📦 Simulación y Colas")
    
    tab_simulacion.grid_columnconfigure(0, weight=1) 
    tab_simulacion.grid_rowconfigure(2, weight=1) 
    
    # Crear controlador
    ctrl = SimulacionTab(red_bibliotecas)
    
    # === FRAME CONTROLES ===
    sim_controls = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=15)
    sim_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    
    tk.Label(sim_controls, text="⚙️ CONTROLES DE SIMULACIÓN", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="▶️ Iniciar", 
               command=ctrl.iniciar_simulacion).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="⏸️ Pausar", 
               command=ctrl.pausar_simulacion).pack(side='left', padx=10)
    
    # === FRAME MÉTRICAS ===
    metrics_frame = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    metrics_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    
    tk.Label(metrics_frame, text="MÉTRICAS DE DESPACHO:", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')
    
    ctrl.metricas_label = tk.Label(metrics_frame, 
                                   text="Estado: Detenido | Transferencias activas: 0", 
                                   bg=FILTER_BG, fg=ACCENT_COLOR)
    ctrl.metricas_label.pack(anchor='w', pady=5)
    
    # === FRAME COLAS ===
    colas_container = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    colas_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    
    tk.Label(colas_container, text="🚦 ESTADO DE COLAS POR BIBLIOTECA", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=10)
    
    tk.Label(colas_container, 
             text="[Las colas se mostrarán cuando se carguen bibliotecas y se inicie la simulación]", 
             font=FONT_LABEL, pady=20, bg=FILTER_BG).pack(fill='x')
    
    return tab_simulacion, ctrl