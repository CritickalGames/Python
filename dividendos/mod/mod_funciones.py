import os
import tkinter as tk
from tkinter import messagebox, ttk

FILE_NAME = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'txt/indices.txt')
print("ruta:\n"+FILE_NAME)

def _leer_indices():
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

def _limpiar_entradas(*entries):
    for entry in entries:
        entry.delete(0, tk.END)

def _convertir_a_mayusculas(texto):
    return texto.upper() if texto.isalpha() else texto

def _guardar_indices(indices):
    with open(FILE_NAME, 'w') as file:
        for indice, valores in indices.items():
            file.write(f"{indice}||{'||'.join(valores)}\n")

def _ordenar_indices():
    # Leer los índices del archivo
    indices = _leer_indices()
    
    # Ordenar los índices alfabéticamente
    indices_ordenados = dict(sorted(indices.items(), key=lambda item: item[0]))

    # Guardar los índices ordenados en el archivo
    _guardar_indices(indices_ordenados)

def _colorear(indices, tree):
    blue_o_green = True
    # Configurar la etiqueta para el color de fondo
    for indice in indices.keys():
        tree.tag_configure(indice, background="lightblue") if blue_o_green else tree.tag_configure(indice, background="lightgreen")
        blue_o_green = not blue_o_green

def actualizar_tabla(tree):
    indices = _leer_indices()
    for row in tree.get_children():
        tree.delete(row)
    for indice, valores in indices.items():
        tree.insert('', 'end', values=(indice, *valores), tags=(indice))
    _colorear(indices, tree)

def agregar_indice(entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia, tree):
    indice = _convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return

    indices = _leer_indices()

    precio = _convertir_a_mayusculas(entry_precio.get().strip())
    dividendo = entry_dividendo.get().strip()
    tipo = _convertir_a_mayusculas(entry_tipo.get().strip())
    rendimiento = entry_rendimiento.get().strip()
    ganancia = entry_ganancia.get().strip() if entry_ganancia.get().strip() else "0"

    valores = indices.get(indice, [""]*5)

    # Actualiza los valores solo si se ha introducido un nuevo valor
    valores[0] = precio if precio else valores[0]
    valores[1] = dividendo if dividendo else valores[1]
    valores[2] = tipo if tipo else valores[2]
    valores[3] = rendimiento if rendimiento else valores[3]
    valores[4] = ganancia if ganancia else valores[4]

    indices[indice] = valores

    _guardar_indices(indices)
    _ordenar_indices()
    actualizar_tabla(tree)
    _limpiar_entradas(entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia)

def eliminar_indice(entry_indice, tree):
    indice = _convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return

    indices = _leer_indices()

    if indice in indices:
        del indices[indice]
        _guardar_indices(indices)
        actualizar_tabla(tree)
        _limpiar_entradas(entry_indice)
    else:
        messagebox.showerror("Error", f"El índice '{indice}' no existe.")

def sumar_ganancia(entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia, tree):
    indice = _convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return
    indices = _leer_indices()
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
    agregar_indice(entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia, tree)

def siguiente_entry(current_entry, entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia):
    # Lista de los campos de entrada en el orden en que deben recibir el foco
    entries = [entry_indice, entry_precio, entry_dividendo, entry_tipo, entry_rendimiento, entry_ganancia]
    
    # Obtener el índice del campo de entrada actual
    try:
        current_index = entries.index(current_entry)
        # Mover el foco al siguiente campo, si existe
        next_index = (current_index + 1) % len(entries)  # Cicla al primer campo si se alcanza el último
        entries[next_index].focus_set()
    except ValueError:
        pass