from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Variable global para almacenar la imagen actual
current_image_id = None

def recortar_imagenes(variables):
    imagen_entrada = variables[0].get()
    carpeta_salida = variables[1].get()
    ancho = int(variables[2].get())
    alto = int(variables[3].get())
    inicio_x = int(variables[4].get())
    inicio_y = int(variables[5].get())
    nombre_entrada = variables[6].get()
    formato = variables[7].get()

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    with Image.open(imagen_entrada) as img:
        ancho_img, alto_img = img.size
        x, y = ancho, alto
        
        if inicio_x + x > ancho_img or inicio_y + y > alto_img:
            messagebox.showerror("Error", "Las dimensiones del recorte exceden el tamaño de la imagen.")
            return

        recorte_der = inicio_x + x
        recorte_inf = inicio_y + y
        img_recortada = img.crop((inicio_x, inicio_y, recorte_der, recorte_inf))

        nombre_archivo = os.path.basename(imagen_entrada)
        nombre_salida = f"{nombre_archivo.split('.')[0]}-{nombre_entrada}.{formato}"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)
        img_recortada.save(ruta_salida)

        messagebox.showinfo("Finalizado", "Imagen recortada y guardada con éxito.")

def seleccionar_imagen_entrada(ventana, variables, canvas, slider_x, slider_y):
    imagen_entrada_var = variables[0]
    ancho_var = variables[2]
    alto_var = variables[3]

    archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.webp")])
    if archivo:
        imagen_entrada_var.set(archivo)
        with Image.open(imagen_entrada_var.get()) as img:
            # Obtener el ancho de la imagen y actualizar el slider
            ancho_img, alto_img = img.size  # Obtener el ancho y alto de la imagen original
            slider_x.config(to=ancho_img - 1)  # Configurar el máximo del slider X
            slider_y.config(to=alto_img - int(alto_var.get()))  # Configurar el máximo del slider Y
        actualizar_previsualizacion(None, variables, canvas)

def mostrar_previsualizacion(archivo, canvas):
    img = Image.open(archivo)
    img.thumbnail((300, 300))  # Redimensionar para que encaje en el canvas
    img_tk = ImageTk.PhotoImage(img)
    
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

def seleccionar_carpeta_salida(carpeta_salida_var):
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_salida_var.set(carpeta)

def actualizar_previsualizacion(event=None, variables=None, canvas=None, tween_duration = 500):
    global current_image_id
    imagen_entrada_var = variables[0]
    imagen_entrada = imagen_entrada_var.get()
    if not imagen_entrada:
        return
    ancho_var = variables[2]
    alto_var = variables[3]
    inicio_x = int(variables[4].get())
    inicio_y = int(variables[5].get())
    
    ancho = int(ancho_var.get())
    alto = int(alto_var.get())
    
    with Image.open(imagen_entrada) as img:
        # Comprobar y ajustar ancho
        if ancho > img.width:
            ancho_var.set(img.width)
            ancho = img.width
        if alto > img.height:
            alto_var.set(img.height)
            alto = img.height

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

        def transicion_suave(canvas, inicio_x_objetivo, inicio_y_objetivo):
            intervalo = 10  # Tiempo entre pasos de transición en ms
            pasos = tween_duration // intervalo
            variables = {
                "x": canvas.coords(current_image_id)[0] if current_image_id else 0,
                "y": canvas.coords(current_image_id)[1] if current_image_id else 0
            }
            incremento_x = (inicio_x_objetivo - variables['x']) / pasos
            incremento_y = (inicio_y_objetivo - variables['y']) / pasos

            def step():
                variables['x'] = tween(variables['x'], inicio_x_objetivo, incremento_x)
                variables['y'] = tween(variables['y'], inicio_y_objetivo, incremento_y)
                
                canvas.coords(current_image_id, variables['x'], variables['y'])
                
                if (variables['x'], variables['y']) != (inicio_x_objetivo, inicio_y_objetivo):
                    canvas.after(intervalo, step)
            
            step()  # Inicia la transición

        def tween(actual, objetivo, paso):
            """Calcula el siguiente valor en una interpolación lineal."""
            if abs(objetivo - actual) < paso:
                return objetivo
            return actual + paso if actual < objetivo else actual - paso

def iniciar_recorte(variables):
    imagen_entrada = variables[0].get()
    carpeta_salida = variables[1].get()
    ancho = int(variables[2].get())
    alto = int(variables[3].get())
    inicio_x = int(variables[4].get())
    inicio_y = int(variables[5].get())
    formato = variables[7].get()

    if not imagen_entrada or not carpeta_salida or not ancho or not alto or not formato:
        messagebox.showwarning("Error", "Por favor completa todos los campos.")
        return

    recorte = (ancho, alto)
    coordenadas_inicio = (inicio_x, inicio_y)
    recortar_imagenes(variables)  # Pasa el arreglo de variables a la función recortar_imagenes

