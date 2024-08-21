import tkinter as tk
from tkinter import ttk
from mod_funciones import agregar_indice, eliminar_indice, actualizar_tabla, sumar_ganancia

# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Índices")

# Crear un contenedor con un margen de 5 píxeles
frame = tk.Frame(root, padx=5, pady=5)
frame.grid(sticky="nsew")

# Input para el índice
tk.Label(frame, text="Índice:").grid(row=0, column=0, padx=5, pady=5)
entry_indice = tk.Entry(frame)
entry_indice.grid(row=0, column=1, padx=5, pady=5)

# Inputs para los datos del índice en una fila
tk.Label(frame, text="Precio:").grid(row=0, column=2, padx=5, pady=5)
entry_precio = tk.Entry(frame)
entry_precio.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame, text="Dividendo:").grid(row=0, column=4, padx=5, pady=5)
entry_dividendo = tk.Entry(frame)
entry_dividendo.grid(row=0, column=5, padx=5, pady=5)

tk.Label(frame, text="Pagas:").grid(row=0, column=6, padx=5, pady=5)
entry_pagas = tk.Entry(frame)
entry_pagas.grid(row=0, column=7, padx=5, pady=5)

tk.Label(frame, text="Rendimiento:").grid(row=0, column=8, padx=5, pady=5)
entry_rendimiento = tk.Entry(frame)
entry_rendimiento.grid(row=0, column=9, padx=5, pady=5)

tk.Label(frame, text="Mi Ganancia:").grid(row=0, column=10, padx=5, pady=5)
entry_ganancia = tk.Entry(frame)
entry_ganancia.grid(row=0, column=11, padx=5, pady=5)

# Botones para agregar y eliminar
tk.Button(frame, text="Agregar Índice", command=lambda: agregar_indice(entry_indice, entry_precio, entry_dividendo, entry_pagas, entry_rendimiento, entry_ganancia, tree)).grid(row=1, column=0, columnspan=6, pady=5, padx=5)
tk.Button(frame, text="Eliminar Índice", command=lambda: eliminar_indice(entry_indice, tree)).grid(row=1, column=6, columnspan=6, pady=5, padx=5)
tk.Button(frame, text="Sumar Ganancia", command=lambda: sumar_ganancia(entry_indice, entry_precio, entry_dividendo, entry_pagas, entry_rendimiento, entry_ganancia, tree)).grid(row=1, column=11, pady=5, padx=5)

# Crear la tabla
tree = ttk.Treeview(frame, columns=("Indice", "Precio", "Dividendo", "Pagas", "Rendimiento", "Mi Ganancia"), show='headings')
tree.heading("Indice", text="Índice")
tree.heading("Precio", text="Precio")
tree.heading("Dividendo", text="Dividendo")
tree.heading("Pagas", text="Pagas")
tree.heading("Rendimiento", text="Rendimiento")
tree.heading("Mi Ganancia", text="Mi Ganancia")

tree.grid(row=2, column=0, columnspan=12, pady=10, padx=5)

# Inicializa la tabla con los datos del archivo
actualizar_tabla(tree)

# Bind para la tecla Enter en el entry_indice
def on_enter_pressed(event):
    agregar_indice(entry_indice, entry_precio, entry_dividendo, entry_pagas, entry_rendimiento, entry_ganancia, tree)

entry_indice.bind("<Return>", on_enter_pressed)
entry_precio.bind("<Return>", on_enter_pressed)
entry_dividendo.bind("<Return>", on_enter_pressed)
entry_pagas.bind("<Return>", on_enter_pressed)
entry_rendimiento.bind("<Return>", on_enter_pressed)
entry_ganancia.bind("<Return>", on_enter_pressed)

# Inicia la aplicación
root.mainloop()
