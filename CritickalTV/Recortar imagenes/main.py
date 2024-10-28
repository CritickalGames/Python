import tkinter as tk
from creacion import crear_elementos  # Importar la función

# TODO: Hacer funcional el previsualizador de nombre y hacer que use ese entry para ingresar el nombre
# TODO: hacer que el previsualizador de nombre funcione con un texto de ejemplo que explique su función
# TODO: Mejorar la fluidez del slider
# TODO: Hacer que se pueda hacer recorrtes con el ratón
# TODO: Hacer que se mueda mover la previsualización con el ratón
# ? TODO: Hacer que se puedan hacer varios cortes a la vez en el previsualizador
# ? TODO: Cambiar el diseño del programa para que parezca más photshop 

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Recortar Imágenes")
ventana.update_preview_id = None

# Crear elementos y obtener variables
crear_elementos(ventana)

ventana.mainloop()
