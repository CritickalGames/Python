# Variable global para almacenar la imagen actual
import os
from tkinter import messagebox
from PIL import Image

class Imagenes:
    def __init__(self, imagen, recorte_der, recorte_inf, nombre_archivo, nombre_entrada, formato):
        self.imagen = imagen
        self.x = recorte_der
        self.y = recorte_inf
        self.nombre_archivo = nombre_archivo
        self.num_entrada = nombre_entrada
        self.formato = formato

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
        imagen = Imagenes(img_recortada, recorte_der, recorte_inf, nombre_archivo, nombre_entrada, formato)
    return imagen

def recortar_imagenes_multi(
        ancho, alto, 
        inicio_x, inicio_y, 
        recorte_der, recorte_inf, 
        imagen_entrada, nombre_entrada, 
        formato, carpeta_salida, nombre_archivo_var, array_recortes_obj, Recorte_obj):
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

            imagen = Imagenes(img_recortada, recorte_der, recorte_inf, nombre_archivo, nombre_entrada, formato)
            
            Recorte_obj.agregar_recorte(imagen, array_recortes_obj)
            
            ruta_salida = os.path.join(carpeta_salida, nombre_salida)

            #!Tengo que hacer que guarde sólo después de aceptar que todas las imagenes están bien
            img_recortada.save(ruta_salida)
            if recorte_der > ancho_img or recorte_inf+alto > alto_img:
                nombre_archivo_var.set(nombre_entrada)
                return array_recortes_obj.array
            nombre_entrada = str(int(nombre_entrada) + 1)

def iniciar_recorte(variables, array_recortes_obj, multi_recorte = False, Recorte_obj= None):
    imagen_entrada = variables["imagen_entrada"].get()
    carpeta_salida = variables["carpeta_salida"].get()
    ancho = int(variables["ancho"].get())
    alto = int(variables["alto"].get())
    formato = variables["formato"].get()

    inicio_x = int(variables["inicio_x"].get())
    inicio_y = int(variables["inicio_y"].get())
    nombre_entrada = variables["nombre_archivo"].get()

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
        # nombre_entrada=(inicio_y//alto)+1 if alto != 0 else 0
        array_recortes_obj.set(
            recortar_imagenes_multi
                (
                ancho, alto, inicio_x, inicio_y, recorte_der, recorte_inf, 
                imagen_entrada, nombre_entrada, formato, carpeta_salida,
                variables["nombre_archivo"], array_recortes_obj, Recorte_obj
                )
            )
    else:
        # Pasa el arreglo de variables a la función recortar_imagenes
        return recortar_imagen(inicio_x, inicio_y, recorte_der, recorte_inf, imagen_entrada, nombre_entrada, formato, carpeta_salida) 