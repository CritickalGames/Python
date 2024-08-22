# Importaciones
import tkinter as tk
from tkinter import filedialog, messagebox
import pytesseract
from PIL import Image
import os

# TODO: Optimizar el formateo de imagenes separando los procesos por pasos
## While busca todas las imagenes y guarda una lista de tamaño N
## El tamaño N se divide entre la cantidad de hilos
## Si el modulo no es 0, el último hilo trabaja una imagen más

# TODO: Agregar un una ventana de traducción de textos de japonés a español

# Función para configurar Tesseract
def configurar_tesseract():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# Variables globales
image_path = ''
direccion_actual = os.getcwd()

pantalla_ancho = 1100
pantalla_alto = 650

# Configuraciones de ejemplo
configs = [r'--oem 3 --psm 5 -l jpn_vert']

# Función para procesar imagen con configuración personalizada
def arrancar_texto_de_imagen(custom_config):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, config=custom_config)
        text = text.replace(" ", "").replace("\n", "||")
        text = f"{'Archivo:':>10} {os.path.basename(image_path)}\n{text}\n\n"
        texto_label.insert(tk.END, text)
        return True
    except FileNotFoundError as fnf_error:
        error_texto.insert(tk.END, f"Error: Archivo no encontrado - {fnf_error}\n")
    except Exception as e:
        error_texto.insert(tk.END, f"Error al procesar la imagen: {e}\n")
    return False

# Función para cambiar la dirección
def cambiar_direccion():
    global direccion_actual
    nueva_direccion = filedialog.askdirectory()
    if os.path.isdir(nueva_direccion):
        direccion_actual = nueva_direccion
        direccion_entry.delete(0, tk.END)
        direccion_entry.insert(0, direccion_actual)
    else:
        messagebox.showerror("Error", f"La carpeta {nueva_direccion} no existe.")

def encontrar_imagenes_y_texto(nombre_pagina, formato):
    global image_path
    indice = 1
    while True:
        nombre_archivo = f"{nombre_pagina}_{indice}.{formato}"
        image_path = os.path.join(direccion_actual, nombre_archivo)
        if arrancar_texto_de_imagen(configs[0]):
            indice += 1
        else:
            break

# Función para dar nombre a la página
def dar_nombre_pagina():
    nombre_pagina = nombre_entry.get().strip()
    formato = formato_entry.get().strip() or 'png'
    encontrar_imagenes_y_texto(nombre_pagina, formato)

# Función para salir
def salir():
    root.destroy()

# Función para crear instrucciones
def crear_instrucciones(root):
    instrucciones = """
    Instrucciones:
    1. Cada texto debe tener un fondo 100% blanco.
    2. El furigana se debe limpiar.
    3. El texto que no esté vertical debe ir a parte.
    4. Los globos con varias oraciones se deben separar.
    5. A veces el programa de reconocimiento se vuelve loco, por lo que úsalo como un soporte para acelerar el trabajo.
    """
    instrucciones_label = tk.Label(
        root,
        text=instrucciones,
        font=("Arial", 12),
        fg="black",
        bg="lightgray",
        width=70,
        height=7,
        anchor="w",
        justify="left",
        wraplength=root.winfo_screenwidth() - 100
    )
    instrucciones_label.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
# Función para crear la caja de errores
def crear_bloque_de_errores(opciones_frame):
    global error_texto
    error_texto_label = tk.Label(opciones_frame, text="Errores:")
    error_texto_label.pack(anchor="w", pady=5)
    error_texto = tk.Text(
        opciones_frame,
        font=("Arial", 10),
        fg="red",
        bg="white",
        wrap=tk.WORD,
        width=40,
        height=10,
        padx=10,
        pady=5,
        relief=tk.SOLID,
        bd=1,
    )
    
    error_scrollbar_y = tk.Scrollbar(opciones_frame, orient=tk.VERTICAL, command=error_texto.yview)
    error_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    error_texto.config(yscrollcommand=error_scrollbar_y.set)
    error_texto.pack(anchor="w", pady=5)

# Función para crear opciones
def crear_opciones(root):
    global direccion_entry, nombre_entry, formato_entry

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

    canvas = tk.Canvas(canvas_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar_y.set)
    canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    opciones_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=opciones_frame, anchor="nw")

    # Opciones y botones
    widgets = [
        ("Dirección actual:", direccion_actual, "Cambiar dirección de página", cambiar_direccion),
        ("Nombre de la página:", "", "", None),
        ("Formato (.png por defecto):", "", "", None),
    ]

    for label_text, default_value, button_text, button_command in widgets:
        label = tk.Label(opciones_frame, text=label_text)
        label.pack(anchor="w", pady=5)
        entry = tk.Entry(opciones_frame, width=40)
        entry.insert(0, default_value)
        entry.pack(anchor="w", pady=5)
        if button_text:
            button = tk.Button(opciones_frame, text=button_text, command=button_command)
            button.pack(anchor="w", pady=5)
        if label_text == "Dirección actual:":
            direccion_entry = entry
        elif label_text == "Nombre de la página:":
            nombre_entry = entry
        elif label_text == "Formato (.png por defecto):":
            formato_entry = entry

    nombre_pagina_button = tk.Button(opciones_frame, text="Dar nombre de página", command=dar_nombre_pagina)
    nombre_pagina_button.pack(anchor="w", pady=5)
    salir_button = tk.Button(opciones_frame, text="Salir", command=salir)
    salir_button.pack(anchor="w", pady=5)

    # Bloque de texto para errores
    crear_bloque_de_errores(opciones_frame)

# Función para crear el texto reconocido
def crear_texto(root):
    global texto_label
    texto_frame = tk.Frame(root)
    texto_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
    texto_label = tk.Text(
        texto_frame,
        font=("Arial", 12),
        fg="black",
        bg="white",
        wrap=tk.NONE,
        width=60,
        height=20,
        padx=10,
        pady=5,
        relief=tk.SOLID,
        bd=1,
        spacing1=1,
        spacing2=1,
        spacing3=1,
    )    
    scrollbar_x = tk.Scrollbar(texto_frame, orient=tk.HORIZONTAL, command=texto_label.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    texto_label.config(xscrollcommand=scrollbar_x.set)
    
    scrollbar_y = tk.Scrollbar(texto_frame, orient=tk.VERTICAL, command=texto_label.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    texto_label.config(yscrollcommand=scrollbar_y.set)

    texto_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    

def main():
    global root
    root = tk.Tk()
    root.title("OSC - Reconocimiento de Texto")
    root.geometry(f"{pantalla_ancho}x{pantalla_alto}")
    configurar_tesseract()
    crear_instrucciones(root)
    crear_opciones(root)
    crear_texto(root)
    root.mainloop()

if __name__ == "__main__":
    main()
