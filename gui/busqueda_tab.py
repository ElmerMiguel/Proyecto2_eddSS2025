import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx 
import math

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors

# Importaciones requeridas de tu estructura (asumidas disponibles)
from gui.config import TITLE_COLOR, FILTER_BG, FONT_TITLE_MEDIUM, ACCENT_COLOR, DASH_CARD_BG 


class BusquedaTab:
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.ruta_resultado_label = None
        
        self.ruta_fig = None        # Figura de Matplotlib
        self.ruta_ax = None         # Ejes de Matplotlib
        self.ruta_canvas_mpl = None # Canvas de Tkinter para Matplotlib

        # Variables de entrada de Ruta
        self.ruta_origen_var = tk.StringVar()
        self.ruta_destino_var = tk.StringVar()
        self.criterio_var = tk.StringVar(value="tiempo")
        
        # Almacenamiento de Comboboxes de Ruta
        self.ruta_origen_combo: ttk.Combobox | None = None
        self.ruta_destino_combo: ttk.Combobox | None = None
        
        # Almacenar posiciones calculadas para reutilizar
        self._posiciones_grafo = {}
        
        # Almacenar la última ruta calculada para redibujar
        self._ultima_ruta = None 
    
    def actualizar_comboboxes_rutas(self, origen_combo, destino_combo):
        bibliotecas_ids = sorted(list(self.red_bibliotecas.bibliotecas.keys()))
        
        if bibliotecas_ids:
            origen_combo['values'] = bibliotecas_ids
            destino_combo['values'] = bibliotecas_ids
            
            if not self.ruta_origen_var.get() and bibliotecas_ids:
                 self.ruta_origen_var.set(bibliotecas_ids[0])
            if not self.ruta_destino_var.get() and len(bibliotecas_ids) > 1:
                 self.ruta_destino_var.set(bibliotecas_ids[1] if len(bibliotecas_ids) > 1 else bibliotecas_ids[0])

    def refrescar_datos(self):
        if self.ruta_origen_combo and self.ruta_destino_combo:
            self.actualizar_comboboxes_rutas(self.ruta_origen_combo, self.ruta_destino_combo)
        
        self._posiciones_grafo = {} 
        self._ultima_ruta = None 
        
        if self.ruta_canvas_mpl:
            self.dibujar_grafo_con_ruta() 

    def calcular_ruta_optima(self):
        origen = self.ruta_origen_var.get()
        destino = self.ruta_destino_var.get()
        
        if not origen or not destino:
            messagebox.showerror("Error", "Seleccione bibliotecas de origen y destino")
            return
        
        if origen == destino:
            messagebox.showerror("Error", "Origen y destino deben ser diferentes")
            return
        
        try:
            if self.criterio_var.get() == "tiempo":
                peso, ruta = self.red_bibliotecas.grafo.dijkstra_tiempo(origen, destino)
            else:
                peso, ruta = self.red_bibliotecas.grafo.dijkstra_costo(origen, destino)
            
            if ruta:
                self._ultima_ruta = ruta 
                
                ruta_texto = " -> ".join(ruta)
                peso_formateado = f"{peso:.2f}" if self.criterio_var.get() == "costo" else str(peso)
                
                messagebox.showinfo("Ruta Calculada", f"Ruta óptima ({self.criterio_var.get()}):\n{ruta_texto}\nPeso total: {peso_formateado}")
                
                if self.ruta_resultado_label:
                    self.ruta_resultado_label.config(text=f"Ruta: {ruta_texto} | Peso: {peso_formateado} ({self.criterio_var.get().capitalize()})")
                
                self.dibujar_grafo_con_ruta(ruta)
            else:
                messagebox.showerror("Error", "No se encontró ruta entre las bibliotecas")
                self._ultima_ruta = None
                self.dibujar_grafo_con_ruta()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error calculando ruta: {e}")

    def _obtener_grafo_nx(self):
        nx_graph = nx.Graph()
        
        for bib_id in self.red_bibliotecas.bibliotecas.keys():
            nx_graph.add_node(bib_id)
        
        for nodo_origen, aristas in self.red_bibliotecas.grafo.nodos.items():
            for arista in aristas:
                nodo_destino = arista.destino
                
                if nodo_origen < nodo_destino:
                    nx_graph.add_edge(
                        nodo_origen, 
                        nodo_destino, 
                        tiempo=arista.tiempo, 
                        costo=arista.costo
                    )
        return nx_graph
    
    def _calcular_posiciones_grafo_nx(self, nx_graph):
        if self._posiciones_grafo:
            return self._posiciones_grafo
        
        if not nx_graph.nodes:
            return {}

        pos = nx.spring_layout(nx_graph, seed=42, k=0.3, iterations=50) 
        
        self._posiciones_grafo = pos
        return pos

    def dibujar_grafo_con_ruta(self, ruta_destacada=None):
        if self.ruta_ax is None or self.ruta_canvas_mpl is None:
            return
        
        ruta_destacada = ruta_destacada if ruta_destacada is not None else self._ultima_ruta
        
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
            posiciones = self._calcular_posiciones_grafo_nx(nx_graph)
        except Exception as e:
            self.ruta_ax.text(0.5, 0.5, f"Error: {e}\n(Verifique instalación)", 
                                 horizontalalignment='center', verticalalignment='center', 
                                 transform=self.ruta_ax.transAxes, color='red')
            self.ruta_ax.axis('off')
            self.ruta_canvas_mpl.draw()
            return

        
        node_colors = ['lightblue'] * len(nx_graph.nodes)
        node_sizes = [800] * len(nx_graph.nodes)
        
        edge_colors = ['gray'] * len(nx_graph.edges)
        edge_widths = [2] * len(nx_graph.edges)
        
        if ruta_destacada and len(ruta_destacada) > 1:
            
            node_map = {node: i for i, node in enumerate(nx_graph.nodes)}
            
            if ruta_destacada[0] in node_map:
                 node_colors[node_map[ruta_destacada[0]]] = 'green'
            if ruta_destacada[-1] in node_map:
                 node_colors[node_map[ruta_destacada[-1]]] = 'orange'
            for node in ruta_destacada[1:-1]:
                 if node in node_map:
                     node_colors[node_map[node]] = 'yellow'

            edge_list = list(nx_graph.edges)
            
            for i in range(len(ruta_destacada) - 1):
                n1, n2 = ruta_destacada[i], ruta_destacada[i+1]
                
                arista_ruta = tuple(sorted((n1, n2)))
                
                try:
                    idx = edge_list.index(arista_ruta)
                    edge_colors[idx] = ACCENT_COLOR 
                    edge_widths[idx] = 4             
                except ValueError:
                    arista_ruta_rev = tuple(sorted((n2, n1)))
                    try:
                        idx = edge_list.index(arista_ruta_rev)
                        edge_colors[idx] = ACCENT_COLOR
                        edge_widths[idx] = 4
                    except:
                        pass 

        
        nx.draw_networkx_nodes(
            nx_graph, 
            posiciones, 
            ax=self.ruta_ax, 
            node_size=node_sizes,
            node_color=node_colors, 
            edgecolors='black',
            linewidths=2
        )
        
        nx.draw_networkx_edges(
            nx_graph, 
            posiciones, 
            ax=self.ruta_ax, 
            edge_color=edge_colors, 
            width=edge_widths
        )
        
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
        
        self.ruta_ax.set_title("VISUALIZACIÓN DE RUTA (NetworkX/Matplotlib)", color=TITLE_COLOR)
        self.ruta_ax.axis('off') 
        self.ruta_fig.set_facecolor(FILTER_BG)
        
        self.ruta_canvas_mpl.draw()


def crear_busqueda_rutas_tab(notebook, red_bibliotecas):
    
    tab_busqueda_rutas = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_busqueda_rutas, text="🗺️ Rutas Óptimas") 
    
    tab_busqueda_rutas.grid_columnconfigure(0, weight=1)
    tab_busqueda_rutas.grid_rowconfigure(1, weight=1)
    
    ctrl = BusquedaTab(red_bibliotecas)
    
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
    
    ttk.Button(rutas_frame, text="🔄 Refrescar Red", 
            command=ctrl.refrescar_datos).grid(row=current_row, column=0, columnspan=2, pady=5, sticky='ew', padx=5)
    current_row += 1

    ctrl.ruta_resultado_label = tk.Label(rutas_frame, text="Ruta: [No calculada]", 
                                         bg=FILTER_BG, fg=ACCENT_COLOR)
    ctrl.ruta_resultado_label.grid(row=current_row, column=0, columnspan=2, sticky='w', padx=5, pady=5)
    current_row += 1
    
    results_busqueda_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=10)
    results_busqueda_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    results_busqueda_frame.grid_columnconfigure(0, weight=1)
    results_busqueda_frame.grid_rowconfigure(1, weight=1)
    
    tk.Label(results_busqueda_frame, text="VISUALIZACIÓN DE RUTA (Grafo de Fuerza Dirigida)", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).grid(row=0, column=0, sticky='n')
    
    ctrl.ruta_fig = Figure(dpi=100) 
    ctrl.ruta_ax = ctrl.ruta_fig.add_subplot(111)
    
    ctrl.ruta_canvas_mpl = FigureCanvasTkAgg(ctrl.ruta_fig, master=results_busqueda_frame)
    canvas_widget = ctrl.ruta_canvas_mpl.get_tk_widget()
    
    canvas_widget.grid(row=1, column=0, sticky='nsew')
    
    ctrl.ruta_origen_combo = ruta_origen_combo
    ctrl.ruta_destino_combo = ruta_destino_combo

    ctrl.actualizar_comboboxes_rutas(ruta_origen_combo, ruta_destino_combo)

    ctrl.dibujar_grafo_con_ruta()
    
    return tab_busqueda_rutas, ctrl