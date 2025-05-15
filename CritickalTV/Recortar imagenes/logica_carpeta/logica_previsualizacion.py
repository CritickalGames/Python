from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import os

current_image_id = None

def mostrar_previsualizacion(archivo, canvas):
    img = Image.open(archivo)
    img.thumbnail((300, 300))  # Redimensionar para que encaje en el canvas
    img_tk = ImageTk.PhotoImage(img)
    
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

def actualizar_previsualizacion(event=None, variables=None, canvas=None):
    global current_image_id
    imagen_entrada_var = variables["imagen_entrada"]
    imagen_entrada = imagen_entrada_var.get()
    if not imagen_entrada:
        messagebox.showwarning("Error", "Por favor selecciona una imagen.")
        return
    
    ancho_var = variables["ancho"]
    alto_var = variables["alto"]
    inicio_x_var = variables["inicio_x"]
    inicio_y_var = variables["inicio_y"]
    
    ancho = int(ancho_var.get())
    alto = int(alto_var.get())
    inicio_x = int(inicio_x_var.get())
    inicio_y = int(inicio_y_var.get())

    
    
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

def tooltip(array_imagenes_obj, variables, slider_y, Recortes):

    array_imagenes = array_imagenes_obj.get()
    """ 
    imagen, inicio_x, inicio_y, recorte_der, recorte_inf, nombre_archivo, nombre_entrada, formato
    """
    def cerrar_ventana():
        global ventana_toplevel
        ventana_toplevel.destroy()
        del ventana_toplevel
    def crear_ventana():
        global ventana_toplevel
        if 'ventana_toplevel' not in globals() or not ventana_toplevel.winfo_exists():
            ventana_toplevel = tk.Toplevel()
            ventana_toplevel.title("Previsualización")
            ventana_toplevel.protocol("WM_DELETE_WINDOW", cerrar_ventana)
        else:
            ventana_toplevel.lift()
        return ventana_toplevel
    
    tooltip_window = crear_ventana()
    def comprobar_canvas():
        for widget in tooltip_window.winfo_children():
            if isinstance(widget, tk.Canvas):  # Verificar si es un Canvas
                # Buscar el Frame dentro del Canvas
                for hijo in widget.winfo_children():
                    if isinstance(hijo, tk.Frame):  # Verificar si es un Frame
                        return True, widget, hijo  # Retornar el Canvas y su Frame hijo
                widget.destroy()
        return False, -1, -1
    def canvas_y_frame():
        _, canvas, content_frame = comprobar_canvas()
        if _:
            return canvas, content_frame
        # Crear el Canvas
        canvas = tk.Canvas(tooltip_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear el Scrollbar al Tooltip
        scrollbar = tk.Scrollbar(tooltip_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el Canvas para que use el Scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un Frame dentro del Canvas para contener los botones
        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor='nw')
        return canvas, content_frame

    def crear_canvas_button(content_frame, width, height, padx=5, pady=5, indice=0, row=0, column=0):
        # Crear un Frame para contener el Canvas y el Label
        container_frame = tk.Frame(content_frame)
        container_frame.grid(row=row, column=column, padx=padx, pady=pady)

        # Crear el Canvas para la imagen
        canvas_button = tk.Canvas(container_frame, width=width, height=height)
        canvas_button.pack()

        # Obtener la imagen y redimensionarla
        imagen_obj = array_imagenes[indice]
        img = imagen_obj.imagen
        img = img.resize((width, height))
        img = ImageTk.PhotoImage(img)

        # Mostrar la imagen en el Canvas
        canvas_button.create_image(0, 0, anchor=tk.NW, image=img)
        canvas_button.image = img  # Mantener una referencia a la imagen

        # Crear un Frame para el Label y el botón "X"
        label_frame = tk.Frame(container_frame)
        label_frame.pack()

        # Crear un Label con el número de entrada
        texto = (imagen_obj.num_entrada)
        label = tk.Label(label_frame, text=texto)
        label.pack(side=tk.RIGHT)  # Colocar el Label a la izquierda

        # Crear un botón "X" al lado del Label
        close_button = tk.Button(label_frame, text="X", bg="red", fg="white", font=("Arial", 8), bd=0)
        close_button.pack(side=tk.LEFT, padx=(0, 5)) 

        # Asignar un evento de clic al botón "X"
        def on_close_click(event):
            event.widget.master.master.destroy()
            eliminar = int(imagen_obj.num_entrada)-1
            array_imagenes_obj.delete(eliminar)
            destruir_y_crear()
            nombre_salida = f"{imagen_obj.nombre_archivo.split('.')[0]}-{imagen_obj.num_entrada}.{imagen_obj.formato}"
            carpeta_salida = variables["carpeta_salida"].get()
            nombre_salida= os.path.join(carpeta_salida, nombre_salida)
            try:
                os.remove(nombre_salida)
            except Exception as e:
                print("no encontrado")

        
        close_button.bind("<Button-1>", on_close_click) 
        # Vincular el evento de clic

        # Asignar un evento de clic al Canvas
        def on_canvas_click(event):
            num = int(imagen_obj.num_entrada)
            desplazamiento = int(imagen_obj.y)-int(variables["alto"].get())
            variables["nombre_archivo"].set(num)
            # desplazamiento = (num-1)*int(variables["alto"].get())
            controlador= 0
            if int(variables["inicio_y"].get()) < desplazamiento:
                controlador = 1
            else:
                controlador = -1
            controlador = 0 if int(variables["inicio_y"].get()) == desplazamiento else controlador

            Recortes.actualizar_valores(variables, controlador, slider_y, valor_nuevo= desplazamiento)
            variables["inicio_y"].set(desplazamiento)
            pass

        canvas_button.bind("<Button-1>", on_canvas_click)  # Vincular el evento de clic

        
        return canvas_button
    
    canvas, content_frame = canvas_y_frame()
    def crear_previsualizacion():
        # Conseguir ancho de ventana
        tooltip_window.update_idletasks()
        ancho = tooltip_window.winfo_width()
        # Valores para el canvas
        width = 50
        height = 100
        padx=5
        pady=5
        # Variables para controlar la posición en el grid
        column = 0
        row = 0
        ## Número máximo de columnas antes de pasar a la siguiente fila
        max_columns = ancho // (width + 2 * padx) 
        for indice, imagen in enumerate(array_imagenes):
            if array_imagenes[indice] is None:
                continue
            crear_canvas_button(content_frame, width, height, padx, pady, indice, row, column)

            # Actualizar la posición en el grid
            column += 1
            if column >= max_columns:  # Si alcanzamos el número máximo de columnas
                column = 0
                row += 1  # Pasar a la siguiente fila

    tooltip_window.update_idletasks()
    ancho_viejo = tooltip_window.winfo_width()
    lista_anchos = {"ancho_viejo":ancho_viejo}
    def on_actualizar_segun_tamanno(event=None):
        tooltip_window.update_idletasks()
        ancho = tooltip_window.winfo_width()
        if ancho == lista_anchos["ancho_viejo"]:
            return
        tooltip_window.update_idletasks()
        lista_anchos["ancho_viejo"] = tooltip_window.winfo_width()
        destruir_y_crear()
    def destruir_y_crear():
        for widget in content_frame.winfo_children():
            widget.destroy()
        crear_previsualizacion()
        
    crear_previsualizacion()
    tooltip_window.bind("<Configure>", on_actualizar_segun_tamanno)    # Actualizar el tamaño del Canvas al contenido
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))