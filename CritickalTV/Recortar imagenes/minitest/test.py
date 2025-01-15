import tkinter as tk
import os
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado

class ToolTip:
    def __init__(self, widget, image_path):
        self.widget = widget
        self.image_path = image_path
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window is not None:
            return
        x = self.widget.winfo_rootx() + 100
        y = self.widget.winfo_rooty() + -20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Cargar la imagen
        current_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_directory, self.image_path)
        print(current_directory)
        print(self.image_path)
        with Image.open(image_path) as image:
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(self.tooltip_window, image=photo)
            label.image = photo  # Mantener una referencia a la imagen
            label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# Ejemplo de uso
root = tk.Tk()
button = tk.Button(root, text="Pasa el cursor aquí")
button.pack(pady=20)

# Asegúrate de que la ruta de la imagen sea correcta
tooltip = ToolTip(button, "1-1.jpg")

root.mainloop()