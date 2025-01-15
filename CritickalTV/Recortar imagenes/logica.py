from logica_carpeta import logica_recortar as Recortar
from logica_carpeta import logica_previsualizacion as Previsualizar
from tkinter import filedialog
import os
from PIL import Image

class Recortes:
    def __init__(self):
        return

    def agregar_recorte(self, img_obj, array_recortes_obj):
        # index = next((i for i, x in enumerate(array_recortes_obj.array) if x is not None and x.num_entrada == img_obj.num_entrada), None)
        if len(array_recortes_obj.array)==0:
            array_recortes_obj.definir(int(img_obj.num_entrada))
            array_recortes_obj.push(index=int(img_obj.num_entrada), item = img_obj)
            return
        elif 0 <= int(img_obj.num_entrada)-1 < len(array_recortes_obj.array) and (array_recortes_obj.array[int(img_obj.num_entrada)-1] is None or array_recortes_obj.array[int(img_obj.num_entrada)-1] is not None):
            array_recortes_obj.array[int(img_obj.num_entrada)-1] = img_obj
            return
        array_recortes_obj.append(img_obj)
        return
    def iniciar_recorte(self, variables, array_recortes_obj, multi_recorte_obj):
        multi_recorte = multi_recorte_obj.get()
        if not multi_recorte:
            img_obj=Recortar.iniciar_recorte(variables, array_recortes_obj, multi_recorte, self)
            self.agregar_recorte(img_obj, array_recortes_obj)
        Recortar.iniciar_recorte(variables, array_recortes_obj, multi_recorte, self)
        
    def seleccionar_imagen_entrada(variables, mostrar_previsualizacion, slider_x, slider_y):
        imagen_entrada_var = variables["imagen_entrada"]
        ancho_var = variables["ancho"]
        alto_var = variables["alto"]

        archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.webp")])
        if archivo:
            imagen_entrada_var.set(archivo)
            with Image.open(imagen_entrada_var.get()) as img:
                # Obtener el ancho de la imagen y actualizar el slider
                ancho_img, alto_img = img.size  # Obtener el ancho y alto de la imagen original
                slider_x.config(to=ancho_img - int(ancho_var.get()))  # Configurar el máximo del slider X
                slider_y.config(to=alto_img - int(alto_var.get()))  # Configurar el máximo del slider Y
            mostrar_previsualizacion(archivo)
            # Le quita el archivo y luego la carpeta del archivo
            ruta_sin_archivo = os.path.dirname(os.path.dirname(archivo))
            variables["carpeta_salida"].set(ruta_sin_archivo)# Asigna nueva carpeta

    def seleccionar_carpeta_salida(carpeta_salida_var):
        carpeta = filedialog.askdirectory()
        if carpeta:
            carpeta_salida_var.set(carpeta)

    def actualizar_valores(variables, signo, slider_y, alto_value = 10, valor_nuevo = -1):
        if valor_nuevo >-1:
            slider_y.set(valor_nuevo)
            return valor_nuevo
        inicio_y_var = (variables["inicio_y"])
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
    
class Previsualizacion:
    def __init__(self):
        return
    def actualizar_previsualizacion(event=None, variables=None, canvas=None):
        Previsualizar.actualizar_previsualizacion(event, variables, canvas)
    
    def mostrar_previsualizacion(archivo, canvas):
        Previsualizar.mostrar_previsualizacion(archivo, canvas)

    def tooltip(array_recortes_obj, variables, slider_y):
        Previsualizar.tooltip(array_recortes_obj, variables, slider_y, Recortes)