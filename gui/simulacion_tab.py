"""
Pestaña Simulacion - Simulacion de colas y despacho con visualización Matplotlib
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import numpy as np
import networkx as nx
import math

# === IMPORTACIONES PARA MATPLOTLIB ===
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Asume que 'config' es un módulo que contiene variables como FONT_TITLE_LARGE, ACCENT_COLOR, etc.
from .config import *

# === DEFINICIÓN DE COLORES DEL GRAFO (COPIADOS DE dibuja_grafo_colas) ===
COLOR_INGRESO = '#4CAF50'  # Verde
COLOR_TRASPASO = '#FF9800' # Naranja
COLOR_SALIDA = '#F44336'   # Rojo

COLOR_INACTIVO = '#E0E0E0' # Gris claro
COLOR_BAJA = '#81C784'     # Verde claro (Baja Actividad)
COLOR_MEDIA = '#FFB74D'    # Naranja claro (Media Actividad)
COLOR_ALTA = '#F06292'     # Rosa (Alta Actividad)

class SimulacionTab:
    """Controlador de la pestaña de Simulación"""
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.simulacion_activa = False
        self.simulacion_thread = None
        self.metricas_label = None
        self.colas_tree = None
        self.tab_root = None
        self._detener_event = threading.Event()
        self.intervalo_tick = 1.5
        
        # Variables para Matplotlib
        self.fig = None
        self.ax = None
        self.canvas = None

        # Cache para guardar posiciones del grafo (clave para estabilidad visual)
        self._posiciones_grafo = None 

    def configurar_componentes(self, tab_root, metricas_label, colas_tree, fig, ax, canvas):
        """Configura las referencias a componentes de la interfaz"""
        self.tab_root = tab_root
        self.metricas_label = metricas_label
        self.colas_tree = colas_tree
        self.fig = fig
        self.ax = ax
        self.canvas = canvas
        self.inicializar_grafico()
        self.actualizar_estado()

    def inicializar_grafico(self):
        """Configura el gráfico inicial como GRAFO DE NODOS"""
        if not self.ax:
            return
        
        self.ax.clear()
        self.ax.set_title('Red de Bibliotecas - Estado de Colas', fontsize=14, fontweight='bold', pad=5)
        self.ax.axis('off')
        
        if not self.red_bibliotecas.bibliotecas:
            self.ax.text(0.5, 0.5, 'No hay bibliotecas cargadas', 
                        ha='center', va='center', fontsize=14, 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
            self.canvas.draw()
            return
        
        self.dibujar_grafo_colas()

    def _calcular_posiciones_grafo_nx(self, canvas_width=10, canvas_height=8):
        """Calcula y escala las posiciones de los nodos usando un layout de fuerza dirigida."""
        if self._posiciones_grafo is not None:
            return self._posiciones_grafo
        
        nx_graph = nx.Graph()
        
        for bib_id in self.red_bibliotecas.bibliotecas.keys():
            nx_graph.add_node(bib_id)
        
        for origen, aristas in self.red_bibliotecas.grafo.nodos.items():
            for arista in aristas:
                destino = arista.destino
                # Evitar duplicados de aristas en grafo no dirigido
                if origen < destino: 
                    nx_graph.add_edge(origen, destino)

        # Usar el layout 'spring' (Fuerza Dirigida)
        pos = nx.spring_layout(nx_graph, seed=42, k=0.5, iterations=50) 
        
        if not pos:
            return {}

        all_x = [x for x, y in pos.values()]
        all_y = [y for x, y in pos.values()]
        
        if not all_x or not all_y:
            return {}

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        range_x = max_x - min_x if max_x != min_x else 1
        range_y = max_y - min_y if max_y != min_y else 1
        
        # Escalar para que se ajuste al área de (1, 1) a (9, 7) aprox.
        target_width = canvas_width - 2
        target_height = canvas_height - 2
        
        scale_x = target_width / range_x
        scale_y = target_height / range_y
        scale = min(scale_x, scale_y) 

        scaled_pos = {}
        for node, (x, y) in pos.items():
            # Escalar y desplazar para centrar
            scaled_x = 1 + (x - min_x) * scale
            scaled_y = 1 + (y - min_y) * scale
            scaled_pos[node] = (scaled_x, scaled_y)
        
        self._posiciones_grafo = scaled_pos
        return scaled_pos


    def dibujar_grafo_colas(self):
        """Dibuja el grafo de bibliotecas con estado de colas en cada nodo"""
        if not self.ax:
            return
        
        self.ax.clear()
        self.ax.set_title('Red de Bibliotecas - Estado de Colas en Tiempo Real', 
                         fontsize=14, fontweight='bold', pad=5) 
        
        # Establecer límites del plot (coordenadas para el grafo)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 8)
        self.ax.axis('off')
        
        bibliotecas = list(self.red_bibliotecas.bibliotecas.keys())
        if not bibliotecas:
            return
        
        try:
            posiciones = self._calcular_posiciones_grafo_nx(canvas_width=10, canvas_height=8)
        except Exception as e:
            self.ax.text(5, 4, f"Error NX: {e}", ha='center', va='center', color='red')
            self.canvas.draw()
            return

        radio_nodo = 0.5 
        
        # 1. DIBUJAR CONEXIONES (ARISTAS)
        grafo = self.red_bibliotecas.grafo
        aristas_dibujadas = set()

        for origen in grafo.nodos:
            for arista in grafo.nodos[origen]:
                destino = arista.destino
                
                arista_tuple = tuple(sorted((origen, destino)))
                if arista_tuple in aristas_dibujadas:
                    continue
                aristas_dibujadas.add(arista_tuple)
                
                if origen in posiciones and destino in posiciones:
                    x1, y1 = posiciones[origen]
                    x2, y2 = posiciones[destino]
                    
                    self.ax.plot([x1, x2], [y1, y2], 'b-', alpha=0.6, linewidth=2, zorder=1)
                    
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    
                    try:
                        angulo = math.atan2(y2 - y1, x2 - x1)
                    except: 
                        angulo = 0

                    distancia = 0.35
                    
                    offset_x = distancia * math.sin(angulo)
                    offset_y = -distancia * math.cos(angulo)
                         
                    self.ax.text(mid_x + offset_x, mid_y + offset_y, 
                                 f"T:{arista.tiempo//60}m C:{arista.costo:.0f}", 
                                 ha='center', va='center', fontsize=8, zorder=2,
                                 bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9))
        
        # 2. DIBUJAR NODOS (BIBLIOTECAS CON COLAS)
        for bib_id, (x, y) in posiciones.items():
            biblioteca = self.red_bibliotecas.bibliotecas[bib_id]
            estado_colas = biblioteca.obtener_estado_colas()
            
            ing = estado_colas["ingreso"]["cantidad"]
            tras = estado_colas["traspaso"]["cantidad"] 
            sal = estado_colas["salida"]["cantidad"]
            
            total_libros = ing + tras + sal
            if total_libros == 0:
                color_nodo = COLOR_INACTIVO
                actividad_texto = "Inactivo"
            elif total_libros <= 2:
                color_nodo = COLOR_BAJA
                actividad_texto = "Baja"
            elif total_libros <= 5:
                color_nodo = COLOR_MEDIA
                actividad_texto = "Media"
            else:
                color_nodo = COLOR_ALTA
                actividad_texto = "Alta"
            
            # NODO PRINCIPAL (círculo grande)
            circle = plt.Circle((x, y), radio_nodo, color=color_nodo, alpha=0.8, zorder=3)
            self.ax.add_patch(circle)
            
            self.ax.text(x, y + 0.1, bib_id, ha='center', va='center', 
                        fontsize=11, fontweight='bold', zorder=4)
            
            self.ax.text(x, y - 0.25, actividad_texto, ha='center', va='center', 
                        fontsize=7, color='black', zorder=4)
            
            radio_cola = 0.2
            offset = radio_nodo + radio_cola + 0.1
            
            # Cola Ingreso: Usamos 'I' en el centro
            self.ax.plot(x - offset, y, 'o', ms=10, color=COLOR_INGRESO, alpha=0.9, zorder=4)
            self.ax.text(x - offset, y, f"I:{ing}", ha='center', va='center', 
                        fontsize=8, fontweight='bold', color='white', zorder=5)
            
            # Cola Traspaso: Usamos 'T' en el centro
            self.ax.plot(x, y + offset, 'o', ms=10, color=COLOR_TRASPASO, alpha=0.9, zorder=4)
            self.ax.text(x, y + offset, f"T:{tras}", ha='center', va='center', 
                        fontsize=8, fontweight='bold', color='white', zorder=5)
            
            # Cola Salida: Usamos 'S' en el centro
            self.ax.plot(x + offset, y, 'o', ms=10, color=COLOR_SALIDA, alpha=0.9, zorder=4)
            self.ax.text(x + offset, y, f"S:{sal}", ha='center', va='center', 
                        fontsize=8, fontweight='bold', color='white', zorder=5)
            
            self.ax.text(x, y - offset - radio_cola - 0.1, biblioteca.nombre[:15], 
                        ha='center', va='center', fontsize=9, alpha=0.8)
        
        self.canvas.draw()

    def actualizar_grafico(self):
        """Actualiza el gráfico con datos en tiempo real"""
        self.dibujar_grafo_colas()

    # ---------------------------------------------------------------------
    # MÉTODOS DE SIMULACIÓN Y AUXILIARES
    # ---------------------------------------------------------------------

    def iniciar_simulacion(self):
        """Inicia la simulación en un hilo separado"""
        if self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulación ya está en ejecución")
            return
        
        if not self.red_bibliotecas.bibliotecas:
            messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas para simular")
            return
        
        self._posiciones_grafo = None 

        self.simulacion_activa = True
        self._detener_event.clear()
        
        self.simulacion_thread = threading.Thread(target=self._ejecutar_simulacion, daemon=True)
        self.simulacion_thread.start()
        
        self.actualizar_estado("Estado: Iniciando simulación...")
        messagebox.showinfo("Simulación", "Simulación iniciada correctamente")

    def pausar_simulacion(self):
        """Pausa/detiene la simulación"""
        if not self.simulacion_activa:
            messagebox.showwarning("Advertencia", "No hay simulación en ejecución")
            return
        
        self.simulacion_activa = False
        self._detener_event.set()
        
        if self.simulacion_thread and self.simulacion_thread.is_alive():
            self.simulacion_thread.join(timeout=2)
        
        self.actualizar_estado("Estado: Simulación pausada")
        messagebox.showinfo("Simulación", "Simulación pausada/detenida")

    def _ejecutar_simulacion(self):
        """Hilo principal de simulación con criterio de parada"""
        try:
            ticks_sin_actividad = 0
            max_ticks_inactivos = 10
            
            while self.simulacion_activa and not self._detener_event.is_set():
                hay_actividad = self._hay_actividad_en_red()
                
                if not hay_actividad:
                    ticks_sin_actividad += 1
                    if ticks_sin_actividad >= max_ticks_inactivos:
                        self.simulacion_activa = False
                        if self.tab_root:
                            self.tab_root.after(0, lambda: self._finalizar_simulacion_automatica())
                        break
                else:
                    ticks_sin_actividad = 0
                
                self._procesar_tick_simulacion()
                
                if self.tab_root:
                    self.tab_root.after(0, lambda: self.actualizar_estado("Estado: En ejecución"))
                
                time.sleep(self.intervalo_tick)
                
        except Exception as e:
            print(f"Error en simulación: {e}")
            self.simulacion_activa = False
            if self.tab_root:
                self.tab_root.after(0, lambda: messagebox.showerror("Error", f"Error en simulación: {e}"))

    def _hay_actividad_en_red(self):
        """Verifica si hay actividad en alguna biblioteca"""
        for biblioteca in self.red_bibliotecas.bibliotecas.values():
            estado = biblioteca.obtener_estado_colas()
            if (estado["ingreso"]["cantidad"] > 0 or 
                estado["traspaso"]["cantidad"] > 0 or 
                estado["salida"]["cantidad"] > 0):
                return True
        return False

    def _finalizar_simulacion_automatica(self):
        """Finaliza simulación automáticamente"""
        self.actualizar_estado("Estado: Simulación completada - Sin actividad")
        messagebox.showinfo("Simulación Completada", 
                           "La simulación finalizó automáticamente.\nNo hay más transferencias activas.")

    def _procesar_tick_simulacion(self):
        """Procesa un ciclo de simulación (mueve libros entre colas)"""
        try:
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                self._simular_procesamiento_biblioteca(biblioteca)
            self._simular_transferencias_activas()
        except Exception as e:
            print(f"Error procesando tick de simulación: {e}")

    def _simular_procesamiento_biblioteca(self, biblioteca):
        """Simula el procesamiento de libros en las colas de una biblioteca"""
        try:
            if not biblioteca.cola_ingreso.esta_vacia():
                if np.random.random() < 0.3:
                    item = biblioteca.cola_ingreso.desencolar()
                    if hasattr(item, 'titulo') and hasattr(item, 'isbn'):
                        item.cambiar_estado("disponible")
                        biblioteca.agregar_libro_catalogo(item, registrar_rollback=False, contar_ingreso=False)
            
            if not biblioteca.cola_salida.esta_vacia():
                if np.random.random() < 0.4:
                    item = biblioteca.cola_salida.desencolar()
                    if hasattr(item, 'titulo'):
                        self._completar_transferencia_simulada(item)
            
            if not biblioteca.cola_traspaso.esta_vacia():
                if np.random.random() < 0.5:
                    item = biblioteca.cola_traspaso.desencolar()
                    if hasattr(item, 'titulo'):
                        biblioteca.cola_salida.encolar(item)
            
            if np.random.random() < 0.15:
                self._generar_transferencia_aleatoria(biblioteca)
                
        except Exception as e:
            print(f"Error simulando biblioteca {biblioteca.id}: {e}")

    def _simular_transferencias_activas(self):
        """Simula el progreso de transferencias en curso"""
        try:
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                if np.random.random() < 0.2:
                    self._simular_llegada_transferencia(biblioteca)
        except Exception as e:
            print(f"Error simulando transferencias: {e}")

    def _completar_transferencia_simulada(self, libro):
        """Completa una transferencia simulada"""
        try:
            if hasattr(libro, 'titulo'):
                libro.cambiar_estado("disponible")
        except Exception as e:
            print(f"Error completando transferencia: {e}")

    def _generar_transferencia_aleatoria(self, biblioteca_origen):
        """Genera una transferencia aleatoria para simular actividad"""
        try:
            libros_disponibles = biblioteca_origen.catalogo_local.lista_secuencial.mostrar_todos()
            libros_disponibles = [libro for libro in libros_disponibles 
                                if hasattr(libro, 'estado') and libro.estado == "disponible"]
            
            if not libros_disponibles:
                return
            
            libro = np.random.choice(libros_disponibles)
            biblioteca_origen.cola_traspaso.encolar(libro)
            libro.cambiar_estado("en_transito")
            
        except Exception as e:
            print(f"Error generando transferencia aleatoria: {e}")

    def _simular_llegada_transferencia(self, biblioteca):
        """Simula que llega una transferencia a una biblioteca"""
        try:
            todas_las_bibliotecas = list(self.red_bibliotecas.bibliotecas.values())
            
            for otra_biblioteca in todas_las_bibliotecas:
                if otra_biblioteca.id != biblioteca.id:
                    libros_otras = otra_biblioteca.catalogo_local.lista_secuencial.mostrar_todos()
                    libros_en_transito = [libro for libro in libros_otras 
                                        if hasattr(libro, 'estado') and libro.estado == "en_transito"]
                    
                    if libros_en_transito:
                        libro = np.random.choice(libros_en_transito)
                        biblioteca.cola_ingreso.encolar(libro)
                        otra_biblioteca.catalogo_local.lista_secuencial.eliminar(libro)
                        break
                        
        except Exception as e:
            print(f"Error simulando llegada de transferencia: {e}")

    def actualizar_estado(self, texto_estado: str = None):
        """Refresca métricas, tabla Y gráfico"""
        try:
            total_transferencias = 0
            total_en_transito = 0
            
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                estado_colas = biblioteca.obtener_estado_colas()
                total_transferencias += estado_colas["traspaso"]["cantidad"]
                total_en_transito += estado_colas["ingreso"]["cantidad"] + estado_colas["salida"]["cantidad"]
            
            estado = texto_estado or ("Estado: En ejecución" if self.simulacion_activa else "Estado: Detenido")
            
            if self.metricas_label:
                self.metricas_label.config(
                    text=f"{estado} | Transferencias activas: {total_transferencias} | Libros en tránsito: {total_en_transito}"
                )
            
            if self.colas_tree:
                self.colas_tree.delete(*self.colas_tree.get_children())
                for bib_id, biblioteca in self.red_bibliotecas.bibliotecas.items():
                    estado_colas = biblioteca.obtener_estado_colas()
                    self.colas_tree.insert("", "end", text=bib_id,
                        values=(
                            biblioteca.nombre,
                            estado_colas["ingreso"]["cantidad"],
                            estado_colas["traspaso"]["cantidad"],
                            estado_colas["salida"]["cantidad"],
                            estado_colas["ingreso"]["frente"] or "-",
                            estado_colas["traspaso"]["frente"] or "-",
                            estado_colas["salida"]["frente"] or "-"
                        ))
            
            self.actualizar_grafico()
            
        except Exception as e:
            print(f"Error actualizando estado: {e}")


def crear_simulacion_tab(notebook, red_bibliotecas):
    """Crear pestaña de Simulación con visualización Matplotlib"""
    
    tab_simulacion = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_simulacion, text="📦 Simulación y Colas")
    
    # Grid de 2 columnas
    tab_simulacion.grid_columnconfigure(0, weight=1)
    tab_simulacion.grid_columnconfigure(1, weight=1)
    tab_simulacion.grid_rowconfigure(1, weight=1)
    
    ctrl = SimulacionTab(red_bibliotecas)
    
    # === PANEL IZQUIERDO: CONTROLES Y TABLA ===
    panel_izquierdo = ttk.Frame(tab_simulacion, style='Sky.TFrame')
    panel_izquierdo.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
    panel_izquierdo.grid_rowconfigure(2, weight=1)
    
    # Controles
    sim_controls = ttk.Frame(panel_izquierdo, style='Sky.TFrame', padding=10)
    sim_controls.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    tk.Label(sim_controls, text="⚙️ CONTROLES DE SIMULACIÓN", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="▶️ Iniciar", 
               command=ctrl.iniciar_simulacion).pack(side='left', padx=5)
    ttk.Button(sim_controls, text="⏸️ Pausar", 
               command=ctrl.pausar_simulacion).pack(side='left', padx=5)
    
    # Métricas
    metrics_frame = ttk.Frame(panel_izquierdo, style='Sky.TFrame', padding=10)
    metrics_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    
    tk.Label(metrics_frame, text="MÉTRICAS DE DESPACHO:", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')
    
    metricas_label = tk.Label(metrics_frame, 
                              text="Estado: Detenido | Transferencias activas: 0", 
                              bg=FILTER_BG, fg=ACCENT_COLOR)
    metricas_label.pack(anchor='w', pady=5)
    
    # Tabla de colas
    colas_container = ttk.Frame(panel_izquierdo, style='Sky.TFrame', padding=10)
    colas_container.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
    
    tk.Label(colas_container, text="🚦 ESTADO DETALLADO DE COLAS", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=5)
    
    columnas = ("nombre", "ingreso", "traspaso", "salida", "frente_ing", "frente_tra", "frente_sal")
    colas_tree = ttk.Treeview(colas_container, columns=columnas, show="tree headings", height=8)
    
    colas_tree.heading("#0", text="ID")
    colas_tree.column("#0", width=80, anchor="center")
    
    encabezados = ["Nombre", "Ingreso", "Traspaso", "Salida", "Frente Ing", "Frente Tras", "Frente Sal"]
    anchos = [120, 80, 80, 80, 80, 80, 80]
    
    for col, texto, ancho in zip(columnas, encabezados, anchos):
        colas_tree.heading(col, text=texto)
        colas_tree.column(col, width=ancho, anchor="center")
    
    tree_scroll = ttk.Scrollbar(colas_container, orient="vertical", command=colas_tree.yview)
    colas_tree.configure(yscrollcommand=tree_scroll.set)
    
    colas_tree.pack(side="left", fill="both", expand=True)
    tree_scroll.pack(side="right", fill="y")
    
    # === PANEL DERECHO: GRÁFICO MATPLOTLIB ===
    panel_derecho = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    panel_derecho.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
    
    # Título de Visualización
    tk.Label(panel_derecho, text="📊 VISUALIZACIÓN EN TIEMPO REAL", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=5)
    
    # NUEVA SECCIÓN DE LEYENDA (Texto en color con borde)
    leyenda_frame = ttk.Frame(panel_derecho, style='Sky.TFrame', padding=5)
    leyenda_frame.pack(fill="x", padx=5, pady=(0, 5))
    
    def crear_label_leyenda_color(parent, text_color, text_content, is_bold=False):
        """Crea una etiqueta con el texto del color y un borde fuerte."""
        font_style = ('TkDefaultFont', 10, 'bold' if is_bold else '')
        
        # Usamos tk.Label para poder especificar el color de texto (fg) y el borde.
        lbl = tk.Label(parent, 
                       text=text_content, 
                       fg=text_color, 
                       font=font_style, 
                       bg='white', # Fondo neutro para que se vea el color del texto
                       relief=tk.RIDGE, 
                       bd=2, # Borde grueso para distinción
                       padx=5, 
                       pady=2)
        lbl.pack(side='left', padx=(0, 10))
        return lbl

    # 1. Leyenda de Colas (Tipo de Colas)
    tk.Label(leyenda_frame, text="Tipos de Cola (Etiqueta/Color):", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')
             
    colas_line = ttk.Frame(leyenda_frame, style='Sky.TFrame')
    colas_line.pack(anchor='w', pady=(2, 5))
    
    crear_label_leyenda_color(colas_line, COLOR_INGRESO, "Ingreso (I)", is_bold=True)
    crear_label_leyenda_color(colas_line, COLOR_TRASPASO, "Traspaso (T)", is_bold=True)
    crear_label_leyenda_color(colas_line, COLOR_SALIDA, "Salida (S)", is_bold=True)
    
    # 2. Leyenda de Actividad del Nodo
    tk.Label(leyenda_frame, text="Estado de Actividad del Nodo:", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')

    actividad_line = ttk.Frame(leyenda_frame, style='Sky.TFrame')
    actividad_line.pack(anchor='w', pady=(2, 0))

    crear_label_leyenda_color(actividad_line, 'black', "Inactivo (0)", is_bold=False).config(bg=COLOR_INACTIVO)
    crear_label_leyenda_color(actividad_line, COLOR_BAJA, "Baja (1-2)", is_bold=False)
    crear_label_leyenda_color(actividad_line, COLOR_MEDIA, "Media (3-5)", is_bold=False)
    crear_label_leyenda_color(actividad_line, COLOR_ALTA, "Alta (6+)", is_bold=False)

    # Crear figura matplotlib
    fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    
    # Canvas matplotlib
    canvas = FigureCanvasTkAgg(fig, panel_derecho)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Configurar componentes
    ctrl.configurar_componentes(tab_simulacion, metricas_label, colas_tree, fig, ax, canvas)
    
    return tab_simulacion, ctrl