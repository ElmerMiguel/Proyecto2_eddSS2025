"""
Pestaña Pruebas - Pruebas de rendimiento mejoradas e interactivas
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
        
        self.busqueda_titulo_var = tk.StringVar()
        self.busqueda_isbn_var = tk.StringVar()
        self.ordenamiento_campo_var = tk.StringVar(value="titulo")
        
        self.resultados_text = None
    
    def _notificar_actualizacion(self):
        if callable(self.on_datos_actualizados):
            self.on_datos_actualizados()
    
    def comparar_busquedas_interactivo(self):
        titulo_buscar = self.busqueda_titulo_var.get().strip()
        isbn_buscar = self.busqueda_isbn_var.get().strip()
        
        if not titulo_buscar and not isbn_buscar:
            messagebox.showwarning("Advertencia", "Ingrese título o ISBN para buscar")
            return
        
        try:
            if not self.red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas")
                return
            
            biblioteca_con_libro = None
            for bib in self.red_bibliotecas.bibliotecas.values():
                if titulo_buscar and bib.catalogo_local.lista_secuencial.buscar_por_titulo(titulo_buscar):
                    biblioteca_con_libro = bib
                    break
                elif isbn_buscar and bib.catalogo_local.tabla_isbn.buscar(isbn_buscar):
                    biblioteca_con_libro = bib
                    break
            
            if not biblioteca_con_libro:
                messagebox.showwarning("Advertencia", "Libro no encontrado en ninguna biblioteca")
                return
            
            resultados = []
            resultados.append("=" * 60)
            resultados.append("📊 COMPARACIÓN INTERACTIVA DE BÚSQUEDAS")
            resultados.append("=" * 60)
            
            if titulo_buscar:
                resultados.append(f"\n🔍 Búsqueda por título: '{titulo_buscar}'")
                
                inicio = time.perf_counter()
                resultado_sec = biblioteca_con_libro.catalogo_local.lista_secuencial.buscar_por_titulo(titulo_buscar)
                tiempo_sec = time.perf_counter() - inicio
                
                inicio = time.perf_counter()
                resultado_avl = biblioteca_con_libro.catalogo_local.arbol_titulos.buscar(titulo_buscar)
                tiempo_avl = time.perf_counter() - inicio
                
                resultados.append(f"  Secuencial: {tiempo_sec:.8f}s - {'✅ Encontrado' if resultado_sec else '❌ No encontrado'}")
                resultados.append(f"  AVL:        {tiempo_avl:.8f}s - {'✅ Encontrado' if resultado_avl else '❌ No encontrado'}")
                resultados.append(f"  Más rápido: {'AVL' if tiempo_avl < tiempo_sec else 'Secuencial'}")
            
            if isbn_buscar:
                resultados.append(f"\n🔍 Búsqueda por ISBN: '{isbn_buscar}'")
                
                inicio = time.perf_counter()
                resultado_hash = biblioteca_con_libro.catalogo_local.tabla_isbn.buscar(isbn_buscar)
                tiempo_hash = time.perf_counter() - inicio
                
                inicio = time.perf_counter()
                resultado_sec = biblioteca_con_libro.catalogo_local.lista_secuencial.buscar_por_isbn(isbn_buscar)
                tiempo_sec = time.perf_counter() - inicio
                
                resultados.append(f"  Hash:       {tiempo_hash:.8f}s - {'✅ Encontrado' if resultado_hash else '❌ No encontrado'}")
                resultados.append(f"  Secuencial: {tiempo_sec:.8f}s - {'✅ Encontrado' if resultado_sec else '❌ No encontrado'}")
                resultados.append(f"  Más rápido: {'Hash' if tiempo_hash < tiempo_sec else 'Secuencial'}")
            
            if self.resultados_text:
                self.resultados_text.delete(1.0, tk.END)
                self.resultados_text.insert(1.0, "\n".join(resultados))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en comparación: {e}")
    
    def comparar_ordenamientos_interactivo(self):
        campo = self.ordenamiento_campo_var.get()
        
        try:
            if not self.red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas")
                return
            
            todos_los_libros = []
            for biblioteca in self.red_bibliotecas.bibliotecas.values():
                libros_bib = biblioteca.catalogo_local.lista_secuencial.mostrar_todos()
                todos_los_libros.extend(libros_bib)
            
            if len(todos_los_libros) < 2:
                messagebox.showwarning("Advertencia", "Se necesitan al menos 2 libros")
                return
            
            resultado = comparar_metodos(todos_los_libros, campo)
            
            resultados = []
            resultados.append("=" * 60)
            resultados.append("📊 COMPARACIÓN DE ALGORITMOS DE ORDENAMIENTO")
            resultados.append("=" * 60)
            resultados.append(f"Campo de ordenamiento: {campo}")
            resultados.append(f"Cantidad de libros: {len(todos_los_libros)}")
            resultados.append("=" * 60)
            resultados.append(resultado)
            
            if self.resultados_text:
                self.resultados_text.delete(1.0, tk.END)
                self.resultados_text.insert(1.0, "\n".join(resultados))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en comparación: {e}")
    
    def cargar_csv_bibliotecas(self):
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
    
    tab_pruebas_carga = ttk.Frame(notebook, style='Sky.TFrame')
    notebook.add(tab_pruebas_carga, text="⚙️ Pruebas de Rendimiento y Carga (CSV)")
    
    tab_pruebas_carga.grid_columnconfigure((0, 1), weight=1)
    tab_pruebas_carga.grid_rowconfigure((0, 1), weight=1)
    
    ctrl = PruebasTab(red_bibliotecas, on_datos_actualizados)
    
    # === FRAME BÚSQUEDAS INTERACTIVAS ===
    busq_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    busq_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    tk.Label(busq_frame, text="🔍 COMPARACIÓN INTERACTIVA DE BÚSQUEDAS", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    tk.Label(busq_frame, text="Título a buscar:", bg=FILTER_BG).pack(anchor='w')
    ttk.Entry(busq_frame, textvariable=ctrl.busqueda_titulo_var).pack(fill='x', pady=2)
    
    tk.Label(busq_frame, text="ISBN a buscar:", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    ttk.Entry(busq_frame, textvariable=ctrl.busqueda_isbn_var).pack(fill='x', pady=2)
    
    ttk.Button(busq_frame, text="🚀 Comparar Búsquedas", 
               command=ctrl.comparar_busquedas_interactivo).pack(pady=10, fill='x')
    
    # === FRAME ORDENAMIENTOS INTERACTIVOS ===
    ord_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    ord_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
    tk.Label(ord_frame, text="📊 COMPARACIÓN DE ORDENAMIENTOS", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    tk.Label(ord_frame, text="Campo a ordenar:", bg=FILTER_BG).pack(anchor='w')
    campo_combo = ttk.Combobox(ord_frame, textvariable=ctrl.ordenamiento_campo_var, 
                               values=["titulo", "autor", "anio", "isbn"], state="readonly")
    campo_combo.pack(fill='x', pady=2)
    
    ttk.Button(ord_frame, text="🚀 Comparar 5 Algoritmos", 
               command=ctrl.comparar_ordenamientos_interactivo).pack(pady=10, fill='x')
    
    # === FRAME CARGA CSV ===
    carga_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    carga_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    tk.Label(carga_frame, text="📂 CARGA MASIVA (CSV)", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    
    
    ttk.Button(carga_frame, text="⬆️ Cargar Bibliotecas", 
               command=ctrl.cargar_csv_bibliotecas).pack(pady=2, fill='x')
    ttk.Button(carga_frame, text="⬆️ Cargar Libros", 
               command=ctrl.cargar_csv_libros).pack(pady=2, fill='x')
    ttk.Button(carga_frame, text="⬆️ Cargar Conexiones", 
               command=ctrl.cargar_csv_conexiones).pack(pady=2, fill='x')
    
    # === FRAME RESULTADOS ===
    result_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    result_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    
    tk.Label(result_frame, text="📋 RESULTADOS DE PRUEBAS", 
             font=FONT_TITLE_SMALL, fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 5))
    
    text_frame = ttk.Frame(result_frame)
    text_frame.pack(fill='both', expand=True)
    
    ctrl.resultados_text = tk.Text(text_frame, height=15, font=("Courier", 9))
    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=ctrl.resultados_text.yview)
    ctrl.resultados_text.configure(yscrollcommand=scrollbar.set)
    
    ctrl.resultados_text.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return tab_pruebas_carga, ctrl