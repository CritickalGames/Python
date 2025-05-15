import requests
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Variable global para almacenar la ruta de la carpeta
ruta_destino_global = None

def descargar_imagen(url, ruta_destino):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        nombre_archivo = url.split("/")[-1]
        ruta_completa = os.path.join(ruta_destino, nombre_archivo)
        
        with open(ruta_completa, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Imagen guardada como {ruta_completa}")
    except requests.exceptions.RequestException as e:
        mostrar_ventana_emergente(f"Error al descargar la imagen: {e}")
        return True

def seleccionar_carpeta():
    global ruta_destino_global
    ruta_destino = filedialog.askdirectory()
    if ruta_destino:
        ruta_destino_global = ruta_destino
        ruta_label.config(text=f"Carpeta seleccionada: {ruta_destino_global}")
        buscar_button.config(state="normal")

def ejecutar_descarga():
    if ruta_destino_global:
        url_base = url_entry.get()
        numero_inicial_str = (url_base.split('/')[-1])
        numero_inicial_str = (numero_inicial_str.split('.')[0])
        print(f"Numero inicial: {numero_inicial_str}")
        numero_inicial = int(numero_inicial_str)
        formato = len(numero_inicial_str)
        numero_final = int(numero_final_entry.get())
        for numero in range(numero_inicial, numero_final + 1):
            url = url_base.replace(f"/{numero_inicial_str}.", f"/{str(numero).zfill(formato)}.")
            salir= descargar_imagen(url, ruta_destino_global)
            if salir:
                break
        mostrar_ventana_emergente("Fin de la busqueda")
        


def mostrar_ventana_emergente(e):
    messagebox.showinfo("Información", e)


# Configurar la interfaz de Tkinter
root = tk.Tk()
root.title("Descargar imagen .webp")

tk.Label(root, text="URL base de la imagen (terminando en un número):").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

tk.Label(root, text="Número final:").pack()
numero_final_entry = tk.Entry(root, width=10)
numero_final_entry.pack()

ruta_label = tk.Label(root, text="Carpeta no seleccionada")
ruta_label.pack()

carpeta_button = tk.Button(root, text="Seleccionar carpeta", command=seleccionar_carpeta)
carpeta_button.pack()

buscar_button = tk.Button(root, text="Buscar", state="disabled", command=ejecutar_descarga)
buscar_button.pack()

root.mainloop()
