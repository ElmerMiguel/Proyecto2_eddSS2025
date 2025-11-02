"""
Pestaña Red - Gestión de bibliotecas y conexiones (Grafo)
USANDO MATPLOTLIB
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import networkx as nx # Importación necesaria para el diseño de grafos

# === NUEVAS IMPORTACIONES PARA MATPLOTLIB ===
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# ============================================

# Importaciones necesarias de tu proyecto:
from .config import * # from objetos.biblioteca import Biblioteca # Mantener si se usa, pero no es crucial para el fix.

class RedTab:
    """Controlador de la pestaña de Red de Bibliotecas"""
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        
        # --- REFERENCIAS DE MATPLOTLIB ---
        self.grafo_fig = None     # Figura de Matplotlib
        self.grafo_ax = None      # Ejes de Matplotlib
        self.grafo_canvas_mpl = None # Canvas de Tkinter para Matplotlib
        # El antiguo self.grafo_canvas (tk.Canvas) ya no se usa.
        
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

        # Cache para guardar posiciones del grafo y mantenerlas estables
        self._posiciones_grafo = {}
    
    def agregar_biblioteca(self):
        """Agregar nueva biblioteca"""
        # ... (código para agregar biblioteca, sin cambios)
        try:
            nombre = self.bib_nombre_var.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre de la biblioteca es obligatorio")
                return
            
            ubicacion = self.bib_ubicacion_var.get().strip() or "Sin ubicacion"
            try:
                t_ingreso = int(self.bib_tiempo_ingreso_var.get() or 10)
                t_traspaso = int(self.bib_tiempo_traspaso_var.get() or 5)
                intervalo = int(self.bib_intervalo_despacho_var.get() or 3)
            except ValueError:
                messagebox.showerror("Error", "Los tiempos deben ser numeros enteros")
                return

            if any(bib.nombre.lower() == nombre.lower() for bib in self.red_bibliotecas.bibliotecas.values()):
                messagebox.showerror("Error", "Ya existe una biblioteca con ese nombre")
                return
            
            # Generar ID único
            nuevo_id = f"BIB{len(self.red_bibliotecas.bibliotecas) + 1:03d}"
            
            self.red_bibliotecas.agregar_biblioteca(
                id_bib=nuevo_id,
                nombre=nombre,
                ubicacion=ubicacion,
                t_ingreso=t_ingreso,
                t_traspaso=t_traspaso,
                intervalo=intervalo
            )
            
            messagebox.showinfo("Éxito", f"Biblioteca '{nombre}' creada con ID: {nuevo_id}")
            
            # Limpiar campos
            self._limpiar_formulario_bib()
            
            # Limpiar posiciones para forzar un nuevo cálculo de layout
            self._posiciones_grafo = {} 

            if hasattr(self, 'callback_actualizar'):
                self.callback_actualizar()
            if hasattr(self, "callback_dibujar"):
                self.callback_dibujar()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear biblioteca: {e}")
    
    def agregar_conexion(self):
        """Agregar conexión entre bibliotecas"""
        # ... (código para agregar conexión, sin cambios)
        try:
            origen = self.origen_var.get().strip()
            destino = self.destino_var.get().strip()

            if not origen or not destino:
                messagebox.showerror("Error", "Debe seleccionar origen y destino")
                return
            if origen == destino:
                messagebox.showerror("Error", "Origen y destino deben ser diferentes")
                return

            try:
                tiempo = int(self.tiempo_conexion_var.get())
                costo = float(self.costo_conexion_var.get())
            except ValueError:
                messagebox.showerror("Error", "Tiempo y costo deben ser numericos")
                return
            
            # NOTA: Asumiendo que red_bibliotecas.agregar_conexion maneja la lógica
            # para actualizar el grafo interno (que es la fuente de verdad).
            creada = self.red_bibliotecas.agregar_conexion(
                origen=origen,
                destino=destino,
                tiempo=tiempo,
                costo=costo,
                bidireccional=self.bidireccional_var.get()
            )
            
            if creada:
                messagebox.showinfo("Éxito", f"Conexión creada: {origen} -> {destino}")
                
                self.tiempo_conexion_var.set("")
                self.costo_conexion_var.set("")
                
                # Limpiar posiciones para que el grafo se ajuste con la nueva conexión
                self._posiciones_grafo = {} 

                if hasattr(self, 'callback_dibujar'):
                    self.callback_dibujar()
            else:
                messagebox.showwarning("Advertencia", "No se pudo crear la conexion")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear conexión: {e}")
    
    def actualizar_comboboxes_conexiones(self, origen_combo, destino_combo):
        """Actualiza comboboxes de bibliotecas para conexiones"""
        ids = sorted(list(self.red_bibliotecas.bibliotecas.keys()))
        
        origen_combo['values'] = ids
        destino_combo['values'] = ids
        
        if ids:
            if not self.origen_var.get() or self.origen_var.get() not in ids:
                self.origen_var.set(ids[0])
            if not self.destino_var.get() or self.destino_var.get() not in ids:
                self.destino_var.set(ids[-1] if len(ids) > 1 else ids[0])
    
    
    # ---------------------------------------------------------------------
    # Lógica de dibujo con NetworkX y Matplotlib
    # ---------------------------------------------------------------------

    def _obtener_grafo_nx(self):
        """Crea un objeto nx.Graph desde la estructura de datos 'red_bibliotecas.grafo'."""
        nx_graph = nx.Graph()
        
        # 1. Agregar nodos
        for bib_id in self.red_bibliotecas.bibliotecas.keys():
            # Si el nodo no existe en el grafo, NetworkX lo agregará.
            nx_graph.add_node(bib_id)
        
        # 2. Agregar aristas y sus atributos
        for nodo_origen, aristas in self.red_bibliotecas.grafo.nodos.items():
            for arista in aristas:
                nodo_destino = arista.destino
                
                # Para un grafo NO dirigido (Graph), solo se agrega una vez (e.g., A-B)
                # La condición 'origen < destino' asegura que solo se agregue A-B y no B-A
                if nodo_origen < nodo_destino:
                    # Almacenamos tiempo y costo como atributos del borde (edge)
                    # NetworkX necesita que los atributos se pasen a add_edge
                    nx_graph.add_edge(
                        nodo_origen, 
                        nodo_destino, 
                        tiempo=arista.tiempo, 
                        costo=arista.costo
                    )
        return nx_graph
    
    def _calcular_posiciones_grafo_nx(self, nx_graph):
        """Calcula las posiciones de los nodos usando un layout de fuerza dirigida."""
        if self._posiciones_grafo:
            return self._posiciones_grafo
        
        if not nx_graph.nodes:
            return {}

        # Usa el layout de NetworkX. Recomendable usar un seed para estabilidad.
        pos = nx.spring_layout(nx_graph, seed=42, k=0.3, iterations=50) 
        
        self._posiciones_grafo = pos
        return pos


    def dibujar_grafo(self):
        """Dibuja el grafo en el FigureCanvasTkAgg usando NetworkX y Matplotlib."""
        if self.grafo_ax is None or self.grafo_canvas_mpl is None:
            return
        
        # 1. Limpiar el lienzo
        self.grafo_ax.clear()
        
        nx_graph = self._obtener_grafo_nx()
        
        if not nx_graph.nodes:
            self.grafo_ax.text(0.5, 0.5, "No hay bibliotecas para dibujar.", 
                                 horizontalalignment='center', verticalalignment='center', 
                                 transform=self.grafo_ax.transAxes, color=TITLE_COLOR)
            self.grafo_ax.axis('off')
            self.grafo_canvas_mpl.draw()
            return
        
        try:
            # 2. Calcular las posiciones (usa la caché si ya existe)
            posiciones = self._calcular_posiciones_grafo_nx(nx_graph)
        except Exception as e:
            self.grafo_ax.text(0.5, 0.5, f"Error al calcular layout: {e}", 
                                 horizontalalignment='center', verticalalignment='center', 
                                 transform=self.grafo_ax.transAxes, color='red')
            self.grafo_ax.axis('off')
            self.grafo_canvas_mpl.draw()
            return


        # 3. Dibujar componentes del grafo
        
        # Nodos
        nx.draw_networkx_nodes(
            nx_graph, 
            posiciones, 
            ax=self.grafo_ax, 
            node_size=800, # Aumentado para mejor visualización
            node_color=BUTTON_COLOR, 
            edgecolors=TITLE_COLOR,
            linewidths=2
        )
        
        # Aristas
        nx.draw_networkx_edges(
            nx_graph, 
            posiciones, 
            ax=self.grafo_ax, 
            edge_color=ACCENT_COLOR, 
            width=2
        )
        
        # Etiquetas de Nodos (IDs de biblioteca)
        node_labels = {node_id: node_id for node_id in nx_graph.nodes()}
        nx.draw_networkx_labels(
            nx_graph, 
            posiciones, 
            labels=node_labels, 
            ax=self.grafo_ax, 
            font_size=10, 
            font_color="white", 
            font_weight='bold'
        )
        
        # Etiquetas de Aristas (Tiempo y Costo)
        edge_labels = {
            (u, v): f"T:{data['tiempo']} C:{data['costo']:.1f}" 
            for u, v, data in nx_graph.edges(data=True)
        }
        nx.draw_networkx_edge_labels(
            nx_graph, 
            posiciones, 
            edge_labels=edge_labels, 
            ax=self.grafo_ax, 
            font_color=TITLE_COLOR, 
            font_size=8,
            bbox={"alpha": 0.5, "facecolor": DASH_CARD_BG, "edgecolor": "none"} # Fondo para que el texto resalte
        )
        
        # 4. Configurar y renderizar
        self.grafo_ax.set_title("RED DE BIBLIOTECAS (NetworkX/Matplotlib)", color=ACCENT_COLOR)
        self.grafo_ax.axis('off') # Ocultar los ejes de coordenadas de Matplotlib
        self.grafo_fig.set_facecolor(FILTER_BG) # Color de fondo de la figura (ajustar si es necesario)
        
        self.grafo_canvas_mpl.draw() # Renderizar el gráfico en el canvas de Tkinter

    
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
    notebook.add(tab_red, text="🕸️ Gestión de la Red (Grafo)")
    
    tab_red.grid_columnconfigure(0, weight=1)
    tab_red.grid_columnconfigure(1, weight=3)
    tab_red.grid_rowconfigure(0, weight=1)
    
    # Crear controlador
    ctrl = RedTab(red_bibliotecas)
    
    # === FRAME CONFIGURACIÓN (Lado Izquierdo) ===
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
    
    # === FRAME GRAFO (Lado Derecho) ===
    grafo_frame = ttk.Frame(tab_red, style='Sky.TFrame', padding=10)
    grafo_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    # --- Título ---
    tk.Label(grafo_frame, text="🕸️ RED DE BIBLIOTECAS (Fuerza Dirigida)", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    # --- CREACIÓN DEL CANVAS DE MATPLOTLIB ---
    
    # 1. Crear Figura de Matplotlib (donde se dibuja)
    # Establecemos un DPI más bajo, Matplotlib se escalará al tamaño del frame.
    ctrl.grafo_fig = Figure(dpi=100) 
    ctrl.grafo_ax = ctrl.grafo_fig.add_subplot(111) # Añadir los ejes
    
    # 2. Crear el canvas de Tkinter a partir de la Figura
    ctrl.grafo_canvas_mpl = FigureCanvasTkAgg(ctrl.grafo_fig, master=grafo_frame)
    canvas_widget = ctrl.grafo_canvas_mpl.get_tk_widget()
    
    # Reemplazamos el antiguo tk.Canvas por el widget de Matplotlib
    canvas_widget.pack(fill='both', expand=True, pady=5)
    
    # NOTA: En Matplotlib, el evento de 'Configure' ya no es necesario para redibujar 
    # debido a que Matplotlib maneja mejor el redimensionamiento.
    
    # ----------------------------------------------------------------------
    
    # Actualizar comboboxes y dibujar
    ctrl.actualizar_comboboxes_conexiones(origen_combo, destino_combo)

    def refrescar_conexiones():
        # Limpiar cache de posiciones cuando se refrescan los datos
        ctrl._posiciones_grafo = {}
        ctrl.actualizar_comboboxes_conexiones(origen_combo, destino_combo)
        ctrl.dibujar_grafo()

    ctrl.callback_actualizar = refrescar_conexiones
    ctrl.callback_dibujar = ctrl.dibujar_grafo
    
    # Dibujar por primera vez al cargar la pestaña
    ctrl.dibujar_grafo() 
    
    return tab_red, ctrl