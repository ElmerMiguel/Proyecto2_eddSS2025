"""
Pestaña Visualizacion - Representacion grafica de estructuras
"""

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
]

class VisualizacionTab:
    """Controlador para la pestaña de visualizacion"""

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
        self.canvas.bind("<MouseWheel>", self._zoom_rodillo)          # Windows / macOS
        self.canvas.bind("<Button-4>", self._zoom_scroll_arriba)      # Linux scroll up
        self.canvas.bind("<Button-5>", self._zoom_scroll_abajo)       # Linux scroll down

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
        self.canvas.scale("all", x, y, 1, 1)  # mantener posición relativa

    def _limpiar_canvas(self):
        if self.canvas:
            self.canvas.delete("all")
            self.canvas_imagen_id = None

    def _crear_directorio_temp(self):
        if self._temp_dir and os.path.exists(self._temp_dir):
            return
        self._temp_dir = tempfile.mkdtemp(prefix="viz_biblioteca_")

    def _generar_dot(self, estructura: str) -> str:
        """Genera archivo DOT temporal y retorna su ruta."""
        self._crear_directorio_temp()
        archivo_dot = os.path.join(self._temp_dir, f"{estructura}.dot")

        try:
            if estructura == "grafo":
                if not self.red_bibliotecas.grafo:
                    raise ValueError("El grafo no está inicializado")
                self.red_bibliotecas.grafo.exportar_dot(archivo_dot)
            elif estructura == "colas":
                if not self.red_bibliotecas.bibliotecas:
                    raise ValueError("No hay bibliotecas cargadas")
                biblioteca = next(iter(self.red_bibliotecas.bibliotecas.values()))
                biblioteca.exportar_colas_dot(self._temp_dir)
                # mostramos solo ingreso por defecto
                archivo_dot = os.path.join(self._temp_dir, f"{biblioteca.id}_cola_ingreso.dot")
            else:
                biblioteca = self._obtener_biblioteca_referencia()
                biblioteca.catalogo_local.exportar_estructura_dot(estructura, archivo_dot)
        except Exception as error:
            raise RuntimeError(f"No se pudo generar DOT: {error}") from error

        return archivo_dot

    def _dot_a_png(self, ruta_dot: str) -> str:
        """Convierte dot -> png usando graphviz (requiere 'dot' en PATH)."""
        ruta_png = ruta_dot.replace(".dot", ".png")
        comando = ["dot", "-Tpng", ruta_dot, "-o", ruta_png]
        try:
            subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            raise FileNotFoundError("No se encontró el comando 'dot'. Instala graphviz.")
        except subprocess.CalledProcessError as error:
            raise RuntimeError(error.stderr.decode("utf-8", errors="ignore") or str(error))
        return ruta_png

    def visualizar_estructura(self, estructura: str):
        if not self.canvas:
            return
        try:
            ruta_dot = self._generar_dot(estructura)
            ruta_png = self._dot_a_png(ruta_dot)
            self._mostrar_imagen(ruta_png)
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
        text="🌳 REPRESENTACIÓN GRÁFICA DE ESTRUCTURAS",
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