from googleapiclient.discovery import build
import re

# Función para obtener la ID de una lista de reproducción
def obtener_id_lista(url):
    match = re.search(r'list=([^&]+)', url)
    if match:
        return match.group(1)
    return None

# Función para obtener las IDs de los videos
def obtener_ids_videos(enlaces):
    video_ids = []
    for enlace in enlaces:
        match = re.search(r'v=([^&]+)', enlace)
        if match:
            video_ids.append(match.group(1))
    return video_ids

# Función para agregar videos a la lista de reproducción
def agregar_videos_a_lista(api_key, playlist_id, video_ids):
    youtube = build('youtube', 'v3', developerKey=api_key)

    for video_id in video_ids:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()
        print(f'Video {video_id} agregado.')

# Función para leer los enlaces desde un archivo y ordenarlos inversamente
def leer_enlaces_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as file:
        enlaces = file.readlines()
    enlaces = [enlace.strip() for enlace in enlaces]  # Eliminar espacios en blanco y saltos de línea
    return enlaces[::-1]  # Invertir el orden de los enlaces

# Ejemplo de uso
nombre_archivo = "./descargar_links_yt_lista/links.txt"
url_lista = "https://www.youtube.com/playlist?list=PLsNSb29cmsj1sLAwe9fNTnPd3iE1sFwQ3" # URL de Crono SMG4
api_key = "YOUR_API_KEY"

enlaces_invertidos = leer_enlaces_desde_archivo(nombre_archivo)
playlist_id = obtener_id_lista(url_lista)
video_ids = obtener_ids_videos(enlaces_invertidos)

agregar_videos_a_lista(api_key, playlist_id, video_ids)
