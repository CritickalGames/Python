# creacion.py
import tkinter as tk
from logica import (
    seleccionar_imagen_entrada,
    mostrar_previsualizacion, 
    seleccionar_carpeta_salida, 
    iniciar_recorte,
    actualizar_previsualizacion)
import time

# Restricciones
def validar_numeros(P):
    if P == "" or P.isdigit():  # Permitir solo números o vacío
        return True
    else:
        return False

def crear_elementos(ventana):
    # Configurar la validación
    vcmd = (ventana.register(validar_numeros), '%P')

    # Variables
    imagen_entrada_var = tk.StringVar()
    carpeta_salida_var = tk.StringVar()
    ancho_var = tk.StringVar(value="800")  # Valor por defecto
    alto_var = tk.StringVar(value="1422")  # Valor por defecto
    inicio_x_var = tk.StringVar(value="0")  # Coordenada X por defecto
    inicio_y_var = tk.StringVar(value="0")  # Coordenada Y por defecto
    formato_var = tk.StringVar(value="jpg")  # Valor por defecto
    nombre_archivo_var = tk.StringVar(value="0") # Valor por defecto


    # Array de variables
    variables = [
        imagen_entrada_var, # 0
        carpeta_salida_var, # 1
        ancho_var,          # 2
        alto_var,           # 3 
        inicio_x_var,       # 4
        inicio_y_var,       # 5
        nombre_archivo_var, # 6
        formato_var         # 7
        ]

    # Asigar comportamiento a eventos
    def vincular_actualizacion_write(var):
        var.trace_add("write", lambda *args: actualizar_previsualizacion(None, variables, canvas))

    def vincular_actualizacion_ButtonRelease(var):
        var.bind("<ButtonRelease-1>", lambda event: actualizar_previsualizacion(event, variables, canvas))
    
    
    # Widgets
    tk.Label(ventana, text="Seleccionar imagen de entrada:").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(ventana, textvariable=imagen_entrada_var, width=40).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(ventana, text="Buscar", command=lambda: seleccionar_imagen_entrada(variables, lambda archivo: mostrar_previsualizacion(archivo, canvas), slider_x, slider_y)).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(ventana, text="Seleccionar carpeta de salida:").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(ventana, textvariable=carpeta_salida_var, width=40).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(ventana, text="Buscar", command=lambda: seleccionar_carpeta_salida(carpeta_salida_var)).grid(row=1, column=2, padx=10, pady=5)

    tk.Label(ventana, text="Ancho del recorte:").grid(row=2, column=0, padx=10, pady=5)
    tk.Entry(ventana, textvariable=ancho_var).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Alto del recorte:").grid(row=3, column=0, padx=10, pady=5)
    tk.Entry(ventana, textvariable=alto_var).grid(row=3, column=1, padx=10, pady=5)

    # Slider para coordenada X de inicio
    tk.Label(ventana, text="Coordenada X de inicio:").grid(row=4, column=0, padx=10, pady=5)
    tk.Entry(ventana, textvariable=inicio_x_var).grid(row=4, column=1, padx=5, pady=5)

    slider_x = tk.Scale(ventana, from_=0, to=800, orient=tk.HORIZONTAL, command=lambda _: inicio_x_var.set(slider_x.get()))
    slider_x.grid(row=4, column=2, padx=5, pady=5)

    # Slider para coordenada Y de inicio
    tk.Label(ventana, text="Coordenada Y de inicio:").grid(row=5, column=0, padx=10, pady=5)
    tk.Entry(ventana, textvariable=inicio_y_var).grid(row=5, column=1, padx=1, pady=5)

    slider_y = tk.Scale(ventana, from_=0, to=1422, orient=tk.HORIZONTAL, command=lambda _: inicio_y_var.set(slider_y.get()))
    slider_y.grid(row=5, column=2, padx=1, pady=5)

    tk.Label(ventana, text="Formato de salida:").grid(row=6, column=0, padx=10, pady=5)
    tk.Entry(ventana, textvariable=formato_var).grid(row=6, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Nombre del archivo:").grid(row=7, column=0, padx=10, pady=5)
    entry_nombre_archivo = tk.Entry(ventana, validate='key', validatecommand=vcmd, textvariable=nombre_archivo_var)
    entry_nombre_archivo.grid(row=7, column=1, padx=10, pady=5)
    # Botones + y -
    boton_mas = tk.Button(ventana, text="-", command=lambda: nombre_archivo_var.set(((int)(nombre_archivo_var.get())-1 if nombre_archivo_var.get() != "0" else (int)(nombre_archivo_var.get()))))
    boton_mas.grid(row=7, column=2, padx=5, pady=5)  # Eliminar último carácter
    boton_menos=tk.Button(ventana, text="+", command=lambda: nombre_archivo_var.set((int)(nombre_archivo_var.get())+1))
    boton_menos.grid(row=7, column=3, padx=5, pady=5)  # Agregar "nuevo" como ejemplo

    # Canvas para la previsualización
    canvas = tk.Canvas(ventana, width=300, height=300, bg="gray")
    canvas.grid(row=0, column=4, rowspan=8, padx=10, pady=5)

    tk.Button(ventana, text="Iniciar recorte", command=lambda: iniciar_recorte(variables)).grid(row=8, column=1, padx=10, pady=10)

    # Actualizar previsualización automáticamente cuando se cambien los valores de las entradas
    vincular_actualizacion_write(variables[2])  # ancho_var
    vincular_actualizacion_write(variables[3])  # alto_var
    vincular_actualizacion_write(variables[4])  # inicio_x_var
    vincular_actualizacion_write(variables[5])  # inicio_y_var

    # Actualizar al precionar
    vincular_actualizacion_ButtonRelease(slider_x)
    vincular_actualizacion_ButtonRelease(slider_y)
    vincular_actualizacion_ButtonRelease(boton_mas)
    vincular_actualizacion_ButtonRelease(boton_menos)