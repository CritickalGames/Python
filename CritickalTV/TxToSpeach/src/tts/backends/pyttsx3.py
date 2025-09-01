import pyttsx3
from src.tts.backends.base import MotorTTS

class MotorPyttsx3(MotorTTS):
    def __init__(self, config):
        self.engine = pyttsx3.init()
        self.voz = config.get("voz")
        if self.voz:
            self._seleccionar_voz(self.voz)

    def _seleccionar_voz(self, nombre):
        for voz in self.engine.getProperty("voices"):
            if nombre.lower() in voz.name.lower():
                self.engine.setProperty("voice", voz.id)
                break

    def leer(self, texto: str):
        self.engine.say(texto)
        self.engine.runAndWait()

    def guardar(self, texto: str, archivo: str):
        return

    def listar_voces(self):
        return [v.name for v in self.engine.getProperty("voices")]