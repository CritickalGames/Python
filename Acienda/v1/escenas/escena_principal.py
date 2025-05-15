import sys
import os

# Agregar el directorio raíz al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk
from mod.mod_funciones import *  # Alternativamente, puedes volver a llamar las funciones de manera individual
from mod.Treeview_ordenar import TreeviewSorter

def _label_y_entry(frame, nombre="", L_row=0, L_col=0, E_row=0, E_col=0, Lx=5,Ly=5, Ex=5,Ey=5):
    tk.Label(frame, text=nombre).grid(row=L_row, column=L_col, padx=Lx, pady=Ly)
    entry = tk.Entry(frame)
    entry.grid(row=E_row, column=E_col, padx=Ex, pady=Ey)
    return entry
def _tree(frame):
    tree = ttk.Treeview(frame, columns=("Indice", "Precio", "Dividendo", "Pagas", "Rendimiento", "Mi inversión", "Mi Ganancia", "Potencial Ganancia", "Ganancia Por Pago"), show='headings', selectmode="browse")
    tree.heading("Indice", text="Índice")
    tree.heading("Precio", text="Precio")
    tree.heading("Dividendo", text="Dividendo")
    tree.heading("Pagas", text="Pagas")
    tree.heading("Rendimiento", text="Rendimiento")
    tree.heading("Mi inversión", text="Mi inversión")
    tree.heading("Mi Ganancia", text="Mi Ganancia")
    tree.heading("Potencial Ganancia", text="Potencial Ganancia")
    tree.heading("Ganancia Por Pago", text="Ganancia Por Pago")

    # Establecer el mismo ancho para todas las columnas
    column_width = 150
    for col in tree["columns"]:
        tree.column(col, width=column_width)

    tree.grid(row=2, column=0, columnspan=26, pady=10, padx=5)
    return tree
def _botones(frame, tree, entradas, entry_inversion_inicial):

    tk.Button(frame, text="Agregar Índice", 
        command=lambda: 
        agregar_indice(entradas, tree)).grid(row=1, column=3, columnspan=1, pady=5, padx=5)
    tk.Button(frame, text="Calcular Ganancia", 
        command=lambda: 
        calcular_ganancia_potencial(entry_inversion_inicial, tree)).grid(row=1, column=4, columnspan=6, pady=5, padx=5)
    tk.Button(frame, text="Eliminar Índice", 
        command=lambda: 
        eliminar_indice(entradas[0], tree)).grid(row=1, column=6, columnspan=6, pady=5, padx=5)
    tk.Button(frame, text="Sumar Ganancia", 
        command=lambda: 
        sumar_ganancia(entradas, tree)).grid(row=1, column=11, pady=5, padx=5)

def _asignar_eventos(tree, entradas):
    entry_indice = entradas[0]
    entry_precio = entradas[1]
    entry_dividendo = entradas[2]
    entry_tipo = entradas[3]
    entry_rendimiento = entradas[4]
    entry_ganancia = entradas[6]
    def on_siguiente_entry(event):
        siguiente_entry(event.widget, entradas)
    def on_agregar_indice(event):
        agregar_indice(entradas, tree)
    def on_sumar_ganancia(event):
        sumar_ganancia(entradas, tree)

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

    # Configurar el comportamiento de expansión
    root.columnconfigure(0, weight=1)  # Permitir que la columna 0 del root se expanda
    root.rowconfigure(0, weight=1)     # Permitir que la fila 0 del root se expanda
    frame.columnconfigure(0, weight=1)  # Permitir que la columna 0 del frame se expanda
    frame.rowconfigure(2, weight=1)     # Permitir que la fila 2 (donde está el Treeview) del frame se expanda

    # Input para el índice
    entry_indice = _label_y_entry(frame, "Índice:", 0, 0, 0, 1)
    # Inputs para los datos del índice en una fila
    entry_precio = _label_y_entry(frame,"Precio:", 0, 2, 0, 3)
    entry_dividendo = _label_y_entry(frame,"Dividendo:", 0, 4, 0, 5)
    entry_tipo = _label_y_entry(frame,"Tipo:", 0, 6, 0, 7)
    entry_rendimiento = _label_y_entry(frame,"Rendimiento:", 0, 8, 0, 9)
    entry_mi_inversion = _label_y_entry(frame,"Mi inversión:", 1, 1, 1, 2)
    entry_ganancia = _label_y_entry(frame,"Mi Ganancia:", 0, 10, 0, 11)

    entry_inversion_inicial = _label_y_entry(frame,"Inversión de:", 1, 4, 1, 5)

    entradas = [
        entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_mi_inversion, entry_ganancia
    ]

    # Crear la tabla
    tree = _tree(frame)

    # Botones para agregar y eliminar
    _botones(frame, tree, entradas, entry_inversion_inicial)

    # Bind para la tecla Enter en el entry_indice
    _asignar_eventos(tree, entradas)

    # Configurar el sorter
    sorter = TreeviewSorter(tree)

    # Inicializa la tabla con los datos del archivo
    actualizar_tabla(tree)

    # Inicia la aplicación
    root.mainloop()
