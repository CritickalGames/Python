import os
import tkinter as tk

def crear_botones(frame, num_botones, botones_por_fila = 5):
    """Crea botones en el frame dado, alineados en filas según el tamaño de la ventana."""
    if botones_por_fila == 0:
        return
    for i in range(num_botones):
        # Calcular la fila y la columna
        fila = i // botones_por_fila  # Dividir el índice por botones_por_fila para obtener la fila
        columna = i % botones_por_fila  # Obtener el índice de la columna
        button = tk.Button(frame, text=f"Botón {i + 1}")
        button.grid(row=fila, column=columna, padx=5, pady=5)  # Coloca el botón en la grilla

def actualizar_botones(frame, num_botones):
    """Actualiza la cantidad de botones en función del tamaño de la ventana."""
    # Obtener el ancho de la ventana
    ancho_ventana = frame.winfo_width()
    
    # Definir el ancho de cada botón (ajusta este valor según el tamaño real de tus botones)
    ancho_boton = 100  # Ancho estimado de cada botón
    espacio = 10  # Espacio entre botones

    # Calcular cuántos botones caben en una fila
    
    # Limpiar el frame antes de agregar botones
    if frame.winfo_children():
        for widget in frame.winfo_children():
            widget.destroy()
    botones_por_fila = (ancho_ventana - espacio) // (ancho_boton + espacio)
    print(botones_por_fila)
    # Crear botones en el frame
    crear_botones(frame, num_botones, botones_por_fila)

def crear_ventana(ventana):
    """Crea la ventana principal con una grilla de botones y una barra de desplazamiento."""

    # Crear un frame para contener el canvas y la scrollbar
    frame_principal = tk.Frame(ventana)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Crear un canvas
    canvas = tk.Canvas(frame_principal)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Crear una barra de desplazamiento
    scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configurar el canvas para que use la scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un frame dentro del canvas
    frame_botones = tk.Frame(canvas)

    # Agregar el frame de botones al canvas
    canvas.create_window((0, 0), window=frame_botones, anchor="nw")

    # Crear botones en el frame
    num_botones = 30  # Cambia el número de botones según sea necesario
    crear_botones(frame_botones, num_botones, 5)  # Inicialmente, 5 botones por fila

ventana = tk.Tk()
ventana.title("Grilla de Botones con Desplazamiento")
ventana.geometry("422x322")
# Actualizar los botones cuando se redimensiona la ventana
os.system('cls' if os.name == 'nt' else 'clear')
def on_resize(event):
    # Aquí puedes agregar lógica para manejar el cambio de tamaño
    print(f"Nuevo tamaño de ventana: {event.width}x{event.height}")

ventana.bind("<Configure>", on_resize)
# Llamar a la función para crear la ventana
crear_ventana(ventana)
ventana.mainloop()
