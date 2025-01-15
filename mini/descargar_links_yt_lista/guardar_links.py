from pytube import Playlist

# URL de la lista de reproducción
playlist_url = 'https://www.youtube.com/playlist?list=PLsNSb29cmsj1F5_Km5McWaq0rQWl48v5a'

# Crear objeto de la lista de reproducción
playlist = Playlist(playlist_url)

# Guardar los enlaces de los videos en un archivo txt
with open('./descargar_links_yt_lista/links.txt', 'w', encoding='utf-8') as file:
    for video in playlist.videos:
        file.write(video.watch_url + '\n')

print("Los enlaces se han guardado en links.txt")