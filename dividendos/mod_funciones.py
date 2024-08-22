import os
import tkinter as tk
from tkinter import messagebox, ttk

FILE_NAME = os.path.join(os.path.dirname(__file__), 'indices.txt')

def leer_indices():
    indices = {}
    try:
        with open(FILE_NAME, 'r') as file:
            for line in file:
                if line.strip():
                    partes = line.strip().split("||")
                    indices[partes[0]] = partes[1:]
    except FileNotFoundError:
        pass
    return indices

def guardar_indices(indices):
    with open(FILE_NAME, 'w') as file:
        for indice, valores in indices.items():
            file.write(f"{indice}||{'||'.join(valores)}\n")


def actualizar_tabla(tree):
    indices = leer_indices()
    for row in tree.get_children():
        tree.delete(row)
    for indice, valores in indices.items():
        tree.insert('', 'end', values=(indice, *valores))

def convertir_a_mayusculas(texto):
    return texto.upper() if texto.isalpha() else texto

def limpiar_entries(*entries):
    for entry in entries:
        entry.delete(0, tk.END)

def agregar_indice(entry_indice, entry_precio, entry_dividendo, entry_pagas, entry_rendimiento, entry_ganancia, tree):
    indice = convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return

    indices = leer_indices()

    precio = convertir_a_mayusculas(entry_precio.get().strip())
    dividendo = entry_dividendo.get().strip()
    pagas = convertir_a_mayusculas(entry_pagas.get().strip())
    rendimiento = entry_rendimiento.get().strip()
    ganancia = entry_ganancia.get().strip() if entry_ganancia.get().strip() else "0"

    valores = indices.get(indice, [""]*5)

    # Actualiza los valores solo si se ha introducido un nuevo valor
    valores[0] = precio if precio else valores[0]
    valores[1] = dividendo if dividendo else valores[1]
    valores[2] = pagas if pagas else valores[2]
    valores[3] = rendimiento if rendimiento else valores[3]
    valores[4] = ganancia if ganancia else valores[4]

    indices[indice] = valores

    guardar_indices(indices)
    actualizar_tabla(tree)
    limpiar_entries(entry_indice, entry_precio, entry_dividendo, entry_pagas, entry_rendimiento, entry_ganancia)

def eliminar_indice(entry_indice, tree):
    indice = convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return

    indices = leer_indices()

    if indice in indices:
        del indices[indice]
        guardar_indices(indices)
        actualizar_tabla(tree)
    else:
        messagebox.showerror("Error", f"El índice '{indice}' no existe.")

def sumar_ganancia(entry_indice, entry_precio, entry_dividendo, entry_pagas, entry_rendimiento, entry_ganancia, tree):
    indice = convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return
    indices = leer_indices()
    mi_ganancia = "se va a reemplazar"
    ganancia_actual = "se va a reemplazar"
    try:
        ganancia_actual = float(entry_ganancia.get().strip())
        mi_ganancia = float(indices[indice][4])
    except ValueError:
        print("La cadena no se puede convertir a float.")
        return
    ganancia_actual += mi_ganancia
    # Actualizar el valor en el Entry
    entry_ganancia.delete(0, tk.END)  # Borra el contenido actual
    entry_ganancia.insert(0, str(ganancia_actual))  # Inserta el nuevo valor
    agregar_indice(entry_indice, entry_precio, entry_dividendo, entry_pagas, entry_rendimiento, entry_ganancia, tree)