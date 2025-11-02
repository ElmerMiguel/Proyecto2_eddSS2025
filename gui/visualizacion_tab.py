"""
Pestaña Visualizacion - Representacion grafica de estructuras
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .config import *
import os
from PIL import Image, ImageTk  # requiere pillow
import subprocess
import tempfile

ESTRUCTURAS_DISPONIBLES = [
    ("Arbol AVL", "avl"),
    ("Arbol B", "b"),
    ("Arbol B+", "bplus"),
    ("Tabla Hash", "hash"),
    ("Grafo de la Red", "grafo"),
]

class VisualizacionTab:
    """Controlador para la pestaña de visualizacion"""

    def __init__(self, red_bibliotecas):
        self.red_bibliotecas = red_bibliotecas
        self.canvas = None
        self.imagen_actual = None
        self.ruta_imagen_temp = None

    def configurar_canvas(self, canvas):
        self.canvas = canvas
        self.canvas.create_text(
            self.canvas.winfo_reqwidth() // 2,
            self.canvas.winfo_reqheight() // 2,
            text="Selecciona una estructura para generar su visualizacion",
            font=FONT_LABEL_SMALL,
            fill=TITLE_COLOR,
        )

    def _generar_dot(self, estructura: str) -> str:
        """Genera archivo DOT temporal y retorna su ruta."""
        directorio = tempfile.mkdtemp(prefix="viz_estructura_")
        archivo_dot = os.path.join(directorio, f"{estructura}.dot")

        try:
            if estructura == "grafo":
                self.red_bibliotecas.grafo.exportar_dot(archivo_dot)
            else:
                if not self.red_bibliotecas.bibliotecas:
                    raise ValueError("No hay bibliotecas cargadas")
                biblioteca = next(iter(self.red_bibliotecas.bibliotecas.values()))
                if estructura == "avl":
                    biblioteca.catalogo_local.arbol_avl.exportar_dot(archivo_dot)
                elif estructura == "b":
                    biblioteca.catalogo_local.arbol_b.exportar_dot(archivo_dot)
                elif estructura == "bplus":
                    biblioteca.catalogo_local.arbol_bplus.exportar_dot(archivo_dot)
                elif estructura == "hash":
                    biblioteca.catalogo_local.tabla_isbn.exportar_dot(archivo_dot)
                else:
                    raise ValueError("Estructura no soportada")
        except Exception as error:
            raise RuntimeError(f"No se pudo generar DOT: {error}") from error

        return archivo_dot

    @staticmethod
    def _dot_a_imagen(ruta_dot: str) -> str:
        """Convierte dot -> png usando graphviz (requiere 'dot' en PATH)."""
        ruta_png = ruta_dot.replace(".dot", ".png")
        comando = ["dot", "-Tpng", ruta_dot, "-o", ruta_png]
        subprocess.run(comando, check=True)
        return ruta_png

    def visualizar_estructura(self, estructura: str):
        if not self.canvas:
            return
        try:
            ruta_dot = self._generar_dot(estructura)
            ruta_png = self._dot_a_imagen(ruta_dot)

            imagen = Image.open(ruta_png)
            self.imagen_actual = ImageTk.PhotoImage(imagen)

            self.canvas.delete("all")
            self.canvas.create_image(
                self.canvas.winfo_reqwidth() // 2,
                self.canvas.winfo_reqheight() // 2,
                image=self.imagen_actual,
                anchor="center",
            )
        except FileNotFoundError:
            messagebox.showwarning("Graphviz", "No se encontro el comando 'dot'. Instala graphviz.")
        except RuntimeError as error:
            messagebox.showerror("Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo renderizar la estructura: {error}")

def crear_visualizacion_tab(notebook, red_bibliotecas):
    tab_visualizacion = ttk.Frame(notebook, style="Sky.TFrame")
    notebook.add(tab_visualizacion, text="📊 Visualizacion Estructuras")

    tk.Label(
        tab_visualizacion,
        text="🌳 REPRESENTACION GRAFICA DE ESTRUCTURAS",
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

    vis_canvas = tk.Canvas(
        tab_visualizacion,
        bg=DASH_CARD_BG,
        highlightthickness=1,
        highlightbackground=TITLE_COLOR,
        width=800,
        height=500,
    )
    vis_canvas.pack(fill="both", expand=True, padx=20, pady=10)

    ctrl.configurar_canvas(vis_canvas)
    return tab_visualizacion, ctrl