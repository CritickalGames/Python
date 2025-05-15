import sys
import os

# Agregar el directorio raíz al PYTHONPATH
sys.path.append((os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk
from mod_funciones import _colorear

class TreeviewSorter:
    def __init__(self, tree):
        self.tree = tree
        self.column = None
        self.reverse = True

        # Configurar el evento de clic en el encabezado
        for col in tree["columns"]:
            tree.heading(col, text=col, command=lambda c=col: self.sort(c))

    def sort(self, column):
        # Verificar si el encabezado de columna ha sido clickeado de nuevo
        if self.column == column:
            self.reverse = not self.reverse
        else:
            self.column = column
            self.reverse = True

        # Obtener los elementos del Treeview
        items = [(self.tree.item(item)["values"], item) for item in self.tree.get_children()]

        # Ordenar basándose en la columna actual
        def sort_key(item):
            try:
                col_index = self.tree["columns"].index(column)
                if col_index >= len(item[0]):
                    raise IndexError("Columna index out of range")  # Manejo explícito de índice fuera de rango
                value = item[0][col_index]
                try:
                    # Convertir a flotante si es posible
                    return (float(value), value)
                except ValueError:
                    # Mantener como cadena si no se puede convertir a flotante
                    return (float('inf'), value)
            except (IndexError, ValueError) as e:
                print(f"Error: {e}")  # Depuración
                return (float('inf'), '')

        items.sort(key=sort_key, reverse=self.reverse)

        # Reordenar los elementos en el Treeview
        for index, (values, item) in enumerate(items):
            self.tree.move(item, '', index)

        # Actualizar los encabezados de columna para reflejar el estado actual
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col + (" ↑" if (col == column and not self.reverse) else " ↓" if (col == column and self.reverse) else ""))

        # Crear un diccionario para pasar a _colorear
        indices_ordenados = {self.tree.item(item)["values"][0]: self.tree.item(item)["values"][1:] for item in self.tree.get_children()}
        _colorear(indices_ordenados, self.tree)
