# creacion.py
import tkinter as tk
from logica import (
    seleccionar_imagen_entrada,
    mostrar_previsualizacion, 
    seleccionar_carpeta_salida, 
    iniciar_recorte,
    actualizar_previsualizacion)
import time

def _inner_frame(frame, frame_args=None, **grid_kwargs):
    # Configuración predeterminada para frame_kwargs y grid_kwargs
    frame_kwargs = frame_args or {}
    # Crear un frame interno para organizar el Label y Entry juntos
    inner_frame = tk.Frame(frame, **frame_kwargs)
    inner_frame.grid(**grid_kwargs)  # Espacio alrededor del conjunto Label + Entry
    return inner_frame

def _label_y_entry(frame, textvariable= None, nombre="", L_row=0, L_col=0, E_row=0, E_col=0, Lx=5,Ly=5, Ex=5,Ey=5, **entry_kwargs):
    tk.Label(frame, text=nombre).grid(row=L_row, column=L_col, padx=Lx, pady=Ly)
    entry = tk.Entry(frame, textvariable=textvariable, **entry_kwargs)
    entry.grid(row=E_row, column=E_col, padx=Ex, pady=Ey)
    return entry

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
    
    def _inner_frame1(ventana_original, canvas):
        pad_inner_frame=50
        ventana = _inner_frame(ventana_original, None, row= 0, column=0, pady=10)
        # Seleccionar imagen de entrada
        inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
        _label_y_entry(inner_frame, imagen_entrada_var, nombre="Seleccionar imagen de entrada:",\
            L_row=0, L_col=0,\
            E_row=0, E_col=1,\
            Lx=10,Ly=5,\
            Ex=10,Ey=5,\
                width=40)
        tk.Button(inner_frame, text="Buscar", command=lambda: seleccionar_imagen_entrada(variables, lambda archivo: mostrar_previsualizacion(archivo, canvas), slider_x, slider_y)).grid(row=0, column=2, padx=10, pady=5)

        # Seleccionar carpeta de salida
        inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
        _label_y_entry(inner_frame, carpeta_salida_var, nombre="Seleccionar carpeta de salida:",\
            L_row=1, L_col=0,\
            E_row=1, E_col=1,\
            Lx=10,Ly=5,\
            Ex=10,Ey=5,\
                width=40)
        tk.Button(inner_frame, text="Buscar", command=lambda: seleccionar_carpeta_salida(carpeta_salida_var)).grid(row=1, column=2, padx=10, pady=5)

        # Ancho del recorte
        inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
        _label_y_entry(inner_frame, ancho_var, nombre="Ancho del recorte:",\
            L_row=2, L_col=0,\
            E_row=2, E_col=1,\
            Lx=10,Ly=5,\
            Ex=10,Ey=5)

        # Alto del recorte
        inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
        _label_y_entry(inner_frame, alto_var, nombre="Alto del recorte:",\
            L_row=3, L_col=0,\
            E_row=3, E_col=1,\
            Lx=10,Ly=5,\
            Ex=10,Ey=5)

        # Slider para coordenada X de inicio
        inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
        _label_y_entry(inner_frame, inicio_x_var, nombre="Coordenada X de inicio:",\
            L_row=4, L_col=0,\
            E_row=4, E_col=1,\
            Lx=10,Ly=5,\
            Ex=10,Ey=5)

        slider_x = tk.Scale(inner_frame, from_=0, to=800, orient=tk.HORIZONTAL, command=lambda _: inicio_x_var.set(slider_x.get()))
        slider_x.grid(row=4, column=2, padx=5, pady=5)

        # Slider para coordenada Y de inicio
        inner_frame = _inner_frame(ventana, frame_args={"bg": "lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
        _label_y_entry(inner_frame, inicio_y_var, nombre="Coordenada Y de inicio:",
                        L_row=0, L_col=0,
                        E_row=0, E_col=1,
                        Lx=10, Ly=5,
                        Ex=10, Ey=5)

        slider_y = tk.Scale(inner_frame, bg="lightblue", from_=0, to=1422, orient=tk.HORIZONTAL, command=lambda _: inicio_y_var.set(slider_y.get()))
        slider_y.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Botón "+"
        boton_mas = tk.Button(inner_frame, text="+", command=lambda: actualizar_valores(1))
        boton_mas.grid(row=0, column=3, padx=5, pady=5)

        # Botón "-"
        boton_menos = tk.Button(inner_frame, text="-", command=lambda: actualizar_valores(-1))
        boton_menos.grid(row=0, column=4, padx=5, pady=5)

        def actualizar_valores(signo):
            # Obtener el valor actual de inicio_y_var y alto_var
            current_value = int(inicio_y_var.get())
            alto_value = int(alto_var.get())
            max_value = slider_y['to']  # El valor máximo configurado en el slider

            # Actualizar inicio_y_var
            nuevo_valor = current_value + (alto_value * signo)
            if slider_y.get() >= max_value:
                return
            inicio_y_var.set(max(0, max(0, nuevo_valor)))  # Limitar entre 0 y Máximo

            # Actualizar nombre_archivo_var
            nuevo_numero = int(nombre_archivo_var.get()) + signo
            nombre_archivo_var.set(max(0, nuevo_numero))  # Limitar a valores no negativos
            slider_y.set(nuevo_valor)

        # Formato de salida
        inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
        _label_y_entry(inner_frame, formato_var, nombre="Formato de salida:",\
            L_row=0, L_col=0,\
            E_row=0, E_col=1,\
            Lx=10,Ly=5,\
            Ex=10,Ey=5)

        # Número de recorte
        inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
        entry_nombre_archivo=_label_y_entry(inner_frame, nombre_archivo_var, nombre="Número de recorte:",\
            L_row=0, L_col=0,\
            E_row=0, E_col=1,\
            Lx=10,Ly=5,\
            Ex=10,Ey=5,\
                validate='key', validatecommand=vcmd)
        
            # Botones + y -
        boton_mas = tk.Button(inner_frame, text="-", command=lambda: nombre_archivo_var.set(((int)(nombre_archivo_var.get())-1 if nombre_archivo_var.get() != "0" else (int)(nombre_archivo_var.get()))))
        boton_mas.grid(row=0, column=2, padx=5, pady=5)  # Eliminar último carácter
        boton_menos=tk.Button(inner_frame, text="+", command=lambda: nombre_archivo_var.set((int)(nombre_archivo_var.get())+1))
        boton_menos.grid(row=0, column=3, padx=5, pady=5)  # Agregar "nuevo" como ejemplo

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
    
    def _inner_frame2(ventana_original):
        ventana = _inner_frame(ventana_original, None, row= 0,column=1)
        # Canvas para la previsualización
        canvas = tk.Canvas(ventana, width=300, height=300, bg="gray")
        canvas.grid(padx=5, pady=5)

        tk.Button(ventana, text="Iniciar recorte", command=lambda: iniciar_recorte(variables)).grid(row=8, column=0, padx=5, pady=10)
        
        entry_nombre=_label_y_entry(ventana, None, "Archivo:", L_row=9, L_col=0, E_row=9, E_col=0)
        entry_nombre.insert(0, "Nombre del archivo")

        

        return canvas

    canvas=_inner_frame2(ventana)
    _inner_frame1(ventana, canvas)
    