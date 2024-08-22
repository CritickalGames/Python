import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("Ejemplo de Interfaz Gráfica")

# Texto de las instrucciones
instrucciones = "Estas son las instrucciones para el usuario. \n1. Cambiar dirección de página\n2. Dar nombre de página\n0. Salir"

# Crear y empaquetar la etiqueta de instrucciones en la parte superior
instrucciones_label = tk.Label(
    root,
    text=instrucciones,
    font=("Arial", 12),
    fg="black",
    bg="lightgray",
    width=50,
    height=5,
    anchor="w",  # Alinea el texto a la izquierda
    wraplength=300
)
instrucciones_label.pack(side=tk.TOP, fill=tk.X, pady=10)

# Crear un frame para las opciones y botones a la derecha
opciones_frame = tk.Frame(root)
opciones_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

# Crear y empaquetar las opciones y botones en el frame de opciones
direccion_label = tk.Label(opciones_frame, text="Dirección actual:")
direccion_label.pack(anchor="w", pady=5)

direccion_entry = tk.Entry(opciones_frame, width=40)
direccion_entry.pack(anchor="w", pady=5)

cambiar_direccion_button = tk.Button(opciones_frame, text="Cambiar dirección de página")
cambiar_direccion_button.pack(anchor="w", pady=5)

nombre_label = tk.Label(opciones_frame, text="Nombre de la página:")
nombre_label.pack(anchor="w", pady=5)

nombre_entry = tk.Entry(opciones_frame, width=40)
nombre_entry.pack(anchor="w", pady=5)

formato_label = tk.Label(opciones_frame, text="Formato:")
formato_label.pack(anchor="w", pady=5)

formato_entry = tk.Entry(opciones_frame, width=40)
formato_entry.pack(anchor="w", pady=5)

nombre_pagina_button = tk.Button(opciones_frame, text="Dar nombre de página")
nombre_pagina_button.pack(anchor="w", pady=5)

salir_button = tk.Button(opciones_frame, text="Salir", command=root.quit)
salir_button.pack(anchor="w", pady=5)

# Crear y empaquetar un frame para mostrar el texto reconocido (a la izquierda)
texto_frame = tk.Frame(root)
texto_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

texto_label = tk.Label(
    texto_frame,
    text="",  # Este se llenará con el texto reconocido
    font=("Arial", 12),
    fg="black",
    bg="white",
    anchor="w",  # Alinea el texto a la izquierda
    justify="left",  # Justifica el texto a la izquierda
    wraplength=500
)
texto_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

# Iniciar el bucle principal de la ventana
root.mainloop()
