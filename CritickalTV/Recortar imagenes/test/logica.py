from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Variable global para almacenar la imagen actual
current_image_id = None

def preparar_imagen(imagen_entrada, ancho, alto, inicio_x, inicio_y):
    try:
        with Image.open(imagen_entrada) as img:
            ancho_img, alto_img = img.size
            recorte_der = inicio_x + ancho
            recorte_inf = inicio_y + alto

            if recorte_der > ancho_img or recorte_inf > alto_img:
                messagebox.showerror("Error", "Las dimensiones del recorte exceden el tamaño de la imagen.")
                return
            return recorte_der, recorte_inf
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
        return None

def recortar_imagen(inicio_x, inicio_y, recorte_der, recorte_inf, imagen_entrada, nombre_entrada, formato, carpeta_salida):
    with Image.open(imagen_entrada) as img:
        img_recortada = img.crop((inicio_x, inicio_y, recorte_der, recorte_inf))
        nombre_archivo = os.path.basename(imagen_entrada)
        nombre_salida = f"{nombre_archivo.split('.')[0]}-{nombre_entrada}.{formato}"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)
        img_recortada.save(ruta_salida)

def recortar_imagenes_multi(ancho, alto, inicio_x, inicio_y, recorte_der, recorte_inf, imagen_entrada, nombre_entrada, formato, carpeta_salida, var6):
    with Image.open(imagen_entrada) as img:
        ancho_img, alto_img = img.size
        retorno = 0 # valor generico para que entre por primera vez
        while retorno is not None:
            retorno = preparar_imagen(imagen_entrada, ancho, alto, inicio_x, inicio_y)
            if retorno is None:
                return
            recorte_der, recorte_inf = retorno

            img_recortada = img.crop((inicio_x, inicio_y, recorte_der, recorte_inf))
            inicio_y = recorte_inf
            nombre_archivo = os.path.basename(imagen_entrada)
            nombre_salida = f"{nombre_archivo.split('.')[0]}-{nombre_entrada}.{formato}"
            ruta_salida = os.path.join(carpeta_salida, nombre_salida)

            #!Tengo que hacer que guarde sólo después de aceptar que todas las imagenes están bien
            img_recortada.save(ruta_salida)
            if recorte_der > ancho_img or recorte_inf+alto > alto_img:
                var6.set(nombre_entrada)
                return
            nombre_entrada = str(int(nombre_entrada) + 1)

def iniciar_recorte(variables, multi_recorte = False):
    imagen_entrada = variables[0].get()
    carpeta_salida = variables[1].get()
    ancho = int(variables[2].get())
    alto = int(variables[3].get())
    formato = variables[7].get()

    inicio_x = int(variables[4].get())
    inicio_y = int(variables[5].get())
    nombre_entrada = variables[6].get()

    if not imagen_entrada or not carpeta_salida or not ancho or not alto or not formato:
        messagebox.showwarning("Error", "Por favor completa todos los campos.")
        return
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    resultado = preparar_imagen(imagen_entrada, ancho, alto, inicio_x, inicio_y)

    if resultado is None:
        return
    
    recorte_der, recorte_inf = resultado

    if multi_recorte:
        recortar_imagenes_multi(
            ancho, alto, inicio_x, inicio_y, recorte_der, recorte_inf, 
            imagen_entrada, nombre_entrada, formato, carpeta_salida,
            variables[6])
    else:
        # Pasa el arreglo de variables a la función recortar_imagenes
        recortar_imagen(inicio_x, inicio_y, recorte_der, recorte_inf, imagen_entrada, nombre_entrada, formato, carpeta_salida) 
    
    variables[8].set(os.path.basename(carpeta_salida)+"/"+
                    os.path.splitext(
                        os.path.basename(imagen_entrada))[0]+"-"+variables[6].get()
                        )
    messagebox.showinfo("Finalizado", "Imagen recortada y guardada con éxito.")

    
    
def seleccionar_imagen_entrada(variables, mostrar_previsualizacion, slider_x, slider_y):
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
        mostrar_previsualizacion(archivo)
        # Le quita el archivo y luego la carpeta del archivo
        ruta_sin_archivo = os.path.dirname(os.path.dirname(archivo))
        variables[1].set(ruta_sin_archivo)# Asigna nueva carpeta

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

def actualizar_previsualizacion(event=None, variables=None, canvas=None):
    global current_image_id
    imagen_entrada_var = variables[0]
    ancho_var = variables[2]
    alto_var = variables[3]
    inicio_x_var = variables[4]
    inicio_y_var = variables[5]

    imagen_entrada = imagen_entrada_var.get()
    ancho = int(ancho_var.get())
    alto = int(alto_var.get())
    inicio_x = int(inicio_x_var.get())
    inicio_y = int(inicio_y_var.get())

    if not imagen_entrada:
        messagebox.showwarning("Error", "Por favor selecciona una imagen.")
        return
    
    with Image.open(imagen_entrada) as img:
        # Comprobar y ajustar ancho
        if ancho > img.width:
            ancho_var.set(img.width)
            ancho = img.width  # Actualizar el ancho a la imagen si es mayor

        recorte_der = inicio_x + ancho
        recorte_inf = inicio_y + alto

        # Asegúrate de que los recortes no excedan los límites de la imagen
        if recorte_der >= img.width:
            recorte_der = img.width
        if recorte_inf > img.height:
            recorte_inf = img.height

        img_recortada = img.crop((inicio_x, inicio_y, recorte_der, recorte_inf))  # Recorta la imagen
        img_recortada.thumbnail((300, 300))  # Redimensionar para que encaje en el canvas
        img_tk = ImageTk.PhotoImage(img_recortada)

        if current_image_id:  # Si hay una imagen actual, eliminarla
            canvas.delete(current_image_id)

        # Dibuja la nueva imagen y guarda su ID
        current_image_id = canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        
        # Mantener una referencia a la imagen para evitar que sea recolectada por el GC
        canvas.image = img_tk  

def actualizar_valores(variables, signo, slider_y, alto_value = 10):
    inicio_y_var = (variables[5])
    # Obtener el valor actual de inicio_y_var y alto_var
    current_value = int(inicio_y_var.get())
    max_value = slider_y['to']  # El valor máximo configurado en el slider

    # Actualizar inicio_y_var
    nuevo_valor = current_value + (alto_value * signo)
    if slider_y.get() >= max_value and signo >0:
        return
    inicio_y_var.set(max(0, max(0, nuevo_valor)))  # Limitar entre 0 y Máximo
    slider_y.set(nuevo_valor)
    return nuevo_valor