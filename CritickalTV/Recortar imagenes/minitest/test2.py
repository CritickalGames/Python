import tkinter as tk
from PIL import Image, ImageTk

current_image_id = None
tween_duration = 300  # Duración de la transición en milisegundos

def tween(actual, objetivo, paso):
    """Calcula el siguiente valor en una interpolación lineal."""
    if abs(objetivo - actual) < paso:
        return objetivo
    return actual + paso if actual < objetivo else actual - paso

def actualizar_previsualizacion(event=None, variables=None, canvas=None):
    global current_image_id
    imagen_entrada_var = variables[0]
    imagen_entrada = imagen_entrada_var.get()
    if not imagen_entrada:
        return
    
    ancho_var = variables[1]
    alto_var = variables[2]
    inicio_x_var = variables[3]
    inicio_y_var = variables[4]

    ancho = int(ancho_var.get())
    alto = int(alto_var.get())
    inicio_x = int(inicio_x_var.get())
    inicio_y = int(inicio_y_var.get())
    
    with Image.open(imagen_entrada) as img:
        # Comprobar y ajustar ancho
        if ancho > img.width:
            ancho_var.set(img.width)
            ancho = img.width

        recorte_der = inicio_x + ancho
        recorte_inf = inicio_y + alto

        # Limitar los recortes a los límites de la imagen
        if recorte_der >= img.width:
            recorte_der = img.width
        if recorte_inf > img.height:
            recorte_inf = img.height

        img_recortada = img.crop((inicio_x, inicio_y, recorte_der, recorte_inf))
        img_recortada.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img_recortada)

        if current_image_id:
            canvas.delete(current_image_id)

        current_image_id = canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk  # Mantener la referencia para el GC

def transicion_coordenadas(canvas, variables):
    inicio_x_var = variables[3]
    inicio_y_var = variables[4]
    intervalo = 5  # Tiempo entre pasos de transición en ms
    pasos = tween_duration // intervalo
    objetivo_x = int(inicio_x_var.get())
    objetivo_y = int(inicio_y_var.get())

    # Variables para animar las coordenadas
    current_x = 0
    current_y = 0

    # Calcular los incrementos
    incremento_x = (objetivo_x - current_x) / pasos
    incremento_y = (objetivo_y - current_y) / pasos

    def step():
        nonlocal current_x, current_y
        current_x = tween(current_x, objetivo_x, incremento_x)
        current_y = tween(current_y, objetivo_y, incremento_y)
        
        # Actualizar el recorte de imagen basado en las coordenadas actuales
        inicio_x_var.set(int(current_x))
        inicio_y_var.set(int(current_y))
        actualizar_previsualizacion(variables=variables, canvas=canvas)  # Actualiza la previsualización
        
        # Continuar la animación hasta alcanzar el objetivo
        if (current_x, current_y) != (objetivo_x, objetivo_y):
            canvas.after(intervalo, step)
    
    step()  # Inicia la transición

# Configuración de ejemplo (puedes adaptarla a tu aplicación)
ventana = tk.Tk()
canvas = tk.Canvas(ventana, width=500, height=500)
canvas.pack()
variables = [
    tk.StringVar(value="E:/Vídeos del canal/Bebé gunster/Img/parte4/c11/003.webp"),  # imagen_entrada_var
    tk.IntVar(value=500),                     # width
    tk.IntVar(value=500),                     # height
    tk.IntVar(value=0),                       # inicio_x
    tk.IntVar(value=50)                       # inicio_y
]

# Botón para cargar la imagen
boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=lambda: transicion_coordenadas(canvas, variables))
boton_cargar.pack()

ventana.mainloop()
