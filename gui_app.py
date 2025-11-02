import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import time
import threading
from pathlib import Path

# Importar todas las estructuras del backend
from objetos.red_bibliotecas import RedBibliotecas
from objetos.biblioteca import Biblioteca
from objetos.libro import Libro
from objetos.transferencia import Transferencia
from estructuras.metodos_ordenamiento import comparar_metodos

# Colores mágicos
BG_COLOR = "#e6f0ff"        
TITLE_COLOR = "#2a2a72"     
BUTTON_COLOR = "#4a90e2"    
FILTER_BG = "#d9e4f5"       
ACCENT_COLOR = "#1e6bbd"    
DASH_CARD_BG = "#ffffff"    

# Variables globales
red_bibliotecas = None
simulacion_activa = False
simulacion_thread = None

def iniciar_gui():
    global red_bibliotecas
    
    # Inicializar sistema
    red_bibliotecas = RedBibliotecas()
    
    # --- 1. CONFIGURACIÓN INICIAL Y ESTILOS ---
    root = tk.Tk()
    root.title("📚 Biblioteca Mágica Alrededor del Mundo - Sistema de Gestión de Red")
    root.geometry("1200x800")
    root.configure(bg=BG_COLOR)

    style = ttk.Style(root)
    style.theme_use("clam") 

    # Estilos ttk
    style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
    style.configure('TNotebook.Tab', 
                    font=('Arial', 11, 'bold'), 
                    foreground='white',
                    background=BUTTON_COLOR,
                    bordercolor=BG_COLOR,
                    padding=[15, 5])

    style.map('TNotebook.Tab', 
              background=[('selected', ACCENT_COLOR), ('active', BUTTON_COLOR)],
              foreground=[('selected', 'white')],
              bordercolor=[('selected', FILTER_BG)])

    style.configure('Sky.TFrame', background=FILTER_BG)
    style.configure('TLabel', background=FILTER_BG)
    style.configure('TCheckbutton', background=FILTER_BG, foreground=TITLE_COLOR)
    style.configure('TRadiobutton', background=FILTER_BG, foreground=TITLE_COLOR)
    style.configure('TButton', font=('Arial', 10, 'bold'), foreground='white', 
                    background=BUTTON_COLOR, padding=6, relief='flat')
    style.map('TButton', background=[('active', ACCENT_COLOR)])

    # --- 2. LAYOUT PRINCIPAL ---
    title = tk.Label(root, text="✨ Sistema de Gestión Arcana ✨", 
                     font=("Georgia", 26, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
    title.pack(pady=(20, 10))

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=20, expand=True, fill="both")

    # --- 3. CREACIÓN DE PESTAÑAS ---
    tab_dashboard = ttk.Frame(notebook, style='Sky.TFrame')
    tab_catalogo = ttk.Frame(notebook, style='Sky.TFrame')
    tab_red = ttk.Frame(notebook, style='Sky.TFrame')
    tab_busqueda_rutas = ttk.Frame(notebook, style='Sky.TFrame') 
    tab_simulacion = ttk.Frame(notebook, style='Sky.TFrame')
    tab_visualizacion = ttk.Frame(notebook, style='Sky.TFrame')
    tab_pruebas_carga = ttk.Frame(notebook, style='Sky.TFrame')

    notebook.add(tab_dashboard, text="🏠 Inicio/Dashboard")
    notebook.add(tab_catalogo, text="📚 Catálogo y Libro (CRUD)")
    notebook.add(tab_red, text="🌐 Gestión de la Red (Grafo)")
    notebook.add(tab_busqueda_rutas, text="🔍 Búsqueda y Rutas Óptimas")
    notebook.add(tab_simulacion, text="📦 Simulación y Colas")
    notebook.add(tab_visualizacion, text="📊 Visualización Estructuras")
    notebook.add(tab_pruebas_carga, text="⚙️ Pruebas de Rendimiento y Carga (CSV)")

    # --- 4. VARIABLES DE ENTRADA ---
    # Variables para CRUD de libros
    titulo_var = tk.StringVar()
    autor_var = tk.StringVar()
    isbn_var = tk.StringVar()
    anio_var = tk.StringVar()
    genero_var = tk.StringVar()
    estado_var = tk.StringVar(value="disponible")
    biblioteca_origen_var = tk.StringVar()
    biblioteca_destino_var = tk.StringVar()
    prioridad_var = tk.StringVar(value="tiempo")
    
    # Variables para bibliotecas
    bib_nombre_var = tk.StringVar()
    bib_ubicacion_var = tk.StringVar()
    bib_tiempo_ingreso_var = tk.StringVar(value="10")
    bib_tiempo_traspaso_var = tk.StringVar(value="5")
    bib_intervalo_despacho_var = tk.StringVar(value="3")
    
    # Variables para conexiones
    origen_var = tk.StringVar()
    destino_var = tk.StringVar()
    tiempo_conexion_var = tk.StringVar()
    costo_conexion_var = tk.StringVar()
    bidireccional_var = tk.BooleanVar(value=True)
    
    # Variables para búsquedas
    buscar_titulo_var = tk.StringVar()
    buscar_isbn_var = tk.StringVar()
    buscar_genero_var = tk.StringVar()
    anio_inicio_var = tk.StringVar()
    anio_fin_var = tk.StringVar()
    
    # Variables para rutas
    libro_enviar_var = tk.StringVar()
    ruta_origen_var = tk.StringVar()
    ruta_destino_var = tk.StringVar()
    criterio_var = tk.StringVar(value="tiempo")

    # --- 5. FUNCIONES DEL BACKEND ---
    
    def actualizar_catalogo_tree():
        """Actualiza el TreeView con libros del catálogo"""
        for item in catalog_tree.get_children():
            catalog_tree.delete(item)
        
        total_libros = 0
        for biblioteca_id, biblioteca in red_bibliotecas.bibliotecas.items():
            try:
                # ✅ CORREGIDO: catalogo_local en lugar de catalogo
                libros = biblioteca.catalogo_local.lista_secuencial.mostrar_todos()
                
                # ✅ VERIFICAR QUE NO SEA None
                if libros is None:
                    libros = []
                
                for libro in libros:
                    catalog_tree.insert("", "end", values=(
                        libro.titulo, libro.autor, libro.isbn, libro.estado, biblioteca_id
                    ))
                    total_libros += 1
                    
            except Exception as e:
                print(f"Error obteniendo libros de {biblioteca_id}: {e}")
        
        print(f"✅ {total_libros} libros mostrados en la tabla")
    
    

    def actualizar_comboboxes():
        """Actualiza los comboboxes con datos actuales"""
        bibliotecas_ids = list(red_bibliotecas.bibliotecas.keys())
        
        # Actualizar comboboxes de bibliotecas
        if bibliotecas_ids:
            origen_combo['values'] = bibliotecas_ids
            destino_combo['values'] = bibliotecas_ids
            ruta_origen_combo['values'] = bibliotecas_ids
            ruta_destino_combo['values'] = bibliotecas_ids
            # ✅ AGREGAR ESTAS LÍNEAS:
            biblioteca_origen_combo['values'] = bibliotecas_ids
            biblioteca_destino_combo['values'] = bibliotecas_ids
            
            # Establecer primera biblioteca como origen por defecto
            if biblioteca_origen_var.get() == "":
                biblioteca_origen_var.set(bibliotecas_ids[0])
        
        # Actualizar géneros disponibles
        generos = set()
        for bib in red_bibliotecas.bibliotecas.values():
            try:
                generos_bib = bib.catalogo_local.obtener_generos_disponibles()
                generos.update(generos_bib)
            except Exception:
                pass
        
        if generos:
            buscar_genero_combo['values'] = list(generos)

    
    
    
    
    def agregar_libro():
        """Agregar nuevo libro con todos los campos"""
        try:
            # Validar campos obligatorios
            if not all([titulo_var.get().strip(), autor_var.get().strip(), isbn_var.get().strip()]):
                messagebox.showerror("Error", "Título, autor e ISBN son obligatorios")
                return
            
            # Validar que hay bibliotecas
            if not red_bibliotecas.bibliotecas:
                messagebox.showerror("Error", "No hay bibliotecas. Carga bibliotecas primero.")
                return
                
            try:
                anio = int(anio_var.get())
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número válido")
                return
            
            # ✅ CREAR LIBRO CON TODOS LOS CAMPOS
            libro = Libro(
                titulo=titulo_var.get().strip(),
                isbn=isbn_var.get().strip(),
                genero=genero_var.get().strip(),
                anio=anio,
                autor=autor_var.get().strip(),
                estado=estado_var.get(),
                biblioteca_origen=biblioteca_origen_var.get(),
                biblioteca_destino=biblioteca_destino_var.get(),
                prioridad=prioridad_var.get()
            )
            
            # ✅ AGREGAR A BIBLIOTECA CORRECTA
            bib_origen = biblioteca_origen_var.get()
            if bib_origen and bib_origen in red_bibliotecas.bibliotecas:
                red_bibliotecas.bibliotecas[bib_origen].catalogo_local.agregar_libro(libro, "General")
                
                # ✅ SI HAY DESTINO DIFERENTE, PROGRAMAR TRANSFERENCIA
                bib_destino = biblioteca_destino_var.get()
                if bib_destino and bib_destino != bib_origen:
                    red_bibliotecas.programar_transferencia(libro.isbn, bib_origen, bib_destino, prioridad_var.get())
            else:
                # Agregar a primera biblioteca disponible
                primera_bib = next(iter(red_bibliotecas.bibliotecas.values()))
                primera_bib.catalogo_local.agregar_libro(libro, "General")
            
            # Limpiar formulario
            titulo_var.set("")
            autor_var.set("")
            isbn_var.set("")
            anio_var.set("")
            genero_var.set("")
            estado_var.set("disponible")
            biblioteca_origen_var.set("")
            biblioteca_destino_var.set("")
            prioridad_var.set("tiempo")
            
            messagebox.showinfo("Éxito", f"Libro '{libro.titulo}' agregado correctamente")
            actualizar_catalogo_tree()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar libro: {e}")


    def eliminar_libro():
        """Eliminar libro del catálogo"""
        selected = catalog_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar")
            return
        
        try:
            item = catalog_tree.item(selected[0])
            isbn = item['values'][2]
            
            eliminado = False
            for biblioteca in red_bibliotecas.bibliotecas.values():
                # ✅ USAR MÉTODO CORRECTO DE BIBLIOTECA
                if biblioteca.eliminar_libro_catalogo(isbn):
                    eliminado = True
                    break
            
            if eliminado:
                messagebox.showinfo("Éxito", "Libro eliminado correctamente")
                actualizar_catalogo_tree()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el libro")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar libro: {e}")

    def rollback_operacion():
        """Deshacer última operación"""
        try:
            if red_bibliotecas.bibliotecas:
                primera_bib = next(iter(red_bibliotecas.bibliotecas.values()))
                # ✅ USAR MÉTODO CORRECTO DE BIBLIOTECA
                libro_restaurado = primera_bib.rollback_ultimo_ingreso()
                
                if libro_restaurado:
                    messagebox.showinfo("Éxito", f"Operación deshecha: {libro_restaurado.titulo}")
                    actualizar_catalogo_tree()
                else:
                    messagebox.showwarning("Advertencia", "No hay operaciones para deshacer")
        except Exception as e:
            messagebox.showerror("Error", f"Error en rollback: {e}")

    def agregar_biblioteca():
        """Agregar nueva biblioteca"""
        try:
            nombre = bib_nombre_var.get()
            if not nombre:
                messagebox.showerror("Error", "El nombre de la biblioteca es obligatorio")
                return
            
            # Generar ID único
            bib_id = f"BIB{len(red_bibliotecas.bibliotecas) + 1:03d}"
            
            biblioteca = Biblioteca(
                id_biblioteca=bib_id,
                nombre=nombre,
                ubicacion=bib_ubicacion_var.get() or "Sin ubicación",
                tiempo_ingreso=int(bib_tiempo_ingreso_var.get()) if bib_tiempo_ingreso_var.get() else 10,
                tiempo_traspaso=int(bib_tiempo_traspaso_var.get()) if bib_tiempo_traspaso_var.get() else 5,
                intervalo_despacho=int(bib_intervalo_despacho_var.get()) if bib_intervalo_despacho_var.get() else 3
            )
            
            red_bibliotecas.bibliotecas[bib_id] = biblioteca
            # ✅ CORREGIDO: grafo en lugar de grafo_red
            red_bibliotecas.grafo.agregar_nodo(bib_id, nombre)
            
            messagebox.showinfo("Éxito", f"Biblioteca '{nombre}' creada con ID: {bib_id}")
            
            # Limpiar campos
            bib_nombre_var.set("")
            bib_ubicacion_var.set("")
            bib_tiempo_ingreso_var.set("10")
            bib_tiempo_traspaso_var.set("5")
            bib_intervalo_despacho_var.set("3")
            
            actualizar_comboboxes()
            dibujar_grafo()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear biblioteca: {e}")

    def agregar_conexion():
        """Agregar conexión entre bibliotecas"""
        try:
            origen = origen_var.get()
            destino = destino_var.get()
            tiempo = tiempo_conexion_var.get()
            costo = costo_conexion_var.get()
            
            if not all([origen, destino, tiempo, costo]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # ✅ CORREGIDO: grafo en lugar de grafo_red
            red_bibliotecas.grafo.agregar_arista(
                origen=origen,
                destino=destino,
                tiempo=int(tiempo),
                costo=float(costo),
                bidireccional=bidireccional_var.get()
            )
            
            messagebox.showinfo("Éxito", f"Conexión creada: {origen} -> {destino}")
            
            # Limpiar campos
            tiempo_conexion_var.set("")
            costo_conexion_var.set("")
            
            dibujar_grafo()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear conexión: {e}")

    def buscar_por_titulo():
        """Búsqueda por título usando AVL"""
        titulo = buscar_titulo_var.get()
        if not titulo:
            messagebox.showwarning("Advertencia", "Ingrese un título para buscar")
            return
        
        resultados = []
        for biblioteca in red_bibliotecas.bibliotecas.values():
            try:
                # ✅ CORREGIDO: usar método correcto del controlador
                libro = biblioteca.catalogo_local.buscar_por_titulo(titulo)
                if libro:
                    resultados.append(libro)
            except Exception:
                pass
        
        mostrar_resultados_busqueda(resultados, f"Título: {titulo}")

    def buscar_por_isbn():
        """Búsqueda por ISBN usando Hash"""
        isbn = buscar_isbn_var.get()
        if not isbn:
            messagebox.showwarning("Advertencia", "Ingrese un ISBN para buscar")
            return
        
        resultados = []
        for biblioteca in red_bibliotecas.bibliotecas.values():
            try:
                # ✅ CORREGIDO: usar método correcto del controlador
                libro = biblioteca.catalogo_local.buscar_por_isbn(isbn)
                if libro:
                    resultados.append(libro)
                    break
            except Exception:
                pass
        
        mostrar_resultados_busqueda(resultados, f"ISBN: {isbn}")

    def buscar_por_genero():
        """Búsqueda por género usando B+"""
        genero = buscar_genero_var.get()
        if not genero:
            messagebox.showwarning("Advertencia", "Seleccione un género para buscar")
            return
        
        resultados = []
        for biblioteca in red_bibliotecas.bibliotecas.values():
            try:
                # ✅ CORREGIDO: usar método correcto del controlador
                libros = biblioteca.catalogo_local.buscar_por_genero(genero)
                resultados.extend(libros)
            except Exception:
                pass
        
        mostrar_resultados_busqueda(resultados, f"Género: {genero}")

    def buscar_por_rango():
        """Búsqueda por rango de fechas usando Árbol B"""
        try:
            inicio = int(anio_inicio_var.get()) if anio_inicio_var.get() else None
            fin = int(anio_fin_var.get()) if anio_fin_var.get() else None
            
            if inicio is None or fin is None:
                messagebox.showerror("Error", "Ingrese ambos años para el rango")
                return
            
            resultados = []
            for biblioteca in red_bibliotecas.bibliotecas.values():
                try:
                    # ✅ CORREGIDO: usar método correcto del controlador
                    libros_rango = biblioteca.catalogo_local.buscar_por_rango_fechas(inicio, fin)
                    resultados.extend(libros_rango)
                except Exception:
                    pass
            
            mostrar_resultados_busqueda(resultados, f"Rango: {inicio}-{fin}")
            
        except ValueError:
            messagebox.showerror("Error", "Los años deben ser números válidos")

    def mostrar_resultados_busqueda(libros, criterio):
        """Mostrar resultados en una ventana nueva"""
        if not libros:
            messagebox.showinfo("Búsqueda", f"No se encontraron libros para {criterio}")
            return
        
        ventana = tk.Toplevel()
        ventana.title(f"Resultados - {criterio}")
        ventana.geometry("800x400")
        ventana.configure(bg=BG_COLOR)
        
        frame = ttk.Frame(ventana, style='Sky.TFrame', padding=10)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text=f"Resultados para {criterio} ({len(libros)} encontrados):",
                font=('Arial', 12, 'bold'), bg=FILTER_BG).pack(pady=(0, 10))
        
        tree = ttk.Treeview(frame, columns=("Título", "Autor", "ISBN", "Año", "Género"), show='headings')
        tree.heading("Título", text="Título")
        tree.heading("Autor", text="Autor")
        tree.heading("ISBN", text="ISBN")
        tree.heading("Año", text="Año")
        tree.heading("Género", text="Género")
        
        for libro in libros:
            tree.insert("", "end", values=(
                libro.titulo, libro.autor, libro.isbn, libro.anio, libro.genero
            ))
        
        tree.pack(fill='both', expand=True)

    def calcular_ruta_optima():
        """Calcular ruta óptima entre bibliotecas"""
        origen = ruta_origen_var.get()
        destino = ruta_destino_var.get()
        
        if not origen or not destino:
            messagebox.showerror("Error", "Seleccione bibliotecas de origen y destino")
            return
        
        if origen == destino:
            messagebox.showerror("Error", "Origen y destino deben ser diferentes")
            return
        
        try:
            # ✅ CORREGIDO: grafo en lugar de grafo_red
            if criterio_var.get() == "tiempo":
                peso, ruta = red_bibliotecas.grafo.dijkstra_tiempo(origen, destino)
            else:
                peso, ruta = red_bibliotecas.grafo.dijkstra_costo(origen, destino)
            
            if ruta:
                ruta_texto = " -> ".join(ruta)
                mensaje = f"Ruta óptima ({criterio_var.get()}):\n{ruta_texto}\nPeso total: {peso}"
                messagebox.showinfo("Ruta Calculada", mensaje)
                
                # Actualizar etiqueta en la GUI
                ruta_resultado_label.config(text=f"Ruta: {ruta_texto} | Peso: {peso}")
            else:
                messagebox.showerror("Error", "No se encontró ruta entre las bibliotecas")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error calculando ruta: {e}")

    def iniciar_transferencia():
        """Iniciar transferencia de libro"""
        try:
            if not libro_enviar_var.get():
                messagebox.showerror("Error", "Seleccione un libro para transferir")
                return
            
            # Aquí implementarías la lógica de transferencia
            messagebox.showinfo("Transferencia", "Transferencia iniciada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en transferencia: {e}")

    def dibujar_grafo():
        """Dibujar grafo en el canvas"""
        grafo_canvas.delete("all")
        
        # ✅ CORREGIDO: grafo en lugar de grafo_red
        if not red_bibliotecas.grafo.nodos:
            return
        
        # Posiciones simples para visualización
        width = grafo_canvas.winfo_width() or 400
        height = grafo_canvas.winfo_height() or 300
        
        # ✅ CORREGIDO: grafo en lugar de grafo_red
        nodos = list(red_bibliotecas.grafo.nodos.keys())
        n = len(nodos)
        
        if n == 0:
            return
        
        import math
        posiciones = {}
        
        # Distribuir nodos en círculo
        for i, nodo in enumerate(nodos):
            angle = 2 * math.pi * i / n
            x = width//2 + (width//3) * math.cos(angle)
            y = height//2 + (height//3) * math.sin(angle)
            posiciones[nodo] = (x, y)
        
        # Dibujar aristas
        # ✅ CORREGIDO: grafo en lugar de grafo_red
        for nodo_origen, aristas in red_bibliotecas.grafo.nodos.items():
            if nodo_origen in posiciones:
                x1, y1 = posiciones[nodo_origen]
                for arista in aristas:
                    if arista.destino in posiciones:
                        x2, y2 = posiciones[arista.destino]
                        grafo_canvas.create_line(x1, y1, x2, y2, fill=ACCENT_COLOR, width=2)
                        
                        # Etiqueta de peso
                        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                        grafo_canvas.create_text(mx, my, text=f"{arista.tiempo}",
                                               fill="red", font=('Arial', 8, 'bold'))
        
        # Dibujar nodos
        for nodo, (x, y) in posiciones.items():
            grafo_canvas.create_oval(x-20, y-20, x+20, y+20, 
                                   fill=BUTTON_COLOR, outline=TITLE_COLOR, width=2)
            grafo_canvas.create_text(x, y, text=nodo, fill="white", 
                                   font=('Arial', 8, 'bold'))

    def cargar_csv_bibliotecas():
        """Cargar bibliotecas desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                count = red_bibliotecas.cargar_bibliotecas_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} bibliotecas cargadas")
                actualizar_comboboxes()
                dibujar_grafo()
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando bibliotecas: {e}")

    def cargar_csv_conexiones():
        """Cargar conexiones desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                count = red_bibliotecas.cargar_conexiones_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} conexiones cargadas")
                dibujar_grafo()
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando conexiones: {e}")

    def cargar_csv_libros():
        """Cargar libros desde CSV"""
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                # ✅ USAR EL MÉTODO CORRECTO DE RED_BIBLIOTECAS
                count = red_bibliotecas.cargar_libros_csv(file_path)
                messagebox.showinfo("Éxito", f"✅ {count} libros cargados")
                actualizar_catalogo_tree()
                actualizar_comboboxes()
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando libros: {e}")

    def comparar_busquedas():
        """Comparar métodos de búsqueda"""
        try:
            if not red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas para comparar")
                return
            
            # Obtener libros para prueba
            primera_bib = next(iter(red_bibliotecas.bibliotecas.values()))
            # ✅ CORREGIDO: usar método correcto
            libros = primera_bib.catalogo_local.lista_secuencial.mostrar_todos()
            
            if not libros:
                messagebox.showwarning("Advertencia", "No hay libros para comparar")
                return
            
            libro_prueba = libros[len(libros)//2]  # Libro del medio
            
            # Medir búsqueda secuencial
            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.lista_secuencial.buscar_por_titulo(libro_prueba.titulo)
            tiempo_secuencial = time.perf_counter() - inicio
            
            # Medir búsqueda AVL
            inicio = time.perf_counter()
            _ = primera_bib.catalogo_local.arbol_titulos.buscar(libro_prueba.titulo)
            tiempo_avl = time.perf_counter() - inicio
            
            # Medir búsqueda Hash
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

    def comparar_ordenamientos():
        """Comparar métodos de ordenamiento"""
        try:
            if not red_bibliotecas.bibliotecas:
                messagebox.showwarning("Advertencia", "No hay bibliotecas cargadas para comparar")
                return
            
            primera_bib = next(iter(red_bibliotecas.bibliotecas.values()))
            # ✅ CORREGIDO: usar método correcto
            libros = primera_bib.catalogo_local.lista_secuencial.mostrar_todos()
            
            if len(libros) < 2:
                messagebox.showwarning("Advertencia", "Se necesitan al menos 2 libros para comparar")
                return
            
            resultado = comparar_metodos(libros, "titulo")
            messagebox.showinfo("Resultados de Ordenamiento", resultado)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en comparación: {e}")

    def iniciar_simulacion():
        """Iniciar simulación de colas"""
        global simulacion_activa
        simulacion_activa = True
        messagebox.showinfo("Simulación", "Simulación iniciada")
        # Aquí implementarías la lógica de simulación en tiempo real

    def pausar_simulacion():
        """Pausar simulación"""
        global simulacion_activa
        simulacion_activa = False
        messagebox.showinfo("Simulación", "Simulación pausada")

    # --- 6. DASHBOARD ---
    tab_dashboard.grid_columnconfigure((0, 1, 2), weight=1)
    tab_dashboard.grid_rowconfigure((0, 1), weight=1)

    def create_info_card(parent, emoji, text_title, value_placeholder, row, col, color, command_index):
        card = tk.Frame(parent, bg=DASH_CARD_BG, bd=2, relief=tk.RAISED, cursor="hand2")
        card.grid(row=row, column=col, sticky="nsew", padx=15, pady=15)
        card.grid_columnconfigure(0, weight=1)
        
        card.bind("<Button-1>", lambda e, idx=command_index: notebook.select(idx))
        
        tk.Label(card, text=emoji, font=('Arial', 38), bg=DASH_CARD_BG, fg=color).pack(pady=(15, 0))
        tk.Label(card, text=text_title, font=('Arial', 16, 'bold'), bg=DASH_CARD_BG, fg=TITLE_COLOR).pack(pady=(0, 5))
        tk.Label(card, text=value_placeholder, font=('Georgia', 11, 'bold'), bg=DASH_CARD_BG, fg=ACCENT_COLOR).pack(pady=(5, 10))
        tk.Label(card, text="Clic para Gestionar", font=('Arial', 9, 'italic'), bg=DASH_CARD_BG, fg=BUTTON_COLOR).pack(pady=(0, 5))

    create_info_card(tab_dashboard, "📘", "Catálogo y Libro (CRUD)", "Estructuras: AVL / B+ / Hash / Listas", 0, 0, ACCENT_COLOR, 1)
    create_info_card(tab_dashboard, "🏛️", "Red de Bibliotecas", "Estructuras: Grafo Ponderado (Nodos/Aristas)", 0, 1, ACCENT_COLOR, 2)
    create_info_card(tab_dashboard, "🗺️", "Rutas y Búsqueda", "Algoritmos: Dijkstra / Búsqueda en Árboles", 0, 2, ACCENT_COLOR, 3)
    create_info_card(tab_dashboard, "⏳", "Simulación de Flujo", "Algoritmos: Colas FIFO (Ingreso, Traspaso, Salida)", 1, 0, ACCENT_COLOR, 4)
    create_info_card(tab_dashboard, "🌳", "Visualización Estructuras", "Representación: Árboles / Hash / Pilas", 1, 1, ACCENT_COLOR, 5)
    create_info_card(tab_dashboard, "📈", "Pruebas y Carga CSV", "Comparación: 5 Sorts / 3 Búsquedas (Big O)", 1, 2, ACCENT_COLOR, 6)

    # --- 7. CATÁLOGO Y LIBRO (CRUD) ---
    tab_catalogo.grid_columnconfigure((0, 1), weight=1)
    tab_catalogo.grid_rowconfigure(0, weight=1)

    crud_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    crud_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(crud_frame, text="✏️ REGISTRO DE LIBRO", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 15))

    tk.Label(crud_frame, text="Título:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=titulo_var, width=40).pack(fill='x')
    
    tk.Label(crud_frame, text="Autor:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=autor_var, width=40).pack(fill='x')
    
    tk.Label(crud_frame, text="ISBN:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=isbn_var, width=20).pack(fill='x')
    
    tk.Label(crud_frame, text="Año de publicación:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=anio_var, width=10).pack(fill='x')
    
    tk.Label(crud_frame, text="Género:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, textvariable=genero_var, width=20).pack(fill='x')

    tk.Label(crud_frame, text="Estado:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Combobox(crud_frame, textvariable=estado_var, values=["disponible", "prestado", "en_transito", "agotado"]).pack(fill='x')
    
    
    
    # ✅ AGREGAR ESTOS CAMPOS NUEVOS:
    tk.Label(crud_frame, text="Biblioteca Origen:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    biblioteca_origen_combo = ttk.Combobox(crud_frame, textvariable=biblioteca_origen_var)
    biblioteca_origen_combo.pack(fill='x')

    tk.Label(crud_frame, text="Biblioteca Destino:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    biblioteca_destino_combo = ttk.Combobox(crud_frame, textvariable=biblioteca_destino_var)
    biblioteca_destino_combo.pack(fill='x')

    tk.Label(crud_frame, text="Prioridad de Envío:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    prioridad_frame = ttk.Frame(crud_frame)
    prioridad_frame.pack(fill='x', pady=2)
    ttk.Radiobutton(prioridad_frame, text="Tiempo", variable=prioridad_var, value="tiempo").pack(side='left', padx=10)
    ttk.Radiobutton(prioridad_frame, text="Costo", variable=prioridad_var, value="costo").pack(side='left', padx=10)
    
    
    
    

    ttk.Button(crud_frame, text="➕ Agregar Libro", command=agregar_libro).pack(pady=(20, 5), fill='x')
    ttk.Button(crud_frame, text="🗑️ Eliminar Libro", command=eliminar_libro).pack(pady=5, fill='x')

    tk.Label(crud_frame, text="🔄 CONTROL DE PILAS", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(20, 10))
    ttk.Button(crud_frame, text="↩️ Deshacer Última Operación", command=rollback_operacion).pack(pady=5, fill='x')

    listado_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
    listado_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    listado_frame.grid_rowconfigure(2, weight=1)

    tk.Label(listado_frame, text="📖 LISTADO Y ALMACENAMIENTO", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    ttk.Button(listado_frame, text="🔄 Actualizar Catálogo", command=actualizar_catalogo_tree).pack(fill='x', pady=5)

    tk.Label(listado_frame, text="CATÁLOGO COMPLETO:", font=('Arial', 12, 'bold'), bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    catalog_tree = ttk.Treeview(listado_frame, columns=("Título", "Autor", "ISBN", "Estado", "Biblioteca"), show='headings')
    catalog_tree.heading("Título", text="Título")
    catalog_tree.heading("Autor", text="Autor")
    catalog_tree.heading("ISBN", text="ISBN")
    catalog_tree.heading("Estado", text="Estado")
    catalog_tree.heading("Biblioteca", text="Biblioteca")
    catalog_tree.pack(fill='both', expand=True, pady=(5, 0))

    # --- 8. GESTIÓN DE LA RED (GRAFO) ---
    tab_red.grid_columnconfigure(0, weight=1)
    tab_red.grid_columnconfigure(1, weight=3)
    tab_red.grid_rowconfigure(0, weight=1)

    config_frame_red = ttk.Frame(tab_red, style='Sky.TFrame', padding=15)
    config_frame_red.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(config_frame_red, text="🏛️ GESTIÓN DE BIBLIOTECAS", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(config_frame_red, text="Nombre:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=bib_nombre_var, width=30).pack(fill='x')
    
    tk.Label(config_frame_red, text="Ubicación:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=bib_ubicacion_var, width=30).pack(fill='x')
    
    tk.Label(config_frame_red, text="Tiempo Ingreso (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=bib_tiempo_ingreso_var, width=15).pack(fill='x')
    
    tk.Label(config_frame_red, text="Tiempo Traspaso (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=bib_tiempo_traspaso_var, width=15).pack(fill='x')
    
    tk.Label(config_frame_red, text="Intervalo Despacho (s):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=bib_intervalo_despacho_var, width=15).pack(fill='x')
        
    ttk.Button(config_frame_red, text="➕ Crear Biblioteca", command=agregar_biblioteca).pack(pady=(15, 5), fill='x')

    tk.Label(config_frame_red, text="🔗 GESTIÓN DE CONEXIONES", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(20, 10))

    tk.Label(config_frame_red, text="Origen:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    origen_combo = ttk.Combobox(config_frame_red, textvariable=origen_var)
    origen_combo.pack(fill='x')
    
    tk.Label(config_frame_red, text="Destino:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    destino_combo = ttk.Combobox(config_frame_red, textvariable=destino_var)
    destino_combo.pack(fill='x')
    
    tk.Label(config_frame_red, text="Tiempo:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=tiempo_conexion_var).pack(fill='x')
    
    tk.Label(config_frame_red, text="Costo:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, textvariable=costo_conexion_var).pack(fill='x')

    ttk.Checkbutton(config_frame_red, text="Conexión Bidireccional", variable=bidireccional_var).pack(anchor='w', pady=5)
    ttk.Button(config_frame_red, text="🔗 Crear Conexión", command=agregar_conexion).pack(pady=10, fill='x')

    grafo_frame = ttk.Frame(tab_red, style='Sky.TFrame', padding=10)
    grafo_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(grafo_frame, text="🌍 RED DE BIBLIOTECAS", font=('Arial', 16, 'bold'), fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    grafo_canvas = tk.Canvas(grafo_frame, bg=DASH_CARD_BG, highlightthickness=1, highlightbackground=TITLE_COLOR)
    grafo_canvas.pack(fill='both', expand=True, pady=5)

    # --- 9. BÚSQUEDA Y RUTAS ÓPTIMAS ---
    tab_busqueda_rutas.grid_columnconfigure((0, 1), weight=1)
    tab_busqueda_rutas.grid_rowconfigure(1, weight=1)

    search_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
    search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(search_frame, text="🔍 BÚSQUEDA AVANZADA", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(search_frame, text="Buscar por Título (AVL):", bg=FILTER_BG).pack(anchor='w')
    search_title_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    search_title_frame.pack(fill='x')
    ttk.Entry(search_title_frame, textvariable=buscar_titulo_var).pack(side='left', fill='x', expand=True)
    ttk.Button(search_title_frame, text="Buscar", command=buscar_por_titulo).pack(side='left', padx=3)

    tk.Label(search_frame, text="Buscar por ISBN (HASH):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    search_isbn_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    search_isbn_frame.pack(fill='x')
    ttk.Entry(search_isbn_frame, textvariable=buscar_isbn_var).pack(side='left', fill='x', expand=True)
    ttk.Button(search_isbn_frame, text="Buscar", command=buscar_por_isbn).pack(side='left', padx=3)

    tk.Label(search_frame, text="Buscar por Género (B+):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    search_genre_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    search_genre_frame.pack(fill='x')
    buscar_genero_combo = ttk.Combobox(search_genre_frame, textvariable=buscar_genero_var)
    buscar_genero_combo.pack(side='left', fill='x', expand=True)
    ttk.Button(search_genre_frame, text="Buscar", command=buscar_por_genero).pack(side='left', padx=3)

    tk.Label(search_frame, text="Rango de Fechas (Árbol B):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    search_date_frame = ttk.Frame(search_frame, style='Sky.TFrame')
    search_date_frame.pack(fill='x')
    ttk.Entry(search_date_frame, textvariable=anio_inicio_var, width=10).pack(side='left', padx=3)
    tk.Label(search_date_frame, text="a", bg=FILTER_BG).pack(side='left')
    ttk.Entry(search_date_frame, textvariable=anio_fin_var, width=10).pack(side='left', padx=3)
    ttk.Button(search_date_frame, text="Buscar", command=buscar_por_rango).pack(side='left', padx=3)

    rutas_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
    rutas_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(rutas_frame, text="🗺️ CÁLCULO DE RUTA ÓPTIMA", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(rutas_frame, text="Biblioteca Origen:", bg=FILTER_BG).pack(anchor='w')
    ruta_origen_combo = ttk.Combobox(rutas_frame, textvariable=ruta_origen_var)
    ruta_origen_combo.pack(fill='x', pady=2)
    
    tk.Label(rutas_frame, text="Biblioteca Destino:", bg=FILTER_BG).pack(anchor='w')
    ruta_destino_combo = ttk.Combobox(rutas_frame, textvariable=ruta_destino_var)
    ruta_destino_combo.pack(fill='x', pady=2)

    tk.Label(rutas_frame, text="Criterio de Optimización:", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
    criterio_options = ttk.Frame(rutas_frame, style='Sky.TFrame')
    criterio_options.pack(fill='x')
    ttk.Radiobutton(criterio_options, text="Tiempo", variable=criterio_var, value="tiempo").pack(side='left', padx=5)
    ttk.Radiobutton(criterio_options, text="Costo", variable=criterio_var, value="costo").pack(side='left', padx=5)

    ttk.Button(rutas_frame, text="🧮 Calcular Ruta Óptima", command=calcular_ruta_optima).pack(pady=(15, 5), fill='x')

    ruta_resultado_label = tk.Label(rutas_frame, text="Ruta: [No calculada]", bg=FILTER_BG, fg=ACCENT_COLOR)
    ruta_resultado_label.pack(anchor='w', pady=5)

    results_busqueda_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=10)
    results_busqueda_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    
    tk.Label(results_busqueda_frame, text="VISUALIZACIÓN DE RUTA", font=('Arial', 14, 'bold'), fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
    ruta_canvas = tk.Canvas(results_busqueda_frame, bg=DASH_CARD_BG, highlightthickness=1, highlightbackground=TITLE_COLOR)
    ruta_canvas.pack(fill='both', expand=True)

    # --- 10. SIMULACIÓN Y COLAS ---
    tab_simulacion.grid_columnconfigure(0, weight=1) 
    tab_simulacion.grid_rowconfigure(2, weight=1) 

    sim_controls = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=15)
    sim_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    
    tk.Label(sim_controls, text="⚙️ CONTROLES DE SIMULACIÓN", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="▶️ Iniciar", command=iniciar_simulacion).pack(side='left', padx=10)
    ttk.Button(sim_controls, text="⏸️ Pausar", command=pausar_simulacion).pack(side='left', padx=10)

    metrics_frame = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    metrics_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    
    tk.Label(metrics_frame, text="MÉTRICAS DE DESPACHO:", font=('Arial', 12, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')
    metricas_label = tk.Label(metrics_frame, text="Estado: Detenido | Transferencias activas: 0", bg=FILTER_BG, fg=ACCENT_COLOR)
    metricas_label.pack(anchor='w', pady=5)

    colas_container = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
    colas_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    
    tk.Label(colas_container, text="🚦 ESTADO DE COLAS POR BIBLIOTECA", font=('Arial', 16, 'bold'), fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=10)
    tk.Label(colas_container, text="[Las colas se mostrarán cuando se carguen bibliotecas y se inicie la simulación]", 
             font=('Arial', 12), pady=20, bg=FILTER_BG).pack(fill='x')

    # --- 11. VISUALIZACIÓN ESTRUCTURAS ---
    tk.Label(tab_visualizacion, text="🌳 REPRESENTACIÓN GRÁFICA DE ESTRUCTURAS", 
             font=('Georgia', 18, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=20)

    vis_buttons = ttk.Frame(tab_visualizacion, style='Sky.TFrame')
    vis_buttons.pack(pady=10)
    ttk.Button(vis_buttons, text="Ver Árbol AVL").pack(side='left', padx=5)
    ttk.Button(vis_buttons, text="Ver Árbol B").pack(side='left', padx=5)
    ttk.Button(vis_buttons, text="Ver Árbol B+").pack(side='left', padx=5)
    ttk.Button(vis_buttons, text="Ver Tabla Hash").pack(side='left', padx=5)

    vis_canvas = tk.Canvas(tab_visualizacion, bg=DASH_CARD_BG, highlightthickness=1, highlightbackground=TITLE_COLOR)
    vis_canvas.pack(fill='both', expand=True, padx=20, pady=10)

    # --- 12. PRUEBAS DE RENDIMIENTO Y CARGA CSV ---
    tab_pruebas_carga.grid_columnconfigure((0, 1), weight=1)
    tab_pruebas_carga.grid_rowconfigure(0, weight=1)

    comp_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    comp_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(comp_frame, text="⏱️ PRUEBAS DE RENDIMIENTO", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(comp_frame, text="COMPARACIÓN DE BÚSQUEDAS:", font=('Arial', 12, 'bold'), bg=FILTER_BG).pack(pady=(5, 5), anchor='w')
    ttk.Button(comp_frame, text="Comparar 3 Métodos de Búsqueda", command=comparar_busquedas).pack(pady=5, fill='x')

    tk.Label(comp_frame, text="COMPARACIÓN DE ORDENAMIENTOS:", font=('Arial', 12, 'bold'), bg=FILTER_BG).pack(pady=(15, 5), anchor='w')
    ttk.Button(comp_frame, text="Comparar 5 Tipos de Ordenamiento", command=comparar_ordenamientos).pack(pady=5, fill='x')

    carga_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
    carga_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    tk.Label(carga_frame, text="📂 CARGA MASIVA DE DATOS (CSV)", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

    tk.Label(carga_frame, text="Seleccione los archivos CSV:", font=('Arial', 12), bg=FILTER_BG).pack(anchor='w', pady=5)
    ttk.Button(carga_frame, text="⬆️ Cargar Catálogo de Libros", command=cargar_csv_libros).pack(pady=5, fill='x')
    ttk.Button(carga_frame, text="⬆️ Cargar Bibliotecas", command=cargar_csv_bibliotecas).pack(pady=5, fill='x')
    ttk.Button(carga_frame, text="⬆️ Cargar Conexiones", command=cargar_csv_conexiones).pack(pady=5, fill='x')

    # Configurar eventos de redimensionado para el canvas del grafo
    def on_canvas_configure(event):
        if event.widget == grafo_canvas:
            root.after(100, dibujar_grafo)  # Redibujar después de un breve delay
    
    grafo_canvas.bind('<Configure>', on_canvas_configure)

    # Inicializar componentes
    actualizar_comboboxes()
    
    # Iniciar la GUI
    root.mainloop()

# Función para usar desde main.py
if __name__ == "__main__":
    iniciar_gui()