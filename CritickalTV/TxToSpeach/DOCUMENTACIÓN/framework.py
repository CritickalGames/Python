# Da el sistema de archivos y caretas mostrado en "Arquitectura.txt"
# Ningún cambio de "Arquitectura.txt" se verá reflejado en el funcionamiento del .py
# pip freeze > requirements.txt se debe ejecutar manualmente
import os

# Define la estructura del proyecto
estructura = {
    "data": [],
    "models": [],
    "output": [],
    "scripts": ["preprocess.py", "train.py", "synthesize.py"],
    "src": ["main.py", "tts_utils.py"],
    "config": ["settings.json"],
    "logs": [],
    "": ["README.md", "requirements.txt", "configpy.toml", ".gitignore"],  # Archivos en la raíz
}

# Crear carpetas y archivos
for carpeta, archivos in estructura.items():
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo) if carpeta else archivo
        open(ruta_archivo, 'a').close()  # Crea el archivo vacío

print("✅ Estructura del proyecto creada correctamente.")
