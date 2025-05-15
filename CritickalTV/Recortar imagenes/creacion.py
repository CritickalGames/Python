# creacion.py
import tkinter as tk
from logica import Recortes, Previsualizacion
import threading

class Lista_de_imagenes:
    def __init__(self):
        self.array = []
    def definir(self, longitud):
        self.array = [0]*longitud
    def delete(self, index):
        self.array[index] = None
    def set(self, array):
        self.array = array
    def get(self):
        return self.array
    def append(self,array):
        self.array.append(array)
    def push(self, item, index):
        self.array[index-1]=item

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
    nombre_archivo_var = tk.StringVar(value="1") # Valor por defecto
    nombre_de_ultimo_archivo_var = tk.StringVar(value="Nombre del archivo") # Valor por defecto
    multi_var = tk.BooleanVar(value=True)


    # Array de variables
    variables = {
        "imagen_entrada": imagen_entrada_var,
        "carpeta_salida": carpeta_salida_var,
        "ancho": ancho_var,
        "alto": alto_var,
        "inicio_x": inicio_x_var,
        "inicio_y": inicio_y_var,
        "nombre_archivo": nombre_archivo_var,
        "formato": formato_var,
        "nombre_de_ultimo_archivo": nombre_de_ultimo_archivo_var
    }
    array_recortes = Lista_de_imagenes()

    # Asigar comportamiento a eventos
    def vincular_actualizacion_write(var):
        var.trace_add("write", lambda *args: Previsualizacion.actualizar_previsualizacion(None, variables, canvas))

    def vincular_actualizacion_ButtonRelease(var):
        var.bind("<ButtonRelease-1>", lambda event: Previsualizacion.actualizar_previsualizacion(event, variables, canvas))
    
    # Funciones
    def actualizar_valores_en_hilo(signo, slider, alto=10):
        threading.Thread(target=Recortes.actualizar_valores, args=(variables, signo, slider, alto), daemon=True).start()
    
    # Widgets
    
    def _inner_frame1(ventana_original, canvas):
        def crear_objetos():
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
            tk.Button(inner_frame, text="Buscar",
                command=lambda: 
                    [
                        Recortes.seleccionar_imagen_entrada(variables, 
                                                lambda archivo: Previsualizacion.mostrar_previsualizacion(archivo, canvas),
                                                slider_x, slider_y),
                        inicio_x_var.set("0"),
                        inicio_y_var.set("0"),
                        nombre_archivo_var.set("1"),
                        slider_y.set(0),
                        multi_var.set(True)
                    ]).grid(row=0, column=2, padx=10, pady=5)
            # Seleccionar carpeta de salida
            inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
            _label_y_entry(inner_frame, carpeta_salida_var, nombre="Seleccionar carpeta de salida:",\
                L_row=1, L_col=0,\
                E_row=1, E_col=1,\
                Lx=10,Ly=5,\
                Ex=10,Ey=5,\
                    width=40)
            tk.Button(inner_frame, text="Buscar", command=lambda: Recortes.seleccionar_carpeta_salida(carpeta_salida_var)).grid(row=1, column=2, padx=10, pady=5)

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
            entry_x=_label_y_entry(inner_frame, inicio_x_var, nombre="Coordenada X de inicio:",\
                L_row=4, L_col=0,\
                E_row=4, E_col=1,\
                Lx=10,Ly=5,\
                Ex=10,Ey=5)

            slider_x = tk.Scale(inner_frame, from_=0, to=800, orient=tk.HORIZONTAL, command=lambda _: inicio_x_var.set(slider_x.get()))
            slider_x.grid(row=4, column=2, padx=5, pady=5)

            # Slider para coordenada Y de inicio
            inner_frame = _inner_frame(ventana, frame_args={"bg": "lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
            entry_y = _label_y_entry(inner_frame, inicio_y_var, nombre="Coordenada Y de inicio:",
                            L_row=0, L_col=0,
                            E_row=0, E_col=1,
                            Lx=10, Ly=5,
                            Ex=10, Ey=5)

            slider_y = tk.Scale(inner_frame, bg="lightblue", from_=0, to=1422, orient=tk.HORIZONTAL, command=lambda _: inicio_y_var.set(slider_y.get()))
            slider_y.grid(row=0, column=2, padx=5, pady=5, sticky="w")

            # Botón "+"
            boton_mas = tk.Button(inner_frame, text="+", command=lambda: actualizar_nombre(1))
            boton_mas.grid(row=0, column=4, padx=5, pady=5)

            # Botón "-"
            boton_menos = tk.Button(inner_frame, text="-", command=lambda: actualizar_nombre(-1))
            boton_menos.grid(row=0, column=3, padx=5, pady=5)

            # Formato de salida
            inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
            _label_y_entry(inner_frame, formato_var, nombre="Formato de salida:",\
                L_row=0, L_col=0,\
                E_row=0, E_col=1,\
                Lx=10,Ly=5,\
                Ex=10,Ey=5)

            # Número de recorte
            inner_frame= _inner_frame(ventana, frame_args={"bg":"lightblue"}, padx=pad_inner_frame, pady=5, sticky="w")
            _label_y_entry(inner_frame, nombre_archivo_var, nombre="Número de recorte:",\
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
            return boton_mas, boton_menos, slider_x, slider_y, entry_x, entry_y
        
        boton_mas, boton_menos, slider_x, slider_y, entry_x, entry_y = crear_objetos()

        def vincular_eventos(v_buttonRelease=[], v_write=[]):
            # Actualizar previsualización automáticamente cuando se cambien los valores de las entradas
            for var in v_write:
                vincular_actualizacion_write(var)

            # Actualizar al precionar
            for var in v_buttonRelease:
                vincular_actualizacion_ButtonRelease(var)
                
        vincular_eventos(
            [slider_x, slider_y, boton_mas, boton_menos],
            # ancho_var # alto_var # inicio_x_var # inicio_y_var
            [variables["ancho"], variables["alto"], variables["inicio_x"], variables["inicio_y"]]
        )
        
        # Evento por teclado
        entry_y.bind("<Up>", lambda event: actualizar_valores_en_hilo(+1, slider_y, 10))
        entry_y.bind("<Down>", lambda event: actualizar_valores_en_hilo(-1, slider_y, 10))

        # funciones creadas acá
        def actualizar_nombre(signo):
            nuevo_valor=Recortes.actualizar_valores(variables, signo, slider_y, int(alto_var.get()))
            # Actualizar nombre_archivo_var
            nuevo_numero = int(nombre_archivo_var.get()) + signo
            nombre_archivo_var.set(max(0, nuevo_numero))  # Limitar a valores no negativos
            slider_y.set(nuevo_valor)
        return slider_y


    def _inner_frame2(ventana_original):
        pad_inner_frame=0
        ventana = _inner_frame(ventana_original, None, row= 0,column=1)
        
        inner_frame= _inner_frame(ventana, frame_args={}, padx=pad_inner_frame, pady=5)
        # Canvas para la previsualización
        canvas = tk.Canvas(inner_frame, width=300, height=300, bg="gray")
        canvas.grid(padx=5, pady=5)
        
        inner_frame= _inner_frame(ventana, frame_args={}, padx=pad_inner_frame, pady=5, sticky="w")
        tk.Checkbutton(inner_frame, text="Multi recorte", variable=multi_var).grid(row=0, column=1, padx=20, pady=5)
        recortes_obj = Recortes()
        tk.Button(inner_frame, text="Iniciar recorte", 
                  command=lambda: 
                  [
                      recortes_obj.iniciar_recorte(variables, array_recortes, multi_var), 
                      Previsualizacion.tooltip(array_recortes, variables, slider_y)
                  ]).grid(row=0, column=0, padx=0, pady=1)
        
        inner_frame= _inner_frame(ventana, frame_args={}, padx=pad_inner_frame, pady=5, sticky="w")
        _label_y_entry(inner_frame, nombre_de_ultimo_archivo_var, "Archivo:", 
                       L_row=3, L_col=0, E_row=3, E_col=0)
        
        return canvas

    canvas=_inner_frame2(ventana)
    slider_y=_inner_frame1(ventana, canvas)
    canvas.bind("<MouseWheel>", lambda event: Recortes.actualizar_valores(variables, 1 if event.delta < 0 else -1, slider_y,100))
    canvas.bind("<Up>", lambda event: actualizar_valores_en_hilo(+1, slider_y, 10))
    canvas.bind("<Down>", lambda event: actualizar_valores_en_hilo(-1, slider_y, 10))