"""
Pestaña Simulacion - Simulacion de colas y despacho con visualización Matplotlib
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import numpy as np

# === IMPORTACIONES PARA MATPLOTLIB ===
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from .config import *


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
        self.intervalo_tick = 1.5  # Reducido para mejor visualización
        
        # Variables para Matplotlib
        self.fig = None
        self.ax = None
        self.canvas = None

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
        self.ax.set_title('🌐 Red de Bibliotecas - Estado de Colas', fontsize=14, fontweight='bold')
        self.ax.set_xlim(-1, 11)
        self.ax.set_ylim(-1, 8)
        self.ax.axis('off')  # Sin ejes para el grafo
        
        bibliotecas = list(self.red_bibliotecas.bibliotecas.keys())
        if not bibliotecas:
            self.ax.text(5, 4, 'No hay bibliotecas cargadas', 
                        ha='center', va='center', fontsize=14, 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
            self.canvas.draw()
            return
        
        # Dibujar grafo inicial (sin datos de colas)
        self.dibujar_grafo_colas()

    def dibujar_grafo_colas(self):
        """Dibuja el grafo de bibliotecas con estado de colas en cada nodo"""
        if not self.ax:
            return
        
        self.ax.clear()
        self.ax.set_title('🌐 Red de Bibliotecas - Estado de Colas en Tiempo Real', 
                         fontsize=14, fontweight='bold')
        self.ax.set_xlim(-1, 11)
        self.ax.set_ylim(-1, 8)
        self.ax.axis('off')
        
        bibliotecas = list(self.red_bibliotecas.bibliotecas.keys())
        if not bibliotecas:
            return
        
        # Posiciones fijas para nodos (distribución circular)
        num_bibliotecas = len(bibliotecas)
        centro_x, centro_y = 5, 3.5
        radio = 2.5
        
        posiciones = {}
        for i, bib_id in enumerate(bibliotecas):
            angulo = 2 * 3.14159 * i / num_bibliotecas
            x = centro_x + radio * np.cos(angulo)
            y = centro_y + radio * np.sin(angulo)
            posiciones[bib_id] = (x, y)
        
        # 1. DIBUJAR CONEXIONES (ARISTAS)
        grafo = self.red_bibliotecas.grafo
        for origen in grafo.nodos:
            for arista in grafo.nodos[origen]:
                destino = arista.destino
                if origen in posiciones and destino in posiciones:
                    x1, y1 = posiciones[origen]
                    x2, y2 = posiciones[destino]
                    
                    # Línea de conexión
                    self.ax.plot([x1, x2], [y1, y2], 'b-', alpha=0.6, linewidth=2)
                    
                    # Etiqueta de peso en la conexión
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    self.ax.text(mid_x, mid_y, f"T:{arista.tiempo//60}m\nC:{arista.costo:.0f}", 
                               ha='center', va='center', fontsize=8, 
                               bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
        
        # 2. DIBUJAR NODOS (BIBLIOTECAS CON COLAS)
        for bib_id, (x, y) in posiciones.items():
            biblioteca = self.red_bibliotecas.bibliotecas[bib_id]
            estado_colas = biblioteca.obtener_estado_colas()
            
            # Datos de las colas
            ing = estado_colas["ingreso"]["cantidad"]
            tras = estado_colas["traspaso"]["cantidad"] 
            sal = estado_colas["salida"]["cantidad"]
            
            # Color del nodo según actividad
            total_libros = ing + tras + sal
            if total_libros == 0:
                color_nodo = '#E0E0E0'  # Gris - inactivo
            elif total_libros <= 2:
                color_nodo = '#81C784'  # Verde - poca actividad
            elif total_libros <= 5:
                color_nodo = '#FFB74D'  # Naranja - actividad media
            else:
                color_nodo = '#F06292'  # Rosa - alta actividad
            
            # NODO PRINCIPAL (círculo grande)
            circle = plt.Circle((x, y), 0.6, color=color_nodo, alpha=0.8, zorder=3)
            self.ax.add_patch(circle)
            
            # ETIQUETA DE BIBLIOTECA
            self.ax.text(x, y + 0.1, bib_id, ha='center', va='center', 
                        fontsize=12, fontweight='bold', zorder=4)
            
            # COLAS COMO MINI-CÍRCULOS ALREDEDOR
            # Cola Ingreso (izquierda)
            ing_circle = plt.Circle((x - 0.8, y), 0.2, 
                                   color='#4CAF50', alpha=0.9, zorder=4)
            self.ax.add_patch(ing_circle)
            self.ax.text(x - 0.8, y, str(ing), ha='center', va='center', 
                        fontsize=10, fontweight='bold', color='white', zorder=5)
            
            # Cola Traspaso (arriba)
            tras_circle = plt.Circle((x, y + 0.8), 0.2, 
                                    color='#FF9800', alpha=0.9, zorder=4)
            self.ax.add_patch(tras_circle)
            self.ax.text(x, y + 0.8, str(tras), ha='center', va='center', 
                        fontsize=10, fontweight='bold', color='white', zorder=5)
            
            # Cola Salida (derecha)
            sal_circle = plt.Circle((x + 0.8, y), 0.2, 
                                   color='#F44336', alpha=0.9, zorder=4)
            self.ax.add_patch(sal_circle)
            self.ax.text(x + 0.8, y, str(sal), ha='center', va='center', 
                        fontsize=10, fontweight='bold', color='white', zorder=5)
            
            # Nombre de biblioteca (abajo del nodo)
            self.ax.text(x, y - 0.9, biblioteca.nombre[:15], ha='center', va='center', 
                        fontsize=9, alpha=0.8)
        
        # 3. LEYENDA
        leyenda_x, leyenda_y = 0.5, 6.5
        self.ax.text(leyenda_x, leyenda_y, "🟢 Ingreso  🟠 Traspaso  🔴 Salida", 
                    fontsize=11, ha='left', va='top',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        # Estado de actividad
        self.ax.text(leyenda_x, leyenda_y - 0.8, 
                    "🔘 Inactivo  🟢 Baja  🟠 Media  🔴 Alta Actividad", 
                    fontsize=10, ha='left', va='top',
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.8))
        
        self.canvas.draw()

    def actualizar_grafico(self):
        """Actualiza el gráfico con datos en tiempo real"""
        # Simplemente redibujar todo el grafo con datos actualizados
        self.dibujar_grafo_colas()

    def iniciar_simulacion(self):
        """Inicia la simulación en un hilo separado"""
        if self.simulacion_activa:
            messagebox.showwarning("Advertencia", "La simulación ya está en ejecución")
            return
        
        if not self.red_bibliotecas.bibliotecas:
            messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas para simular")
            return
        
        self.simulacion_activa = True
        self._detener_event.clear()
        
        # Crear y iniciar hilo de simulación
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
            # Esperar a que termine el hilo (máximo 2 segundos)
            self.simulacion_thread.join(timeout=2)
        
        self.actualizar_estado("Estado: Simulación pausada")
        messagebox.showinfo("Simulación", "Simulación pausada/detenida")

    def _ejecutar_simulacion(self):
        """Hilo principal de simulación con criterio de parada"""
        try:
            ticks_sin_actividad = 0
            max_ticks_inactivos = 10  # Parar tras 10 ticks sin actividad
            
            while self.simulacion_activa and not self._detener_event.is_set():
                # Verificar si hay actividad
                hay_actividad = self._hay_actividad_en_red()
                
                if not hay_actividad:
                    ticks_sin_actividad += 1
                    if ticks_sin_actividad >= max_ticks_inactivos:
                        # Parar simulación automáticamente
                        self.simulacion_activa = False
                        if self.tab_root:
                            self.tab_root.after(0, lambda: self._finalizar_simulacion_automatica())
                        break
                else:
                    ticks_sin_actividad = 0
                
                # Procesar tick
                self._procesar_tick_simulacion()
                
                # Actualizar interfaz
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
            # Iterar sobre todas las bibliotecas
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                # Simular procesamiento de colas
                self._simular_procesamiento_biblioteca(biblioteca)
                
            # Simular transferencias entre bibliotecas
            self._simular_transferencias_activas()
            
        except Exception as e:
            print(f"Error procesando tick de simulación: {e}")

    def _simular_procesamiento_biblioteca(self, biblioteca):
        """Simula el procesamiento de libros en las colas de una biblioteca"""
        try:
            # Procesar cola de ingreso (mover a catálogo)
            if not biblioteca.cola_ingreso.esta_vacia():
                # Probabilidad 30% de procesar libro de ingreso
                if np.random.random() < 0.3:
                    item = biblioteca.cola_ingreso.desencolar()
                    
                    # ✅ VERIFICAR QUE SEA UN OBJETO LIBRO
                    if hasattr(item, 'titulo') and hasattr(item, 'isbn'):
                        # Es un libro real
                        item.cambiar_estado("disponible")
                        biblioteca.agregar_libro_catalogo(item, registrar_rollback=False, contar_ingreso=False)
                    else:
                        # Es un string u otro objeto, ignorar
                        print(f"Item procesado en ingreso: {type(item)}")
            
            # Procesar cola de salida (completar transferencia)
            if not biblioteca.cola_salida.esta_vacia():
                # Probabilidad 40% de despachar libro
                if np.random.random() < 0.4:
                    item = biblioteca.cola_salida.desencolar()
                    
                    # ✅ VERIFICAR QUE SEA UN OBJETO LIBRO
                    if hasattr(item, 'titulo'):
                        self._completar_transferencia_simulada(item)
                    else:
                        print(f"Item procesado en salida: {type(item)}")
            
            # Procesar cola de traspaso (mover a cola de salida)
            if not biblioteca.cola_traspaso.esta_vacia():
                # Probabilidad 50% de procesar traspaso
                if np.random.random() < 0.5:
                    item = biblioteca.cola_traspaso.desencolar()
                    
                    # ✅ VERIFICAR QUE SEA UN OBJETO LIBRO
                    if hasattr(item, 'titulo'):
                        biblioteca.cola_salida.encolar(item)
                    else:
                        print(f"Item procesado en traspaso: {type(item)}")
            
            # Generar nuevas transferencias ocasionalmente
            if np.random.random() < 0.15:  # 15% de probabilidad
                self._generar_transferencia_aleatoria(biblioteca)
                
        except Exception as e:
            print(f"Error simulando biblioteca {biblioteca.id}: {e}")

    def _simular_transferencias_activas(self):
        """Simula el progreso de transferencias en curso"""
        try:
            # Iterar sobre bibliotecas y simular llegada de transferencias
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                # Probabilidad 20% de recibir una transferencia simulada
                if np.random.random() < 0.2:
                    self._simular_llegada_transferencia(biblioteca)
                    
        except Exception as e:
            print(f"Error simulando transferencias: {e}")

    def _completar_transferencia_simulada(self, libro):
        """Completa una transferencia simulada"""
        try:
            if hasattr(libro, 'titulo'):
                libro.cambiar_estado("disponible")
                print(f"Transferencia completada: {libro.titulo}")
            else:
                print(f"Transferencia completada: {libro}")
        except Exception as e:
            print(f"Error completando transferencia: {e}")

    def _generar_transferencia_aleatoria(self, biblioteca_origen):
        """Genera una transferencia aleatoria para simular actividad"""
        try:
            # Obtener libros disponibles REALES
            libros_disponibles = biblioteca_origen.catalogo_local.lista_secuencial.mostrar_todos()
            libros_disponibles = [libro for libro in libros_disponibles 
                                if hasattr(libro, 'estado') and libro.estado == "disponible"]
            
            if not libros_disponibles:
                return
            
            # Seleccionar libro aleatorio REAL
            libro = np.random.choice(libros_disponibles)
            
            # ✅ CORRECCIÓN: Agregar el OBJETO LIBRO, no un string
            biblioteca_origen.cola_traspaso.encolar(libro)
            
            # Cambiar estado del libro
            libro.cambiar_estado("en_transito")
            
        except Exception as e:
            print(f"Error generando transferencia aleatoria: {e}")

    def _simular_llegada_transferencia(self, biblioteca):
        """Simula que llega una transferencia a una biblioteca"""
        try:
            # ✅ CORRECCIÓN: Solo simular si hay libros disponibles para transferir
            todas_las_bibliotecas = list(self.red_bibliotecas.bibliotecas.values())
            
            for otra_biblioteca in todas_las_bibliotecas:
                if otra_biblioteca.id != biblioteca.id:
                    # Obtener libros en tránsito hacia esta biblioteca
                    libros_otras = otra_biblioteca.catalogo_local.lista_secuencial.mostrar_todos()
                    libros_en_transito = [libro for libro in libros_otras 
                                        if hasattr(libro, 'estado') and libro.estado == "en_transito"]
                    
                    if libros_en_transito:
                        # Seleccionar uno aleatorio y "transferirlo"
                        libro = np.random.choice(libros_en_transito)
                        
                        # Mover libro a cola de ingreso del destino
                        biblioteca.cola_ingreso.encolar(libro)
                        
                        # Remover de biblioteca origen (simular transferencia)
                        otra_biblioteca.catalogo_local.lista_secuencial.eliminar(libro)
                        
                        break  # Solo una transferencia por tick
                        
        except Exception as e:
            print(f"Error simulando llegada de transferencia: {e}")

    def actualizar_estado(self, texto_estado: str = None):
        """Refresca métricas, tabla Y gráfico"""
        try:
            # Calcular estadísticas
            total_transferencias = 0
            total_en_transito = 0
            
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                estado_colas = biblioteca.obtener_estado_colas()
                total_transferencias += estado_colas["traspaso"]["cantidad"]
                total_en_transito += estado_colas["ingreso"]["cantidad"] + estado_colas["salida"]["cantidad"]
            
            estado = texto_estado or ("Estado: En ejecución" if self.simulacion_activa else "Estado: Detenido")
            
            # Actualizar métricas
            if self.metricas_label:
                self.metricas_label.config(
                    text=f"{estado} | Transferencias activas: {total_transferencias} | Libros en tránsito: {total_en_transito}"
                )
            
            # Actualizar tabla
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
            
            # Actualizar gráfico Matplotlib
            self.actualizar_grafico()
            
        except Exception as e:
            print(f"Error actualizando estado: {e}")


def crear_simulacion_tab(notebook, red_bibliotecas):
    """Crear pestaña de Simulación con visualización Matplotlib"""
    
    tab_simulacion = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_simulacion, text="📦 Simulación y Colas")
    
    # Grid de 2 columnas: izquierda (controles+tabla), derecha (gráfico)
    tab_simulacion.grid_columnconfigure(0, weight=1)  # Controles y tabla
    tab_simulacion.grid_columnconfigure(1, weight=1)  # Gráfico matplotlib
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
    
    # Configurar tabla
    columnas = ("nombre", "ingreso", "traspaso", "salida", "frente_ing", "frente_tra", "frente_sal")
    colas_tree = ttk.Treeview(colas_container, columns=columnas, show="tree headings", height=8)
    
    # Configurar encabezados
    colas_tree.heading("#0", text="ID")
    colas_tree.column("#0", width=80, anchor="center")
    
    encabezados = ["Nombre", "Ingreso", "Traspaso", "Salida", "Frente Ing", "Frente Tras", "Frente Sal"]
    anchos = [120, 80, 80, 80, 80, 80, 80]
    
    for col, texto, ancho in zip(columnas, encabezados, anchos):
        colas_tree.heading(col, text=texto)
        colas_tree.column(col, width=ancho, anchor="center")
    
    # Scrollbar para tabla
    tree_scroll = ttk.Scrollbar(colas_container, orient="vertical", command=colas_tree.yview)
    colas_tree.configure(yscrollcommand=tree_scroll.set)
    
    colas_tree.pack(side="left", fill="both", expand=True)
    tree_scroll.pack(side="right", fill="y")
    
    # === PANEL DERECHO: GRÁFICO MATPLOTLIB ===
    panel_derecho = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    panel_derecho.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
    
    tk.Label(panel_derecho, text="📊 VISUALIZACIÓN EN TIEMPO REAL", 
             font=FONT_TITLE_LARGE, fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=5)
    
    # Crear figura matplotlib
    fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    
    # Canvas matplotlib
    canvas = FigureCanvasTkAgg(fig, panel_derecho)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Configurar componentes
    ctrl.configurar_componentes(tab_simulacion, metricas_label, colas_tree, fig, ax, canvas)
    
    return tab_simulacion, ctrl