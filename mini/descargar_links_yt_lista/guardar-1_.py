from pytube import Playlist

def leer_enlaces_desde_archivo(nombre_archivo): 
    with open(nombre_archivo, 'r') as file:
        enlaces = file.readlines()
    enlaces = [enlace.strip() for enlace in enlaces] # Eliminar espacios en blanco y saltos de línea 
    return enlaces[::-1] # Invertir el orden de los enlaces 
# Ejemplo de uso 
nombre_archivo = "./descargar_links_yt_lista/links.txt" 
enlaces_invertidos = leer_enlaces_desde_archivo(nombre_archivo) 
print(enlaces_invertidos)

with open('./descargar_links_yt_lista/links-1.txt', 'w', encoding='utf-8') as file:
    for video in enlaces_invertidos:
        file.write(video+ '\n')