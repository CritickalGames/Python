import sys
import os

# Agregar el directorio raíz al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk
from mod.mod_funciones import *  # Alternativamente, puedes volver a llamar las funciones de manera individual
from mod.Treeview_ordenar import TreeviewSorter

def _indice(frame):
    tk.Label(frame, text="Índice:").grid(row=0, column=0, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=0, column=1, padx=5, pady=5)
    return entry
def _precio(frame):
    tk.Label(frame, text="Precio:").grid(row=0, column=2, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=0, column=3, padx=5, pady=5)
    return entry
def _dividendos(frame):
    tk.Label(frame, text="Dividendo:").grid(row=0, column=4, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=0, column=5, padx=5, pady=5)
    return entry
def _tipo(frame):
    tk.Label(frame, text="Tipo:").grid(row=0, column=6, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=0, column=7, padx=5, pady=5)
    return entry
def _rendimiento(frame):
    tk.Label(frame, text="Rendimiento:").grid(row=0, column=8, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=0, column=9, padx=5, pady=5)
    return entry
def _ganancia(frame):
    tk.Label(frame, text="Mi Ganancia:").grid(row=0, column=10, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=0, column=11, padx=5, pady=5)
    return entry

def _tree(frame):
    tree = ttk.Treeview(frame, columns=("Indice", "Precio", "Dividendo", "Pagas", "Rendimiento", "Mi Ganancia"), show='headings', selectmode="browse")
    tree.heading("Indice", text="Índice")
    tree.heading("Precio", text="Precio")
    tree.heading("Dividendo", text="Dividendo")
    tree.heading("Pagas", text="Pagas")
    tree.heading("Rendimiento", text="Rendimiento")
    tree.heading("Mi Ganancia", text="Mi Ganancia")

    tree.grid(row=2, column=0, columnspan=12, pady=10, padx=5)
    return tree

def _botones(frame, tree, *entradas):
    entry_indice = entradas[0]
    entry_precio = entradas[1]
    entry_dividendo = entradas[2]
    entry_tipo = entradas[3]
    entry_rendimiento = entradas[4]
    entry_ganancia = entradas[5]
    tk.Button(frame, text="Agregar Índice", command=lambda: agregar_indice(entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia, tree)).grid(row=1, column=0, columnspan=6, pady=5, padx=5)
    tk.Button(frame, text="Eliminar Índice", command=lambda: eliminar_indice(entry_indice, tree)).grid(row=1, column=6, columnspan=6, pady=5, padx=5)
    tk.Button(frame, text="Sumar Ganancia", command=lambda: sumar_ganancia(entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia, tree)).grid(row=1, column=11, pady=5, padx=5)
   

def _asignar_eventos(tree, *entradas):
    entry_indice = entradas[0]
    entry_precio = entradas[1]
    entry_dividendo = entradas[2]
    entry_tipo = entradas[3]
    entry_rendimiento = entradas[4]
    entry_ganancia = entradas[5]
    def on_siguiente_entry(event):
        siguiente_entry(event.widget, entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia)
    def on_agregar_indice(event):
        agregar_indice(entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia, tree)
    def on_sumar_ganancia(event):
        sumar_ganancia(entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia, tree)

    entry_indice.bind("<Return>", on_siguiente_entry)
    entry_precio.bind("<Return>", on_siguiente_entry)
    entry_dividendo.bind("<Return>", on_siguiente_entry)
    entry_tipo.bind("<Return>", on_siguiente_entry)
    entry_rendimiento.bind("<Return>", on_agregar_indice)
    entry_ganancia.bind("<Return>", on_sumar_ganancia)


def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Gestor de Índices")

    # Crear un contenedor con un margen de 5 píxeles
    frame = tk.Frame(root, padx=5, pady=5)
    frame.grid(sticky="nsew")

    # Input para el índice
    entry_indice = _indice(frame)
    # Inputs para los datos del índice en una fila
    entry_precio = _precio(frame)
    entry_dividendo = _dividendos(frame)
    entry_tipo = _tipo(frame)
    entry_rendimiento = _rendimiento(frame)
    entry_ganancia = _ganancia(frame)

    # Crear la tabla
    tree = _tree(frame)

    # Botones para agregar y eliminar
    _botones(frame, tree, entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia)

    # Bind para la tecla Enter en el entry_indice
    _asignar_eventos(tree, entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia)

    # Configurar el sorter
    sorter = TreeviewSorter(tree)
    
    # Inicializa la tabla con los datos del archivo
    actualizar_tabla(tree)
    # Inicia la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()