import tkinter as tk
from tkinter import ttk

class TreeviewSorter:
    def __init__(self, tree):
        self.tree = tree
        self.column = None
        self.reverse = False

        # Configurar el evento de clic en el encabezado
        for col in tree["columns"]:
            tree.heading(col, text=col, command=lambda c=col: self.sort(c))

    def sort(self, column):
        # Verificar si el encabezado de columna ha sido clickeado de nuevo
        if self.column == column:
            self.reverse = not self.reverse
        else:
            self.column = column
            self.reverse = False

        # Obtener los elementos del Treeview
        items = [(self.tree.item(item)["values"], item) for item in self.tree.get_children()]
        items.sort(key=lambda x: x[0][self.tree["columns"].index(column)], reverse=self.reverse)

        # Reordenar los elementos en el Treeview
        for index, (values, item) in enumerate(items):
            self.tree.move(item, '', index)

        # Actualizar los encabezados de columna para reflejar el estado actual
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col + (" ↑" if (col == column and not self.reverse) else " ↓" if (col == column and self.reverse) else ""))

def main():
    root = tk.Tk()
    root.title("Treeview Ordenable")

    # Crear el Treeview
    columns = ("Columna1", "Columna2")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("Columna1", text="Columna 1")
    tree.heading("Columna2", text="Columna 2")

    # Insertar datos
    tree.insert("", "end", values=("Z", "5"))
    tree.insert("", "end", values=("A", "10"))
    tree.insert("", "end", values=("M", "2"))

    # Configurar el sorter
    sorter = TreeviewSorter(tree)

    # Mostrar el Treeview
    tree.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
