"""
registry.py – Carga dinámica de motores TTS desde py.toml

Lee la configuración desde [tool.tts] y carga el motor activo
usando rutas dinámicas tipo 'modulo:clase'.
"""
import tomllib
import importlib

def leer_configuracion():
    with open("py.toml", "rb") as f:
        data = tomllib.load(f)
    return data.get("tool", {}).get("tts", {})

def cargar_motor():
    config = leer_configuracion()
    nombre = config.get("motor")
    motores = config.get("motores", {})
    subconfig = config.get("config", {}).get(nombre, {})

    if nombre not in motores:
        raise ValueError(f"❌ Motor '{nombre}' no está definido en [tool.tts.motores]")

    ruta = motores[nombre]
    modulo, clase = ruta.split(":")
    mod = importlib.import_module(modulo)
    cls = getattr(mod, clase)
    return cls(subconfig)
