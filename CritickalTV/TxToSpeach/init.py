import subprocess
import sys
import tomllib
import os
BASE = "src"
STRUCTURE = [
    f"{BASE}/tts/backends",
    f"{BASE}/tts",
]

FILES = {
    f"{BASE}/main.py": "# Punto de entrada\n",
    f"{BASE}/tts/backends/__init__.py": "",
    f"{BASE}/tts/backends/base.py": "# Interfaz común para motores TTS\n",
    f"{BASE}/tts/registry.py": "# Registro dinámico de motores\n",
}
def asegurar_pdm():
    try:
        subprocess.check_call([sys.executable, "-m", "pdm", "--version"], stdout=subprocess.DEVNULL)
        print("✅ PDM disponible como módulo.")
    except subprocess.CalledProcessError:
        print("🔍 PDM no encontrado. Instalando con pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pdm"])
        print("✅ PDM instalado correctamente.")

def leer_dependencias():
    archivo = "py.toml"
    if not os.path.exists(archivo):
        print(f"❌ Archivo {archivo} no encontrado.")
        return []
    with open(archivo, "rb") as f:
        data = tomllib.load(f)
    deps = data.get("tool", {}).get("pdm", {}).get("dependencies", {})
    return [f"{pkg}{ver}" for pkg, ver in deps.items()]

def instalar_dependencias():
    deps = leer_dependencias()
    if not deps:
        print("⚠️ No hay dependencias para instalar.")
        return
    print(f"📦 Instalando dependencias desde py.toml...")
    print(f"🔍 Dependencias encontradas: {deps}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *deps])
    print("✅ Entorno listo.")

def create_structure():
    for folder in STRUCTURE:
        os.makedirs(folder, exist_ok=True)
    for path, content in FILES.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    print("✅ Estructura TTS inicializada.")

crear_arbol = False
if __name__ == "__main__":
    asegurar_pdm()
    instalar_dependencias()
    if crear_arbol:
        create_structure()