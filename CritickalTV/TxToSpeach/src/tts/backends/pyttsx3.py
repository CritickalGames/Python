import pyttsx3
from src.tts.backends.base import MotorTTS

class MotorPyttsx3(MotorTTS):
    def __init__(self, config):
        self.engine = pyttsx3.init()
        self.voz = config.get("voz", "")
        self._seleccionar_voz(self.voz)

    def _seleccionar_voz(self, nombre):
        voces = self.engine.getProperty("voices")
        coincidencias = [v for v in voces if nombre.lower() in v.name.lower()]
        if not coincidencias:
            raise ValueError(f"Voz '{nombre}' no encontrada. Voces disponibles: {[v.name for v in voces]}")
        self.engine.setProperty("voice", coincidencias[0].id)


    def leer(self, texto: str):
        self.engine.say(texto)
        self.engine.runAndWait()

    def guardar(self, texto: str, archivo: str):
        print("❌ Guardar no es compatible con pyttsx3")

    def listar_voces(self):
        return [v.name for v in self.engine.getProperty("voices")]