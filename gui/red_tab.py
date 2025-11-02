"""
Pestaña Red - Gestión de bibliotecas y conexiones (Grafo)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
from .config import *
from objetos.biblioteca import Biblioteca

class RedTab:
    """Controlador de la pestaña de Red de Bibliotecas"""
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.grafo_canvas = None
        
        # Variables de entrada
        self.bib_nombre_var = tk.StringVar()
        self.bib_ubicacion_var = tk.StringVar()
        self.bib_tiempo_ingreso_var = tk.StringVar(value="10")
        self.bib_tiempo_traspaso_var = tk.StringVar(value="5")
        self.bib_intervalo_despacho_var = tk.StringVar(value="3")
        
        self.origen_var = tk.StringVar()
        self.destino_var = tk.StringVar()
        self.tiempo_conexion_var = tk.StringVar()
        self.costo_conexion_var = tk.StringVar()
        self.bidireccional_var = tk.BooleanVar(value=True)
    
    def agregar_biblioteca(self):
        """Agregar nueva biblioteca"""
        try:
            nombre = self.bib_nombre_var.get()
            if not nombre:
                messagebox.showerror("Error", "El nombre de la biblioteca es obligatorio")
                return
            
            # Generar ID único
            bib_id = f"BIB{len(self.red_bibliotecas.bibliotecas) + 1:03d}"
            
            biblioteca = Biblioteca(
                id_biblioteca=bib_id,
                nombre=nombre,
                ubicacion=self.bib_ubicacion_var.get() or "Sin ubicación",
                tiempo_ingreso=int(self.bib_tiempo_ingreso_var.get()) if self.bib_tiempo_ingreso_var.get() else 10,
                tiempo_traspaso=int(self.bib_tiempo_traspaso_var.get()) if self.bib_tiempo_traspaso_var.get() else 5,
                intervalo_despacho=int(self.bib_intervalo_despacho_var.get()) if self.bib_intervalo_despacho_var.get() else 3
            )
            
            self.red_bibliotecas.bibliotecas[bib_id] = biblioteca
            self.red_bibliotecas.grafo.agregar_nodo(bib_id, nombre)
            
            messagebox.showinfo("Éxito", f"Biblioteca '{nombre}' creada con ID: {bib_id}")
            
            # Limpiar campos
            self._limpiar_formulario_bib()
            
            # Callback para actualizar UI (se asigna desde gui_app.py)
            if hasattr(self, 'callback_actualizar'):
                self.callback_actualizar()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear biblioteca: {e}")
    
    def agregar_conexion(self):
        """Agregar conexión entre bibliotecas"""
        try:
            origen = self.origen_var.get()
            destino = self.destino_var.get()
            tiempo = self.tiempo_conexion_var.get()
            costo = self.costo_conexion_var.get()
            
            if not all([origen, destino, tiempo, costo]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            self.red_bibliotecas.grafo.agregar_arista(
                origen=origen,
                destino=destino,
                tiempo=int(tiempo),
                costo=float(costo),
                bidireccional=self.bidireccional_var.get()
            )
            
            messagebox.showinfo("Éxito", f"Conexión creada: {origen} -> {destino}")
            
            # Limpiar campos
            self.tiempo_conexion_var.set("")
            self.costo_conexion_var.set("")
            
            # Callback para dibujar grafo
            if hasattr(self, 'callback_dibujar'):
                self.callback_dibujar()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear conexión: {e}")
    
    def actualizar_comboboxes_conexiones(self, origen_combo, destino_combo):
        """Actualiza comboboxes de bibliotecas para conexiones"""
        bibliotecas_ids = list(self.red_bibliotecas.bibliotecas.keys())
        
        if bibliotecas_ids:
            origen_combo['values'] = bibliotecas_ids
            destino_combo['values'] = bibliotecas_ids
    
    def dibujar_grafo(self):
        """Dibujar grafo en el canvas"""
        if self.grafo_canvas is None:
            return
        
        self.grafo_canvas.delete("all")
        
        if not self.red_bibliotecas.grafo.nodos:
            return
        
        # Obtener dimensiones del canvas
        width = self.grafo_canvas.winfo_width() or 400
        height = self.grafo_canvas.winfo_height() or 300
        
        nodos = list(self.red_bibliotecas.grafo.nodos.keys())
        n = len(nodos)
        
        if n == 0:
            return
        
        posiciones = {}
        
        # Distribuir nodos en círculo
        for i, nodo in enumerate(nodos):
            angle = 2 * math.pi * i / n
            x = width // 2 + (width // 3) * math.cos(angle)
            y = height // 2 + (height // 3) * math.sin(angle)
            posiciones[nodo] = (x, y)
        
        # Dibujar aristas
        for nodo_origen, aristas in self.red_bibliotecas.grafo.nodos.items():
            if nodo_origen in posiciones:
                x1, y1 = posiciones[nodo_origen]
                for arista in aristas:
                    if arista.destino in posiciones:
                        x2, y2 = posiciones[arista.destino]
                        self.grafo_canvas.create_line(x1, y1, x2, y2, 
                                                     fill=ACCENT_COLOR, width=2)
                        
                        # Etiqueta de peso
                        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                        self.grafo_canvas.create_text(mx, my, text=f"{arista.tiempo}",
                                                     fill="red", font=('Arial', 8, 'bold'))
        
        # Dibujar nodos
        for nodo, (x, y) in posiciones.items():
            self.grafo_canvas.create_oval(x-20, y-20, x+20, y+20, 
                                        fill=BUTTON_COLOR, outline=TITLE_COLOR, width=2)
            self.grafo_canvas.create_text(x, y, text=nodo, fill="white", 
                                        font=('Arial', 8, 'bold'))
    
    def _limpiar_formulario_bib(self):
        """Limpia formulario de bibliotecas"""
        self.bib_nombre_var.set("")
        self.bib_ubicacion_var.set("")
        self.bib_tiempo_ingreso_var.set("10")
        self.bib_tiempo_traspaso_var.set("5")
        self.bib_intervalo_despacho_var.set("3")


def crear_red_tab(notebook, red_bibliotecas, callback_actualizar=None, callback_dibujar=None):
    """Crear y retornar la pestaña de Red"""
    
    tab_red = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_red, text="🌐 Gestión de la Red (Grafo)")
    
    tab_red.grid_columnconfigure(0, weight=1)
    tab_red.grid_columnconfigure(1, weight=3)
    tab_red.grid_rowconfigure(0, weight=1)
    
    # Crear controlador
    ctrl = RedTab(red_bibliotecas)
    if callback_actualizar:
        ctrl.callback_actualizar = callback_actualizar
    if callback_dibujar:
        ctrl.callback_dibujar = callback_dibujar
    
    # === FRAME CONFIGURACIÓN ===
    config_frame_red = ttk.Frame(tab_red, style='Sky.TFrame', padding=15)
    config_frame_red.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    # --- GESTIÓN DE BIBLIOTECAS ---
    tk.Label(config_frame_red, text="🏛️ GESTIÓN DE BIBLIOTECAS", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    tk.Label(config_frame_red, text="Nombre:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_nombre_var, width=30).pack(fill='x')
    
    tk.Label(config_frame_red, text="Ubicación:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_ubicacion_var, width=30).pack(fill='x')
    
    tk.Label(config_frame_red, text="Tiempo Ingreso (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_tiempo_ingreso_var, width=15).pack(fill='x')
    
    tk.Label(config_frame_red, text="Tiempo Traspaso (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_tiempo_traspaso_var, width=15).pack(fill='x')
    
    tk.Label(config_frame_red, text="Intervalo Despacho (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.bib_intervalo_despacho_var, width=15).pack(fill='x')
    
    ttk.Button(config_frame_red, text="➕ Crear Biblioteca", 
               command=ctrl.agregar_biblioteca).pack(pady=(15, 5), fill='x')
    
    # --- GESTIÓN DE CONEXIONES ---
    tk.Label(config_frame_red, text="🔗 GESTIÓN DE CONEXIONES", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(20, 10))
    
    tk.Label(config_frame_red, text="Origen:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    origen_combo = ttk.Combobox(config_frame_red, textvariable=ctrl.origen_var)
    origen_combo.pack(fill='x')
    
    tk.Label(config_frame_red, text="Destino:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    destino_combo = ttk.Combobox(config_frame_red, textvariable=ctrl.destino_var)
    destino_combo.pack(fill='x')
    
    tk.Label(config_frame_red, text="Tiempo:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.tiempo_conexion_var).pack(fill='x')
    
    tk.Label(config_frame_red, text="Costo:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=ctrl.costo_conexion_var).pack(fill='x')
    
    ttk.Checkbutton(config_frame_red, text="Conexión Bidireccional", 
                    variable=ctrl.bidireccional_var).pack(anchor='w', pady=5)
    
    ttk.Button(config_frame_red, text="🔗 Crear Conexión", 
               command=ctrl.agregar_conexion).pack(pady=10, fill='x')
    
    # === FRAME GRAFO ===
    grafo_frame = ttk.Frame(tab_red, style='Sky.TFrame', padding=10)
    grafo_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    tk.Label(grafo_frame, text="🌍 RED DE BIBLIOTECAS", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    ctrl.grafo_canvas = tk.Canvas(grafo_frame, bg=DASH_CARD_BG, 
                                  highlightthickness=1, highlightbackground=TITLE_COLOR)
    ctrl.grafo_canvas.pack(fill='both', expand=True, pady=5)
    
    # Evento de redimensionado
    def on_canvas_configure(event):
        if event.widget == ctrl.grafo_canvas:
            tk.Tk.after(tab_red, 100, ctrl.dibujar_grafo)
    
    ctrl.grafo_canvas.bind('<Configure>', on_canvas_configure)
    
    # Actualizar comboboxes y dibujar
    ctrl.actualizar_comboboxes_conexiones(origen_combo, destino_combo)
    
    return tab_red, ctrl