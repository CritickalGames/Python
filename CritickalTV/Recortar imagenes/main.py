import tkinter as tk
from creacion import crear_elementos  # Importar la función

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Recortar Imágenes")
ventana.update_preview_id = None

# Crear elementos y obtener variables
crear_elementos(ventana)

ventana.mainloop()
