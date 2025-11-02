"""
Pestaña Simulacion - Simulacion de colas y despacho
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from .config import *

class SimulacionTab:
    """Controlador de la pestaña de Simulacion"""
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.simulacion_activa = False
        self.simulacion_thread = None
        self.metricas_label = None
        self.colas_tree = None
        self.tab_root = None
        self._detener_event = threading.Event()
        self.intervalo_tick = 1.0
    
    def configurar_componentes(self, tab_root, metricas_label, colas_tree):
        self.tab_root = tab_root
        self.metricas_label = metricas_label
        self.colas_tree = colas_tree
        self.actualizar_estado()

    def iniciar_simulacion(self):
        """Iniciar simulacion de colas"""
        if self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulacion ya esta en ejecucion")
            return
        
        if not self.red_bibliotecas.bibliotecas:
            messagebox.showerror("Error", "No hay bibliotecas cargadas en la red")
            return
        
        self.simulacion_activa = True
        self._detener_event.clear()
        self.simulacion_thread = threading.Thread(target=self._bucle_simulacion, daemon=True)
        self.simulacion_thread.start()
        messagebox.showinfo("Simulacion", "Simulacion iniciada")
        self.actualizar_estado(texto_estado="Estado: En ejecucion")

    def pausar_simulacion(self):
        """Pausar simulacion"""
        if not self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulacion no esta en ejecucion")
            return
        
        self._detener_event.set()
        if self.simulacion_thread and self.simulacion_thread.is_alive():
            self.simulacion_thread.join(timeout=1.0)
        
        self.simulacion_activa = False
        messagebox.showinfo("Simulacion", "Simulacion pausada")
        self.actualizar_estado(texto_estado="Estado: Pausado")

    def _bucle_simulacion(self):
        """Loop en hilo de simulacion"""
        while not self._detener_event.is_set():
            inicio = time.perf_counter()
            try:
                self.red_bibliotecas.simular_tick()
            except Exception as error:
                print(f"Error en simulacion: {error}")
                self._detener_event.set()
                break
            
            if self.tab_root:
                self.tab_root.after(0, self.actualizar_estado)
            
            restante = self.intervalo_tick - (time.perf_counter() - inicio)
            if restante > 0:
                self._detener_event.wait(restante)
        self.simulacion_activa = False

    def actualizar_estado(self, texto_estado: str = None):
        """Refresca metricas y tabla de colas"""
        stats = self.red_bibliotecas.obtener_estadisticas_red()
        transferencias = stats.get("transferencias_activas", 0)
        estado = texto_estado or ("Estado: En ejecucion" if self.simulacion_activa else "Estado: Detenido")
        
        if self.metricas_label:
            self.metricas_label.config(
                text=f"{estado} | Transferencias activas: {transferencias} | Libros en transito: {stats.get('total_en_transito', 0)}"
            )
        
        if not self.colas_tree:
            return
        
        self.colas_tree.delete(*self.colas_tree.get_children())
        for bib_id, biblioteca in self.red_bibliotecas.bibliotecas.items():
            estado_colas = biblioteca.obtener_estado_colas()
            self.colas_tree.insert(
                "",
                "end",
                text=bib_id,
                values=(
                    biblioteca.nombre,
                    estado_colas["ingreso"]["cantidad"],
                    estado_colas["traspaso"]["cantidad"],
                    estado_colas["salida"]["cantidad"],
                    estado_colas["ingreso"]["frente"] or "-",
                    estado_colas["traspaso"]["frente"] or "-",
                    estado_colas["salida"]["frente"] or "-"
                )
            )


def crear_simulacion_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Simulacion"""
    
    tab_simulacion = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_simulacion, text="📦 Simulacion y Colas")
    
    tab_simulacion.grid_columnconfigure(0, weight=1) 
    tab_simulacion.grid_rowconfigure(2, weight=1) 
    
    ctrl = SimulacionTab(red_bibliotecas)
    
    sim_controls = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=15)
    sim_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    
    tk.Label(sim_controls, text="⚙️ CONTROLES DE SIMULACION", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="▶️ Iniciar", 
               command=ctrl.iniciar_simulacion).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="⏸️ Pausar", 
               command=ctrl.pausar_simulacion).pack(side='left', padx=10)
    
    metrics_frame = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    metrics_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    
    tk.Label(metrics_frame, text="METRICAS DE DESPACHO:", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')
    
    metricas_label = tk.Label(metrics_frame, 
                              text="Estado: Detenido | Transferencias activas: 0", 
                              bg=FILTER_BG, fg=ACCENT_COLOR)
    metricas_label.pack(anchor='w', pady=5)
    
    colas_container = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    colas_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    
    tk.Label(colas_container, text="🚦 ESTADO DE COLAS POR BIBLIOTECA", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=10)
    
    columnas = ("nombre", "ingreso", "traspaso", "salida", "frente_ing", "frente_tra", "frente_sal")
    colas_tree = ttk.Treeview(
        colas_container,
        columns=columnas,
        show="tree headings",
        height=10
    )
    for col, texto in zip(columnas, ["Nombre", "Ingreso", "Traspaso", "Salida", "Frente ingreso", "Frente traspaso", "Frente salida"]):
        ancho = 140 if col == "nombre" else 110
        colas_tree.heading(col, text=texto)
        colas_tree.column(col, width=ancho, anchor="center")
    colas_tree.pack(fill="both", expand=True, pady=5)
    
    ctrl.configurar_componentes(tab_simulacion, metricas_label, colas_tree)
    
    return tab_simulacion, ctrl