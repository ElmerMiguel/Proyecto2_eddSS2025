"""
Pestaña Pruebas - Pruebas de rendimiento, carga CSV y comparaciones
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
from typing import Callable, Optional
from .config import *
from estructuras.metodos_ordenamiento import comparar_metodos

class PruebasTab:
    """Controlador de la pestaña de Pruebas de Rendimiento"""
    
    def __init__(self, red_bibliotecas, on_datos_actualizados: Optional[Callable[[], None]] = None):
        self.red_bibliotecas = red_bibliotecas
        self.on_datos_actualizados = on_datos_actualizados
    
    def _notificar_actualizacion(self):
        if callable(self.on_datos_actualizados):
            self.on_datos_actualizados()
    
    def comparar_busquedas(self):
        """Comparar métodos de búsqueda"""
        try:
            if not self.red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas para comparar")
                return
            
            primera_bib = next(iter(self.red_bibliotecas.bibliotecas.values()))
            libros = primera_bib.catalogo_local.lista_secuencial.mostrar_todos()
            
            if not libros:
                messagebox.showwarning("Advertencia", "No hay libros para comparar")
                return
            
            libro_prueba = libros[len(libros)//2]
            
            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.lista_secuencial.buscar_por_titulo(libro_prueba.titulo)
            tiempo_secuencial = time.perf_counter() - inicio
            
            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.arbol_titulos.buscar(libro_prueba.titulo)
            tiempo_avl = time.perf_counter() - inicio
            
            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.tabla_isbn.buscar(libro_prueba.isbn)
            tiempo_hash = time.perf_counter() - inicio
            
            resultado = f"""
COMPARACIÓN DE BÚSQUEDAS:
Elemento buscado: {libro_prueba.titulo}
Tamaño del catálogo: {len(libros)} libros

Secuencial: {tiempo_secuencial:.6f} segundos
AVL (Título): {tiempo_avl:.6f} segundos  
Hash (ISBN): {tiempo_hash:.6f} segundos

Más rápido: {'Hash' if tiempo_hash < min(tiempo_secuencial, tiempo_avl) else 'AVL' if tiempo_avl < tiempo_secuencial else 'Secuencial'}
            """
            
            messagebox.showinfo("Resultados de Búsqueda", resultado)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en comparación: {e}")
    
    def comparar_ordenamientos(self):
        """Comparar métodos de ordenamiento"""
        try:
            if not self.red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas para comparar")
                return
            
            primera_bib = next(iter(self.red_bibliotecas.bibliotecas.values()))
            libros = primera_bib.catalogo_local.lista_secuencial.mostrar_todos()
            
            if len(libros) < 2:
                messagebox.showwarning("Advertencia", "Se necesitan al menos 2 libros para comparar")
                return
            
            resultado = comparar_metodos(libros, "titulo")
            messagebox.showinfo("Resultados de Ordenamiento", resultado)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en comparación: {e}")
    
    def cargar_csv_bibliotecas(self):
        """Cargar bibliotecas desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                count = self.red_bibliotecas.cargar_bibliotecas_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} bibliotecas cargadas")
                self._notificar_actualizacion()
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando bibliotecas: {e}")
    
    def cargar_csv_conexiones(self):
        """Cargar conexiones desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                count = self.red_bibliotecas.cargar_conexiones_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} conexiones cargadas")
                self._notificar_actualizacion()
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando conexiones: {e}")
    
    def cargar_csv_libros(self):
        """Cargar libros desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                count = self.red_bibliotecas.cargar_libros_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} libros cargados")
                self._notificar_actualizacion()
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando libros: {e}")


def crear_pruebas_carga_tab(notebook, red_bibliotecas, on_datos_actualizados: Optional[Callable[[], None]] = None):
    """Crear y retornar la pestaña de Pruebas de Carga"""
    
    tab_pruebas_carga = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_pruebas_carga, text="⚙️ Pruebas de Rendimiento y Carga (CSV)")
    
    tab_pruebas_carga.grid_columnconfigure((0, 1), weight=1)
    tab_pruebas_carga.grid_rowconfigure(0, weight=1)
    
    ctrl = PruebasTab(red_bibliotecas, on_datos_actualizados)
    
    comp_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    comp_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    tk.Label(comp_frame, text="⏱️ PRUEBAS DE RENDIMIENTO", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    tk.Label(comp_frame, text="COMPARACIÓN DE BÚSQUEDAS:", 
             font=FONT_TITLE_SMALL, bg=FILTER_BG).pack(pady=(5, 5), anchor='w')
    ttk.Button(comp_frame, text="Comparar 3 Métodos de Búsqueda", 
               command=ctrl.comparar_busquedas).pack(pady=5, fill='x')
    
    tk.Label(comp_frame, text="COMPARACIÓN DE ORDENAMIENTOS:", 
             font=FONT_TITLE_SMALL, bg=FILTER_BG).pack(pady=(15, 5), anchor='w')
    ttk.Button(comp_frame, text="Comparar 5 Tipos de Ordenamiento", 
               command=ctrl.comparar_ordenamientos).pack(pady=5, fill='x')
    
    carga_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    carga_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    tk.Label(carga_frame, text="📂 CARGA MASIVA DE DATOS (CSV)", 
             font=FONT_TITLE_MEDIUM, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    tk.Label(carga_frame, text="Seleccione los archivos CSV:", 
             font=FONT_LABEL, bg=FILTER_BG).pack(anchor='w', pady=5)
    
    ttk.Button(carga_frame, text="⬆️ Cargar Catálogo de Libros", 
               command=ctrl.cargar_csv_libros).pack(pady=5, fill='x')
    ttk.Button(carga_frame, text="⬆️ Cargar Bibliotecas", 
               command=ctrl.cargar_csv_bibliotecas).pack(pady=5, fill='x')
    ttk.Button(carga_frame, text="⬆️ Cargar Conexiones", 
               command=ctrl.cargar_csv_conexiones).pack(pady=5, fill='x')
    
    return tab_pruebas_carga, ctrl