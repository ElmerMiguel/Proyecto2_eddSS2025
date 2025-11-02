"""
Pestaña Rutas - Cálculo y Visualización (Grafo)
USANDO MATPLOTLIB
"""
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx 
import math

# === NUEVAS IMPORTACIONES PARA MATPLOTLIB ===
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
# ============================================

# Importaciones requeridas de tu estructura (asumidas disponibles)
# NOTA: Asegúrate de que gui.config esté disponible o reemplaza los colores por strings.
from gui.config import TITLE_COLOR, FILTER_BG, FONT_TITLE_MEDIUM, ACCENT_COLOR, DASH_CARD_BG 


class BusquedaTab:
    """Controlador de la pestaña de Rutas"""
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.ruta_resultado_label = None
        
        # --- REFERENCIAS DE MATPLOTLIB ---
        self.ruta_fig = None        # Figura de Matplotlib
        self.ruta_ax = None         # Ejes de Matplotlib
        self.ruta_canvas_mpl = None # Canvas de Tkinter para Matplotlib
        # El antiguo self.ruta_canvas (tk.Canvas) ya no se usa.

        # Variables de entrada de Ruta
        self.ruta_origen_var = tk.StringVar()
        self.ruta_destino_var = tk.StringVar()
        self.criterio_var = tk.StringVar(value="tiempo")
        
        # Almacenamiento de Comboboxes de Ruta
        self.ruta_origen_combo: ttk.Combobox | None = None
        self.ruta_destino_combo: ttk.Combobox | None = None
        
        # Almacenar posiciones calculadas para reutilizar (mejora la consistencia)
        self._posiciones_grafo = {}
        
        # Almacenar la última ruta calculada para redibujar
        self._ultima_ruta = None 
    
    def actualizar_comboboxes_rutas(self, origen_combo, destino_combo):
        """Actualiza comboboxes de bibliotecas para rutas"""
        bibliotecas_ids = sorted(list(self.red_bibliotecas.bibliotecas.keys()))
        
        if bibliotecas_ids:
            origen_combo['values'] = bibliotecas_ids
            destino_combo['values'] = bibliotecas_ids
            
            if not self.ruta_origen_var.get() and bibliotecas_ids:
                 self.ruta_origen_var.set(bibliotecas_ids[0])
            if not self.ruta_destino_var.get() and len(bibliotecas_ids) > 1:
                 self.ruta_destino_var.set(bibliotecas_ids[1] if len(bibliotecas_ids) > 1 else bibliotecas_ids[0])

    def refrescar_datos(self):
        """Actualiza comboboxes y redibuja grafo después de cambios"""
        if self.ruta_origen_combo and self.ruta_destino_combo:
            self.actualizar_comboboxes_rutas(self.ruta_origen_combo, self.ruta_destino_combo)
        
        # Limpiar posiciones almacenadas para recalcular el layout si la red cambió
        self._posiciones_grafo = {} 
        self._ultima_ruta = None # También limpiar la ruta destacada
        
        if self.ruta_canvas_mpl:
            # Llama al nuevo método con Matplotlib
            self.dibujar_grafo_con_ruta() 

    def calcular_ruta_optima(self):
        """Calcular ruta óptima entre bibliotecas CON VISUALIZACIÓN"""
        origen = self.ruta_origen_var.get()
        destino = self.ruta_destino_var.get()
        
        if not origen or not destino:
            messagebox.showerror("Error", "Seleccione bibliotecas de origen y destino")
            return
        
        if origen == destino:
            messagebox.showerror("Error", "Origen y destino deben ser diferentes")
            return
        
        try:
            # Calcular ruta óptima
            if self.criterio_var.get() == "tiempo":
                peso, ruta = self.red_bibliotecas.grafo.dijkstra_tiempo(origen, destino)
            else:
                peso, ruta = self.red_bibliotecas.grafo.dijkstra_costo(origen, destino)
            
            if ruta:
                self._ultima_ruta = ruta # Almacenar la ruta para redibujar
                
                ruta_texto = " -> ".join(ruta)
                # Nota: Formatear peso a 2 decimales si costo es el criterio
                peso_formateado = f"{peso:.2f}" if self.criterio_var.get() == "costo" else str(peso)
                
                messagebox.showinfo("Ruta Calculada", f"Ruta óptima ({self.criterio_var.get()}):\n{ruta_texto}\nPeso total: {peso_formateado}")
                
                if self.ruta_resultado_label:
                    self.ruta_resultado_label.config(text=f"Ruta: {ruta_texto} | Peso: {peso_formateado} ({self.criterio_var.get().capitalize()})")
                
                # Llamar al nuevo método de dibujo
                self.dibujar_grafo_con_ruta(ruta)
            else:
                messagebox.showerror("Error", "No se encontró ruta entre las bibliotecas")
                self._ultima_ruta = None
                self.dibujar_grafo_con_ruta()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error calculando ruta: {e}")

    def _obtener_grafo_nx(self):
        """Crea un objeto nx.Graph desde la estructura de datos 'red_bibliotecas.grafo'."""
        nx_graph = nx.Graph()
        
        # 1. Agregar nodos
        for bib_id in self.red_bibliotecas.bibliotecas.keys():
            nx_graph.add_node(bib_id)
        
        # 2. Agregar aristas y sus atributos
        for nodo_origen, aristas in self.red_bibliotecas.grafo.nodos.items():
            for arista in aristas:
                nodo_destino = arista.destino
                
                # Asumiendo grafo no dirigido para NetworkX para el layout
                if nodo_origen < nodo_destino:
                    # Almacenamos tiempo y costo como atributos del borde (edge)
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

    def dibujar_grafo_con_ruta(self, ruta_destacada=None):
        """Dibuja el grafo de bibliotecas con ruta destacada usando Matplotlib."""
        if self.ruta_ax is None or self.ruta_canvas_mpl is None:
            return
        
        ruta_destacada = ruta_destacada if ruta_destacada is not None else self._ultima_ruta
        
        # 1. Limpiar el lienzo
        self.ruta_ax.clear()
        
        nx_graph = self._obtener_grafo_nx()
        
        if not nx_graph.nodes:
            self.ruta_ax.text(0.5, 0.5, "No hay bibliotecas cargadas.", 
                                 horizontalalignment='center', verticalalignment='center', 
                                 transform=self.ruta_ax.transAxes, color=TITLE_COLOR)
            self.ruta_ax.axis('off')
            self.ruta_canvas_mpl.draw()
            return
        
        try:
            # 2. Calcular/Obtener posiciones
            posiciones = self._calcular_posiciones_grafo_nx(nx_graph)
        except Exception as e:
            self.ruta_ax.text(0.5, 0.5, f"Error: {e}\n(Verifique instalación)", 
                                 horizontalalignment='center', verticalalignment='center', 
                                 transform=self.ruta_ax.transAxes, color='red')
            self.ruta_ax.axis('off')
            self.ruta_canvas_mpl.draw()
            return

        # 3. Preparar estilos para el dibujo
        
        # Estilos de Nodos
        node_colors = ['lightblue'] * len(nx_graph.nodes)
        node_sizes = [800] * len(nx_graph.nodes)
        
        # Estilos de Aristas
        edge_colors = ['gray'] * len(nx_graph.edges)
        edge_widths = [2] * len(nx_graph.edges)
        
        if ruta_destacada and len(ruta_destacada) > 1:
            
            # Colores de los nodos de la ruta
            node_map = {node: i for i, node in enumerate(nx_graph.nodes)}
            
            # Origen (verde)
            if ruta_destacada[0] in node_map:
                 node_colors[node_map[ruta_destacada[0]]] = 'green'
            # Destino (naranja)
            if ruta_destacada[-1] in node_map:
                 node_colors[node_map[ruta_destacada[-1]]] = 'orange'
            # Nodos intermedios (amarillo)
            for node in ruta_destacada[1:-1]:
                 if node in node_map:
                     node_colors[node_map[node]] = 'yellow'

            # Colores de las aristas de la ruta
            edge_list = list(nx_graph.edges)
            
            for i in range(len(ruta_destacada) - 1):
                n1, n2 = ruta_destacada[i], ruta_destacada[i+1]
                
                # NetworkX almacena las aristas ordenadas, por lo que usamos tuple(sorted)
                arista_ruta = tuple(sorted((n1, n2)))
                
                try:
                    # Encontrar el índice de la arista en la lista de aristas de NetworkX
                    idx = edge_list.index(arista_ruta)
                    edge_colors[idx] = ACCENT_COLOR # Color destacado
                    edge_widths[idx] = 4             # Grosor destacado
                except ValueError:
                    # Si el NetworkX.Graph es simétrico, puede que la arista esté en el orden inverso
                    arista_ruta_rev = tuple(sorted((n2, n1)))
                    try:
                        idx = edge_list.index(arista_ruta_rev)
                        edge_colors[idx] = ACCENT_COLOR
                        edge_widths[idx] = 4
                    except:
                        pass # Arista no encontrada

        # 4. Dibujar componentes del grafo
        
        # Nodos
        nx.draw_networkx_nodes(
            nx_graph, 
            posiciones, 
            ax=self.ruta_ax, 
            node_size=node_sizes,
            node_color=node_colors, 
            edgecolors='black',
            linewidths=2
        )
        
        # Aristas
        nx.draw_networkx_edges(
            nx_graph, 
            posiciones, 
            ax=self.ruta_ax, 
            edge_color=edge_colors, 
            width=edge_widths
        )
        
        # Etiquetas de Nodos (IDs de biblioteca)
        node_labels = {node_id: node_id for node_id in nx_graph.nodes()}
        nx.draw_networkx_labels(
            nx_graph, 
            posiciones, 
            labels=node_labels, 
            ax=self.ruta_ax, 
            font_size=10, 
            font_color="black", 
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
            ax=self.ruta_ax, 
            font_color='dimgray',
            font_size=8,
            bbox={"alpha": 0.5, "facecolor": DASH_CARD_BG, "edgecolor": "none"}
        )
        
        # 5. Configurar y renderizar
        self.ruta_ax.set_title("VISUALIZACIÓN DE RUTA (NetworkX/Matplotlib)", color=TITLE_COLOR)
        self.ruta_ax.axis('off') # Ocultar ejes de coordenadas
        self.ruta_fig.set_facecolor(FILTER_BG)
        
        self.ruta_canvas_mpl.draw()


def crear_busqueda_rutas_tab(notebook, red_bibliotecas):
    """Crear y retornar la pestaña de Rutas Óptimas"""
    
    tab_busqueda_rutas = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_busqueda_rutas, text="🗺️ Rutas Óptimas") 
    
    tab_busqueda_rutas.grid_columnconfigure(0, weight=1)
    tab_busqueda_rutas.grid_rowconfigure(1, weight=1)
    
    ctrl = BusquedaTab(red_bibliotecas)
    
    # === FRAME RUTAS (Controles) ===
    rutas_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
    rutas_frame.grid(row=0, column=0, sticky="new", padx=10, pady=10)
    rutas_frame.grid_columnconfigure((0, 1), weight=1)

    
    tk.Label(rutas_frame, text="🗺️ CÁLCULO DE RUTA ÓPTIMA", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky='w')
    
    current_row = 1
    
    tk.Label(rutas_frame, text="Biblioteca Origen:", bg=FILTER_BG).grid(row=current_row, column=0, sticky='w', padx=5, pady=2)
    ruta_origen_combo = ttk.Combobox(rutas_frame, textvariable=ctrl.ruta_origen_var, state="readonly")
    ruta_origen_combo.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
    current_row += 1
    
    tk.Label(rutas_frame, text="Biblioteca Destino:", bg=FILTER_BG).grid(row=current_row, column=0, sticky='w', padx=5, pady=2)
    ruta_destino_combo = ttk.Combobox(rutas_frame, textvariable=ctrl.ruta_destino_var, state="readonly")
    ruta_destino_combo.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
    current_row += 1
    
    tk.Label(rutas_frame, text="Criterio:", bg=FILTER_BG).grid(row=current_row, column=0, sticky='w', padx=5, pady=2)
    criterio_options = ttk.Frame(rutas_frame, style='Sky.TFrame')
    criterio_options.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
    ttk.Radiobutton(criterio_options, text="Tiempo", variable=ctrl.criterio_var, value="tiempo").pack(side='left', padx=5)
    ttk.Radiobutton(criterio_options, text="Costo", variable=ctrl.criterio_var, value="costo").pack(side='left', padx=5)
    current_row += 1
    
    ttk.Button(rutas_frame, text="🧮 Calcular Ruta Óptima", 
               command=ctrl.calcular_ruta_optima).grid(row=current_row, column=0, columnspan=2, pady=(15, 5), sticky='ew', padx=5)
    current_row += 1
    
    ctrl.ruta_resultado_label = tk.Label(rutas_frame, text="Ruta: [No calculada]", 
                                         bg=FILTER_BG, fg=ACCENT_COLOR)
    ctrl.ruta_resultado_label.grid(row=current_row, column=0, columnspan=2, sticky='w', padx=5, pady=5)
    current_row += 1
    
    # === FRAME VISUALIZACIÓN RUTAS (Canvas de Matplotlib) ===
    results_busqueda_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=10)
    results_busqueda_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    results_busqueda_frame.grid_columnconfigure(0, weight=1)
    results_busqueda_frame.grid_rowconfigure(1, weight=1)
    
    tk.Label(results_busqueda_frame, text="VISUALIZACIÓN DE RUTA (Grafo de Fuerza Dirigida)", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).grid(row=0, column=0, sticky='n')
    
    # --- CREACIÓN DEL CANVAS DE MATPLOTLIB ---
    ctrl.ruta_fig = Figure(dpi=100) 
    ctrl.ruta_ax = ctrl.ruta_fig.add_subplot(111)
    
    ctrl.ruta_canvas_mpl = FigureCanvasTkAgg(ctrl.ruta_fig, master=results_busqueda_frame)
    canvas_widget = ctrl.ruta_canvas_mpl.get_tk_widget()
    
    # Reemplazamos el antiguo tk.Canvas por el widget de Matplotlib
    canvas_widget.grid(row=1, column=0, sticky='nsew')
    # ----------------------------------------
    
    # Guardar referencias
    ctrl.ruta_origen_combo = ruta_origen_combo
    ctrl.ruta_destino_combo = ruta_destino_combo

    ctrl.actualizar_comboboxes_rutas(ruta_origen_combo, ruta_destino_combo)

    # Dibuja el grafo la primera vez (se redibujará con la ruta al calcular)
    ctrl.dibujar_grafo_con_ruta()
    
    return tab_busqueda_rutas, ctrl