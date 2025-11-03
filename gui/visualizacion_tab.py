import os
import tempfile
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from .config import *
from objetos.biblioteca import Biblioteca

ESTRUCTURAS_DISPONIBLES = [
    ("Árbol AVL", "avl"),
    ("Árbol B", "b"),
    ("Árbol B+", "bplus"),
    ("Tabla Hash", "hash"),
    ("Grafo de la Red", "grafo"),
    ("Colas de Biblioteca (DOT)", "colas"),
    ("Pilas de Rollback (DOT)", "pilas"),
]

class VisualizacionTab:
    
    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.canvas = None
        self.canvas_imagen_id = None
        self.base_image = None
        self.photo_image = None
        self.zoom_factor = 1.0
        self._drag_data = {"x": 0, "y": 0}
        self._temp_dir = None

    def configurar_canvas(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.canvas.create_text(
            self.canvas.winfo_reqwidth() // 2,
            self.canvas.winfo_reqheight() // 2,
            text="Selecciona una estructura para generar su visualización",
            font=FONT_LABEL_SMALL,
            fill=TITLE_COLOR,
        )
        self._configurar_interacciones()

    def _configurar_interacciones(self):
        if not self.canvas:
            return
        self.canvas.bind("<ButtonPress-1>", self._iniciar_arrastre)
        self.canvas.bind("<B1-Motion>", self._arrastrar)
        self.canvas.bind("<MouseWheel>", self._zoom_rodillo)
        self.canvas.bind("<Button-4>", self._zoom_scroll_arriba)
        self.canvas.bind("<Button-5>", self._zoom_scroll_abajo)

    def _iniciar_arrastre(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _arrastrar(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _zoom_rodillo(self, event):
        delta = 1 if event.delta > 0 else -1
        self._aplicar_zoom(delta, event.x, event.y)

    def _zoom_scroll_arriba(self, event):
        self._aplicar_zoom(1, event.x, event.y)

    def _zoom_scroll_abajo(self, event):
        self._aplicar_zoom(-1, event.x, event.y)

    def _aplicar_zoom(self, delta: int, x: int, y: int):
        if not self.base_image:
            return
        nuevo_zoom = self.zoom_factor + (0.1 * delta)
        nuevo_zoom = max(0.2, min(nuevo_zoom, 3.0))
        if abs(nuevo_zoom - self.zoom_factor) < 1e-6:
            return
        self.zoom_factor = nuevo_zoom
        self._renderizar_imagen()
        self.canvas.scale("all", x, y, 1, 1)

    def _limpiar_canvas(self):
        if self.canvas:
            self.canvas.delete("all")
            self.canvas_imagen_id = None

    def _crear_directorio_temp(self):
        if self._temp_dir and os.path.exists(self._temp_dir):
            return
        self._temp_dir = tempfile.mkdtemp(prefix="viz_biblioteca_")

    def _generar_dot(self, estructura: str) -> str:
        
        self._crear_directorio_temp()
        archivo_dot = os.path.join(self._temp_dir, f"{estructura}.dot")

        try:
            if estructura == "grafo":
                if not self.red_bibliotecas.grafo:
                    raise ValueError("El grafo no está inicializado")
                
                # Resaltar la última ruta calculada si existe
                ruta_actual = getattr(self.red_bibliotecas, 'ultima_ruta_calculada', None)
                
                if ruta_actual:
                    self.red_bibliotecas.grafo.exportar_dot_con_ruta(archivo_dot, ruta_actual)
                else:
                    self.red_bibliotecas.grafo.exportar_dot(archivo_dot)
                    
            elif estructura == "colas":
                if not self.red_bibliotecas.bibliotecas:
                    raise ValueError("No hay bibliotecas cargadas")
                biblioteca = next(iter(self.red_bibliotecas.bibliotecas.values()))
                biblioteca.exportar_colas_dot(self._temp_dir)
                archivo_dot = os.path.join(self._temp_dir, f"{biblioteca.id}_cola_ingreso.dot")
            elif estructura == "pilas":
                biblioteca = self._obtener_biblioteca_referencia()
                if biblioteca:
                    biblioteca.exportar_pila_dot(self._temp_dir)
                    return os.path.join(self._temp_dir, f"{biblioteca.id}_pila_rollback.dot")
            else:
                biblioteca = self._obtener_biblioteca_referencia()
                biblioteca.catalogo_local.exportar_estructura_dot(estructura, archivo_dot)
        except Exception as error:
            raise RuntimeError(f"No se pudo generar DOT: {error}") from error
        
        return archivo_dot

    def _dot_a_png(self, ruta_dot: str) -> str:
        
        ruta_png = ruta_dot.replace(".dot", ".png")
        comando = ["dot", "-Tpng", ruta_dot, "-o", ruta_png]
        try:
            subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            raise FileNotFoundError("No se encontró el comando 'dot'. Instala graphviz.")
        except subprocess.CalledProcessError as error:
            raise RuntimeError(error.stderr.decode("utf-8", errors="ignore") or str(error))
        return ruta_png

    def _mostrar_estadisticas_hash(self, biblioteca):
        
        if not hasattr(biblioteca.catalogo_local, 'tabla_isbn'):
            return
        
        hash_table = biblioteca.catalogo_local.tabla_isbn
        
        colisiones = 0
        max_cadena = 0
        buckets_usados = 0
        
        for bucket in hash_table.tabla:
            if bucket:
                buckets_usados += 1
                longitud = 0
                actual = bucket
                while actual:
                    longitud += 1
                    actual = actual.siguiente
                if longitud > 1:
                    colisiones += longitud - 1
                max_cadena = max(max_cadena, longitud)
        
        factor_carga = hash_table.cantidad / hash_table.capacidad
        buckets_vacios = hash_table.capacidad - buckets_usados
        
        ventana_stats = tk.Toplevel()
        ventana_stats.title("Estadísticas Tabla Hash")
        ventana_stats.geometry("500x400")
        ventana_stats.resizable(False, False)
        
        tk.Label(ventana_stats, text="ANÁLISIS DE TABLA HASH", 
                 font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR).pack(pady=15)
        
        stats_frame = ttk.Frame(ventana_stats, padding=20)
        stats_frame.pack(fill='both', expand=True)
        
        ttk.Label(stats_frame, text="INFORMACIÓN GENERAL", 
                  font=FONT_TITLE_SMALL).grid(row=0, column=0, columnspan=2, pady=(0,10), sticky='w')
        
        ttk.Label(stats_frame, text="Capacidad total:").grid(row=1, column=0, sticky='w', pady=2)
        ttk.Label(stats_frame, text=f"{hash_table.capacidad}").grid(row=1, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Label(stats_frame, text="Elementos almacenados:").grid(row=2, column=0, sticky='w', pady=2)
        ttk.Label(stats_frame, text=f"{hash_table.cantidad}").grid(row=2, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Label(stats_frame, text="Factor de carga:").grid(row=3, column=0, sticky='w', pady=2)
        color_factor = "green" if factor_carga <= 0.75 else "orange" if factor_carga <= 0.9 else "red"
        ttk.Label(stats_frame, text=f"{factor_carga:.2%}", 
                  foreground=color_factor).grid(row=3, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Separator(stats_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=15)
        
        ttk.Label(stats_frame, text="ANÁLISIS DE COLISIONES", 
                  font=FONT_TITLE_SMALL).grid(row=5, column=0, columnspan=2, pady=(0,10), sticky='w')
        
        ttk.Label(stats_frame, text="Buckets utilizados:").grid(row=6, column=0, sticky='w', pady=2)
        ttk.Label(stats_frame, text=f"{buckets_usados}").grid(row=6, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Label(stats_frame, text="Buckets vacíos:").grid(row=7, column=0, sticky='w', pady=2)
        ttk.Label(stats_frame, text=f"{buckets_vacios}").grid(row=7, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Label(stats_frame, text="Total de colisiones:").grid(row=8, column=0, sticky='w', pady=2)
        color_colisiones = "green" if colisiones == 0 else "orange" if colisiones < 5 else "red"
        ttk.Label(stats_frame, text=f"{colisiones}", 
                  foreground=color_colisiones).grid(row=8, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Label(stats_frame, text="Cadena más larga:").grid(row=9, column=0, sticky='w', pady=2)
        color_cadena = "green" if max_cadena <= 2 else "orange" if max_cadena <= 4 else "red"
        ttk.Label(stats_frame, text=f"{max_cadena} elementos", 
                  foreground=color_cadena).grid(row=9, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Separator(stats_frame, orient='horizontal').grid(row=10, column=0, columnspan=2, sticky='ew', pady=15)
        
        ttk.Label(stats_frame, text="EVALUACIÓN DE RENDIMIENTO", 
                  font=FONT_TITLE_SMALL).grid(row=11, column=0, columnspan=2, pady=(0,10), sticky='w')
        
        if factor_carga <= 0.75 and colisiones <= 3:
            estado = "EXCELENTE 🟢"
            descripcion = "Rendimiento óptimo"
            color_estado = "green"
        elif factor_carga <= 0.85 and colisiones <= 8:
            estado = "BUENO 🟡"
            descripcion = "Rendimiento aceptable"
            color_estado = "orange"
        else:
            estado = "NECESITA OPTIMIZACIÓN 🔴"
            descripcion = "Considerar rehashing"
            color_estado = "red"
        
        ttk.Label(stats_frame, text="Estado general:").grid(row=12, column=0, sticky='w', pady=2)
        ttk.Label(stats_frame, text=estado, 
                  foreground=color_estado).grid(row=12, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Label(stats_frame, text="Recomendación:").grid(row=13, column=0, sticky='w', pady=2)
        ttk.Label(stats_frame, text=descripcion).grid(row=13, column=1, sticky='w', padx=(20,0), pady=2)
        
        ttk.Button(ventana_stats, text="Cerrar", 
                   command=ventana_stats.destroy).pack(pady=20)

    def visualizar_estructura(self, estructura: str):
        if not self.canvas:
            return
        try:
            ruta_dot = self._generar_dot(estructura)
            ruta_png = self._dot_a_png(ruta_dot)
            self._mostrar_imagen(ruta_png)
            
            if estructura == "hash":
                biblioteca = self._obtener_biblioteca_referencia()
                self._mostrar_estadisticas_hash(biblioteca)
                
        except FileNotFoundError as error:
            messagebox.showwarning("Graphviz", str(error))
        except RuntimeError as error:
            messagebox.showerror("Error", error)
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo renderizar la estructura: {error}")

    def _mostrar_imagen(self, ruta_png: str):
        self._limpiar_canvas()
        self.base_image = Image.open(ruta_png)
        self.zoom_factor = 1.0
        self._renderizar_imagen()

        if self.canvas:
            bbox = self.canvas.bbox("all")
            if bbox:
                self.canvas.configure(scrollregion=bbox)

    def _renderizar_imagen(self):
        if not self.canvas or not self.base_image:
            return

        ancho = max(1, int(self.base_image.width * self.zoom_factor))
        alto = max(1, int(self.base_image.height * self.zoom_factor))
        imagen_redimensionada = self.base_image.resize((ancho, alto), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(imagen_redimensionada)

        self._limpiar_canvas()
        self.canvas_imagen_id = self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.photo_image,
            anchor="center",
            tags="img"
        )

    def _obtener_biblioteca_referencia(self) -> Biblioteca:
        if not self.red_bibliotecas.bibliotecas:
            raise ValueError("No hay bibliotecas registradas en la red")
        return next(iter(self.red_bibliotecas.bibliotecas.values()))

def crear_visualizacion_tab(notebook, red_bibliotecas):
    tab_visualizacion = ttk.Frame(notebook, style="Sky.TFrame")
    notebook.add(tab_visualizacion, text="📊 Visualización Estructuras")

    tk.Label(
        tab_visualizacion,
        text="REPRESENTACIÓN GRÁFICA DE ESTRUCTURAS",
        font=FONT_TITLE_LARGE,
        fg=TITLE_COLOR,
        bg=FILTER_BG,
    ).pack(pady=20)

    ctrl = VisualizacionTab(red_bibliotecas)

    vis_buttons = ttk.Frame(tab_visualizacion, style="Sky.TFrame")
    vis_buttons.pack(pady=10)

    for texto, clave in ESTRUCTURAS_DISPONIBLES:
        ttk.Button(
            vis_buttons,
            text=texto,
            command=lambda clave=clave: ctrl.visualizar_estructura(clave),
        ).pack(side="left", padx=6)

    canvas_container = tk.Frame(tab_visualizacion, bg=BG_COLOR)
    canvas_container.pack(fill="both", expand=True, padx=20, pady=10)

    vis_canvas = tk.Canvas(
        canvas_container,
        bg=DASH_CARD_BG,
        highlightthickness=1,
        highlightbackground=TITLE_COLOR,
        width=880,
        height=520,
        scrollregion=(0, 0, 880, 520)
    )
    h_scroll = ttk.Scrollbar(canvas_container, orient="horizontal", command=vis_canvas.xview)
    v_scroll = ttk.Scrollbar(canvas_container, orient="vertical", command=vis_canvas.yview)
    vis_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

    vis_canvas.pack(side="left", fill="both", expand=True)
    v_scroll.pack(side="right", fill="y")
    h_scroll.pack(side="bottom", fill="x")

    ctrl.configurar_canvas(vis_canvas)
    return tab_visualizacion, ctrl