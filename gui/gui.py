import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Colores mágicos
BG_COLOR = "#e6f0ff"        # Fondo principal (Azul claro/celeste)
TITLE_COLOR = "#2a2a72"     # Color del título (Azul oscuro/índigo)
BUTTON_COLOR = "#4a90e2"    # Color del botón (Azul brillante)
FILTER_BG = "#d9e4f5"       # Fondo de los filtros (Azul muy claro - para marcos/fondo)
ACCENT_COLOR = "#1e6bbd"    # Color de acento (Azul profundo)
DASH_CARD_BG = "#ffffff"    # Fondo de tarjetas y Canvas (Blanco)

# --- 1. CONFIGURACIÓN INICIAL Y ESTILOS ---

root = tk.Tk()
root.title("📚 Biblioteca Mágica Alrededor del Mundo - Sistema de Gestión de Red")
root.geometry("1200x800")
root.configure(bg=BG_COLOR)

style = ttk.Style(root)
style.theme_use("clam") 

# Estilos ttk
style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), foreground=TITLE_COLOR, padding=[15, 5])
style.map('TNotebook.Tab', background=[('selected', FILTER_BG)], foreground=[('selected', ACCENT_COLOR)])
style.configure('Sky.TFrame', background=FILTER_BG)
style.configure('TButton', font=('Arial', 10, 'bold'), foreground='white', background=BUTTON_COLOR, padding=6, relief='flat')
style.map('TButton', background=[('active', ACCENT_COLOR)])

# --- 2. LAYOUT PRINCIPAL (Título y Notebook) ---

title = tk.Label(root, text="✨ Sistema de Gestión Arcana ✨", 
                 font=("Georgia", 26, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
title.pack(pady=(20, 10))

notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=20, expand=True, fill="both")

# --- 3. CREACIÓN DE PESTAÑAS (6 Pestañas Requeridas + Dashboard) ---
tab_dashboard = ttk.Frame(notebook, style='Sky.TFrame')
tab_catalogo = ttk.Frame(notebook, style='Sky.TFrame')
tab_red = ttk.Frame(notebook, style='Sky.TFrame')
tab_busqueda_rutas = ttk.Frame(notebook, style='Sky.TFrame') # Nueva pestaña separada
tab_simulacion = ttk.Frame(notebook, style='Sky.TFrame')
tab_visualizacion = ttk.Frame(notebook, style='Sky.TFrame')
tab_pruebas_carga = ttk.Frame(notebook, style='Sky.TFrame')

# Asignación de Pestañas y sus Índices (0 a 6)
notebook.add(tab_dashboard, text="🏠 Inicio/Dashboard") # Index 0
notebook.add(tab_catalogo, text="📚 Catálogo y Libro (CRUD)") # Index 1
notebook.add(tab_red, text="🌐 Gestión de la Red (Grafo)") # Index 2
notebook.add(tab_busqueda_rutas, text="🔍 Búsqueda y Rutas Óptimas") # Index 3
notebook.add(tab_simulacion, text="📦 Simulación y Colas") # Index 4
notebook.add(tab_visualizacion, text="📊 Visualización Estructuras") # Index 5
notebook.add(tab_pruebas_carga, text="⚙️ Pruebas de Rendimiento y Carga (CSV)") # Index 6


# --- 4. DASHBOARD (INICIO) ---
tab_dashboard.grid_columnconfigure((0, 1, 2), weight=1)
tab_dashboard.grid_rowconfigure((0, 1), weight=1)

# Función con CORRECCIÓN DE REDIRECCIÓN
def create_info_card(parent, title, value_placeholder, row, col, color, command_index):
    card = tk.Frame(parent, bg=DASH_CARD_BG, bd=2, relief=tk.RAISED, cursor="hand2")
    card.grid(row=row, column=col, sticky="nsew", padx=15, pady=15)
    card.grid_columnconfigure(0, weight=1)
    
    # *** REDIRECCIÓN FUNCIONAL ***
    card.bind("<Button-1>", lambda e, idx=command_index: notebook.select(idx))
    
    # Uso de tk.Label para colores de fondo
    tk.Label(card, text=title, font=('Arial', 14, 'bold'), bg=DASH_CARD_BG, fg=color).pack(pady=(15, 5))
    tk.Label(card, text=value_placeholder, font=('Georgia', 28, 'bold'), bg=DASH_CARD_BG, fg=TITLE_COLOR).pack(pady=(5, 15))
    tk.Label(card, text="Clic para Gestionar", font=('Arial', 10, 'italic'), bg=DASH_CARD_BG, fg=BUTTON_COLOR).pack(pady=(0, 5))

# Creación de Tarjetas (Mapeo a los 6 índices de pestaña)
# Índices: 1: Catálogo, 2: Red, 3: Búsqueda/Rutas, 4: Simulación, 5: Visualización, 6: Pruebas/Carga
create_info_card(tab_dashboard, "📚 Catálogo (CRUD)", "AVL/B+/Hash", 0, 0, ACCENT_COLOR, command_index=1)
create_info_card(tab_dashboard, "🏛️ Red de Bibliotecas", "Grafo Ponderado", 0, 1, ACCENT_COLOR, command_index=2)
create_info_card(tab_dashboard, "🔍 Rutas y Búsqueda Avanzada", "Dijkstra/Hash/B", 0, 2, ACCENT_COLOR, command_index=3)
create_info_card(tab_dashboard, "📦 Simulación de Flujo", "Colas FIFO (3 Tipos)", 1, 0, ACCENT_COLOR, command_index=4)
create_info_card(tab_dashboard, "📊 Visualización Estructuras", "Árboles/Hash/Pilas", 1, 1, ACCENT_COLOR, command_index=5)
create_info_card(tab_dashboard, "⚙️ Rendimiento y CSV", "5 Sorts / 3 Búsquedas", 1, 2, ACCENT_COLOR, command_index=6)


# --- 5. PESTAÑAS DETALLADAS ---

# 5.1. 📚 Catálogo y Libro (CRUD y Pilas)
tab_catalogo.grid_columnconfigure((0, 1), weight=1)
tab_catalogo.grid_rowconfigure(0, weight=1)

# --- 5.1.1. Registro y Operaciones CRUD ---
crud_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
crud_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

tk.Label(crud_frame, text="✏️ REGISTRO DE LIBRO", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 15))

# Campos de Atributos del Libro (Requisito: Título, Autor, ISBN, Año, Género, Estado)
atributos = [("Título", 40), ("Autor", 40), ("ISBN", 20), ("Año de publicación", 10), ("Género", 20)]
for label_text, width in atributos:
    tk.Label(crud_frame, text=f"{label_text}:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
    ttk.Entry(crud_frame, width=width).pack(fill='x')

tk.Label(crud_frame, text="Estado:", bg=FILTER_BG).pack(anchor='w', pady=(5, 0))
ttk.Combobox(crud_frame, values=["Disponible", "Prestado", "En Tránsito", "Agotado"]).pack(fill='x')

# Botones de Acción (Requisito: Inserción/Eliminación en TODAS las estructuras)
ttk.Button(crud_frame, text="➕ Agregar Libro (AVL, B, B+, Hash, Lista)").pack(pady=(20, 5), fill='x')
ttk.Button(crud_frame, text="🗑️ Eliminar Libro (De todas las estructuras)").pack(pady=5, fill='x')
tk.Label(crud_frame, text="[Validación de ISBN requerida]", font=('Arial', 9, 'italic'), bg=FILTER_BG).pack(pady=5)

tk.Label(crud_frame, text="🔄 CONTROL DE PILAS", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(20, 10))
ttk.Button(crud_frame, text="↩️ Deshacer Última Operación (Pila Rollback)").pack(pady=5, fill='x')
ttk.Button(crud_frame, text="➕ Apilar Libro Devuelto (Pila Devoluciones)").pack(pady=5, fill='x')


# --- 5.1.2. Listado del Catálogo (Listas Enlazadas) ---
listado_frame = ttk.Frame(tab_catalogo, style='Sky.TFrame', padding=15)
listado_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
listado_frame.grid_rowconfigure(2, weight=1) # Treeview se expande

tk.Label(listado_frame, text="📖 LISTADO Y ALMACENAMIENTO", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

# Visualización (Listas Enlazadas)
tk.Label(listado_frame, text="Almacenamiento Principal: Listas Enlazadas/Arreglos", font=('Arial', 10), bg=FILTER_BG).pack(anchor='w', pady=5)
tk.Label(listado_frame, text="LISTAR (Recorrido In-Order AVL):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
ttk.Button(listado_frame, text="Listar Libros por Título").pack(fill='x', pady=5)


# Tabla de Resultados
tk.Label(listado_frame, text="CATÁLOGO COMPLETO:", font=('Arial', 12, 'bold'), bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
catalog_tree = ttk.Treeview(listado_frame, columns=("Título", "Autor", "ISBN", "Estado"), show='headings')
catalog_tree.heading("Título", text="Título")
catalog_tree.pack(fill='both', expand=True, pady=(5, 0))


# 5.2. 🌐 Gestión de la Red (Grafo)
tab_red.grid_columnconfigure(0, weight=1)
tab_red.grid_columnconfigure(1, weight=3)
tab_red.grid_rowconfigure(0, weight=1)

# --- 5.2.1. Gestión de Nodos/Aristas ---
config_frame_red = ttk.Frame(tab_red, style='Sky.TFrame', padding=15)
config_frame_red.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

tk.Label(config_frame_red, text="🏛️ GESTIÓN DE BIBLIOTECAS (Nodos)", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

# Campos de Propiedades Configurables del Nodo (Requisito: T. Ingreso, T. Traspaso, I. Despacho)
node_props = [("Nombre", 30), ("Ubicación", 30), ("Tiempo Ingreso (s)", 15), 
              ("Tiempo Traspaso (s)", 15), ("Intervalo Despacho (s)", 15)]
for label_text, width in node_props:
    tk.Label(config_frame_red, text=f"{label_text}:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
    ttk.Entry(config_frame_red, width=width).pack(fill='x')
    
ttk.Button(config_frame_red, text="➕ Crear / Modificar Biblioteca").pack(pady=(15, 5), fill='x')
ttk.Button(config_frame_red, text="🗑️ Eliminar Biblioteca").pack(pady=(5, 15), fill='x')

tk.Label(config_frame_red, text="🔗 GESTIÓN DE CONEXIONES (Aristas)", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

# Campos de Propiedades de la Arista (Requisito: Origen, Destino, Peso (Tiempo/Costo), Bidireccionalidad)
tk.Label(config_frame_red, text="Origen:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
ttk.Combobox(config_frame_red).pack(fill='x')
tk.Label(config_frame_red, text="Destino:", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
ttk.Combobox(config_frame_red).pack(fill='x')
tk.Label(config_frame_red, text="Peso (Tiempo/Costo):", bg=FILTER_BG).pack(anchor='w', pady=(3, 0))
ttk.Entry(config_frame_red).pack(fill='x')

bidirectional_var = tk.BooleanVar()
ttk.Checkbutton(config_frame_red, text="Conexión Bidireccional", variable=bidirectional_var).pack(anchor='w', pady=5)
ttk.Button(config_frame_red, text="🔗 Crear / Actualizar Conexión").pack(pady=10, fill='x')


# --- 5.2.2. Visualización del Grafo ---
grafo_frame = ttk.Frame(tab_red, style='Sky.TFrame', padding=10)
grafo_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

tk.Label(grafo_frame, text="🌍 RED DE BIBLIOTECAS (GRAFO PONDERADO)", font=('Arial', 16, 'bold'), fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=(0, 10))
grafo_canvas = tk.Canvas(grafo_frame, bg=DASH_CARD_BG, highlightthickness=1, highlightbackground=TITLE_COLOR)
grafo_canvas.pack(fill='both', expand=True, pady=5)


# 5.3. 🔍 Búsqueda y Rutas Óptimas (Separada del Catálogo)
tab_busqueda_rutas.grid_columnconfigure((0, 1), weight=1)
tab_busqueda_rutas.grid_rowconfigure(1, weight=1)

# --- 5.3.1. Búsqueda Avanzada (AVL, Hash, B+, B) ---
search_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

tk.Label(search_frame, text="🔍 BÚSQUEDA AVANZADA", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

# Búsqueda por Criterios
tk.Label(search_frame, text="Buscar por Título (AVL):", bg=FILTER_BG).pack(anchor='w')
search_title_frame = ttk.Frame(search_frame, style='Sky.TFrame')
search_title_frame.pack(fill='x')
ttk.Entry(search_title_frame).pack(side='left', fill='x', expand=True)
ttk.Button(search_title_frame, text="Buscar Título").pack(side='left', padx=3)

tk.Label(search_frame, text="Buscar por ISBN (HASH):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
search_isbn_frame = ttk.Frame(search_frame, style='Sky.TFrame')
search_isbn_frame.pack(fill='x')
ttk.Entry(search_isbn_frame).pack(side='left', fill='x', expand=True)
ttk.Button(search_isbn_frame, text="Buscar ISBN").pack(side='left', padx=3)

tk.Label(search_frame, text="Buscar por Género (Árbol B+):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
search_genre_frame = ttk.Frame(search_frame, style='Sky.TFrame')
search_genre_frame.pack(fill='x')
ttk.Combobox(search_genre_frame, values=["Fantasía", "Historia", "Ciencia"]).pack(side='left', fill='x', expand=True)
ttk.Button(search_genre_frame, text="Buscar Género").pack(side='left', padx=3)

tk.Label(search_frame, text="Buscar por Rango de Fechas (Árbol B):", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
search_date_frame = ttk.Frame(search_frame, style='Sky.TFrame')
search_date_frame.pack(fill='x')
ttk.Entry(search_date_frame, width=10).pack(side='left', padx=3)
tk.Label(search_date_frame, text="a", bg=FILTER_BG).pack(side='left')
ttk.Entry(search_date_frame, width=10).pack(side='left', padx=3)
ttk.Button(search_date_frame, text="Filtrar Rango").pack(side='left', padx=3)


# --- 5.3.2. Rutas Óptimas ---
rutas_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=15)
rutas_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

tk.Label(rutas_frame, text="🗺️ CÁLCULO DE RUTA ÓPTIMA", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

tk.Label(rutas_frame, text="Libro a Enviar:", bg=FILTER_BG).pack(anchor='w')
ttk.Combobox(rutas_frame, values=["Libro XYZ"]).pack(fill='x', pady=2)
tk.Label(rutas_frame, text="Biblioteca Origen:", bg=FILTER_BG).pack(anchor='w')
ttk.Combobox(rutas_frame).pack(fill='x', pady=2)
tk.Label(rutas_frame, text="Biblioteca Destino:", bg=FILTER_BG).pack(anchor='w')
ttk.Combobox(rutas_frame).pack(fill='x', pady=2)

tk.Label(rutas_frame, text="Criterio de Optimización:", bg=FILTER_BG).pack(anchor='w', pady=(10, 0))
criterio_var = tk.StringVar(value="Tiempo Mínimo")
criterio_options = ttk.Frame(rutas_frame, style='Sky.TFrame')
criterio_options.pack(fill='x')
ttk.Radiobutton(criterio_options, text="Tiempo Mínimo", variable=criterio_var, value="Tiempo Mínimo").pack(side='left', padx=5)
ttk.Radiobutton(criterio_options, text="Costo Mínimo", variable=criterio_var, value="Costo Mínimo").pack(side='left', padx=5)

ttk.Button(rutas_frame, text="🧮 Calcular Ruta y Exportar Libro").pack(pady=(15, 5), fill='x')

tk.Label(rutas_frame, text="ESTADO DEL LIBRO: 'En Tránsito'", font=('Arial', 10, 'bold'), fg='red', bg=FILTER_BG).pack(pady=5)
tk.Label(rutas_frame, text="[Muestra aquí la Ruta calculada (nodos intermedios y costo)]", bg=FILTER_BG, fg=ACCENT_COLOR).pack(anchor='w')


# --- 5.3.3. Área de Resultados de Búsqueda y Rutas ---
results_busqueda_frame = ttk.Frame(tab_busqueda_rutas, style='Sky.TFrame', padding=10)
results_busqueda_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
tk.Label(results_busqueda_frame, text="VISUALIZACIÓN DE RUTA Y RESULTADOS", font=('Arial', 14, 'bold'), fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

ruta_canvas = tk.Canvas(results_busqueda_frame, bg=DASH_CARD_BG, highlightthickness=1, highlightbackground=TITLE_COLOR)
ruta_canvas.pack(fill='both', expand=True)


# 5.4. 📦 Simulación y Colas
tab_simulacion.grid_columnconfigure(0, weight=1) 
tab_simulacion.grid_rowconfigure(2, weight=1) 

# --- 5.4.1. Controles de Simulación ---
sim_controls = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=15)
sim_controls.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
tk.Label(sim_controls, text="⚙️ CONTROLES DE SIMULACIÓN", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(side='left', padx=10)
ttk.Button(sim_controls, text="▶️ Iniciar Simulación").pack(side='left', padx=10)
ttk.Button(sim_controls, text="⏸️ Pausar Simulación").pack(side='left', padx=10)
ttk.Button(sim_controls, text="🛑 Detener Simulación").pack(side='left', padx=10)


# --- 5.4.2. Métricas de Tiempo ---
metrics_frame = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
metrics_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
tk.Label(metrics_frame, text="MÉTRICAS DE DESPACHO:", font=('Arial', 12, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(anchor='w')
tk.Label(metrics_frame, text="ETA del Libro: [Calculado dinámicamente] | Próximo Despacho: [Tiempo] | Capacidad de Nodos: [Info]", 
         bg=FILTER_BG, fg=ACCENT_COLOR).pack(anchor='w', pady=5)


# --- 5.4.3. Visualización de Colas (3 Colas por Biblioteca) ---
colas_container = ttk.Frame(tab_simulacion, style='Sky.TFrame', padding=10)
colas_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
tk.Label(colas_container, text="🚦 ESTADO DE COLAS POR BIBLIOTECA (Ingreso, Traspaso, Salida)", font=('Arial', 16, 'bold'), fg=ACCENT_COLOR, bg=FILTER_BG).pack(pady=10)
tk.Label(colas_container, text="[Área para generar dinámicamente 3 contenedores de cola (listas) por cada biblioteca]", 
         font=('Arial', 12), pady=20, bg=FILTER_BG).pack(fill='x')


# 5.5. 📊 Visualización Estructuras
tk.Label(tab_visualizacion, text="🌳 REPRESENTACIÓN GRÁFICA DE ESTRUCTURAS", 
         font=('Georgia', 18, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=20)

# Botones de Selección
vis_buttons = ttk.Frame(tab_visualizacion, style='Sky.TFrame')
vis_buttons.pack(pady=10)
ttk.Button(vis_buttons, text="Ver Árbol AVL (Título)").pack(side='left', padx=5)
ttk.Button(vis_buttons, text="Ver Árbol B (Rango Fechas)").pack(side='left', padx=5)
ttk.Button(vis_buttons, text="Ver Árbol B+ (Género)").pack(side='left', padx=5)
ttk.Button(vis_buttons, text="Ver Tabla Hash (ISBN)").pack(side='left', padx=5)
ttk.Button(vis_buttons, text="Ver Pilas (Devolución/Rollback)").pack(side='left', padx=5)

# Canvas para dibujar (Árboles/Hash)
vis_canvas = tk.Canvas(tab_visualizacion, bg=DASH_CARD_BG, highlightthickness=1, highlightbackground=TITLE_COLOR)
vis_canvas.pack(fill='both', expand=True, padx=20, pady=10)
tk.Label(tab_visualizacion, text="[El Canvas debe mostrar la estructura con sus claves ordenadas/colisiones]", 
         font=('Arial', 10, 'italic'), bg=FILTER_BG).pack()


# 5.6. ⚙️ Pruebas de Rendimiento y Carga (CSV)
tab_pruebas_carga.grid_columnconfigure((0, 1), weight=1)
tab_pruebas_carga.grid_rowconfigure(0, weight=1)

# --- 5.6.1. Pruebas de Rendimiento (Izquierda) ---
comp_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
comp_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

tk.Label(comp_frame, text="⏱️ PRUEBAS DE RENDIMIENTO Y BIG O", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

# Búsqueda (Requisito: Secuencial vs. Binaria vs. Hash)
tk.Label(comp_frame, text="COMPARACIÓN DE BÚSQUEDAS:", font=('Arial', 12, 'bold'), bg=FILTER_BG).pack(pady=(5, 5), anchor='w')
ttk.Button(comp_frame, text="Ejecutar y Comparar 3 Métodos de Búsqueda").pack(pady=5, fill='x')

# Ordenamiento (Requisito: 5 Métodos)
tk.Label(comp_frame, text="COMPARACIÓN DE ORDENAMIENTOS:", font=('Arial', 12, 'bold'), bg=FILTER_BG).pack(pady=(15, 5), anchor='w')
ttk.Button(comp_frame, text="Ejecutar y Comparar 5 Tipos de Ordenamiento (Quick, Shell, etc.)").pack(pady=5, fill='x')

# Resultados
tk.Label(comp_frame, text="RESULTADOS (Tiempos y Complejidad):", font=('Arial', 12, 'bold'), bg=FILTER_BG).pack(pady=(15, 5), anchor='w')
tk.Label(comp_frame, text="[Aquí se mostrarán los tiempos de ejecución y la documentación de Big O]", font=('Arial', 9), bg=FILTER_BG).pack(pady=5)


# --- 5.6.2. Carga de Archivos CSV (Derecha) ---
carga_frame = ttk.Frame(tab_pruebas_carga, style='Sky.TFrame', padding=15)
carga_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

tk.Label(carga_frame, text="📂 CARGA MASIVA DE DATOS (CSV)", font=('Arial', 14, 'bold'), fg=TITLE_COLOR, bg=FILTER_BG).pack(pady=(0, 10))

def open_csv_dialog(data_type):
    file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        # Lógica de Validación y Carga
        messagebox.showinfo("Carga de Datos", f"Cargando {data_type} desde: {file_path}. Validando formato e ignorando errores...")

# Botones de Carga (Requisito: 3 archivos CSV)
tk.Label(carga_frame, text="Seleccione los archivos para la carga inicial:", font=('Arial', 12), bg=FILTER_BG).pack(anchor='w', pady=5)
ttk.Button(carga_frame, text="⬆️ Cargar Catálogo de Libros (CSV)", command=lambda: open_csv_dialog("Catálogo")).pack(pady=5, fill='x')
ttk.Button(carga_frame, text="⬆️ Cargar Bibliotecas (CSV)", command=lambda: open_csv_dialog("Bibliotecas")).pack(pady=5, fill='x')
ttk.Button(carga_frame, text="⬆️ Cargar Conexiones (CSV)", command=lambda: open_csv_dialog("Conexiones")).pack(pady=5, fill='x')

tk.Label(carga_frame, text="[El sistema debe validar el formato CSV e ignorar líneas mal formateadas]", 
         font=('Arial', 10, 'italic'), bg=FILTER_BG).pack(pady=15)

root.mainloop()