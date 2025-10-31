import tkinter as tk
from tkinter import ttk

# Colores mágicos
BG_COLOR = "#e6f0ff"
TITLE_COLOR = "#2a2a72"
BUTTON_COLOR = "#4a90e2"
FILTER_BG = "#d9e4f5"

# Ventana principal
root = tk.Tk()
root.title("Biblioteca Arcana")
root.geometry("700x500")
root.configure(bg=BG_COLOR)

# Título
title = tk.Label(root, text="📚 Biblioteca Arcana", font=("Georgia", 24, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
title.pack(pady=20)

# Marco de búsqueda
search_frame = tk.Frame(root, bg=BG_COLOR)
search_frame.pack(pady=10)

search_entry = ttk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=10)

search_button = ttk.Button(search_frame, text="Buscar")
search_button.pack(side=tk.LEFT)

# Marco de filtros
filters_frame = tk.Frame(root, bg=BG_COLOR)
filters_frame.pack(pady=30)

def create_filter(icon, text):
    frame = tk.Frame(filters_frame, bg=FILTER_BG, relief=tk.RIDGE, bd=2)
    frame.pack(side=tk.LEFT, padx=10)
    label_icon = tk.Label(frame, text=icon, font=("Arial", 24), bg=FILTER_BG)
    label_icon.pack(pady=5)
    label_text = tk.Label(frame, text=text, font=("Arial", 10, "bold"), bg=FILTER_BG)
    label_text.pack(pady=5)

create_filter("🧑‍🎓", "Filtrar por Autor")
create_filter("📘", "Filtrar por Materia")
create_filter("📂", "Filtrar por Formato")
create_filter("📜", "Archivos Antiguos")

# Llamado a la acción
cta = tk.Label(root, text="✨ Explora el convelmecto creado por studiantas ✨", font=("Comic Sans MS", 12), bg=BG_COLOR, fg="#444")
cta.pack(pady=40)

root.mainloop()
