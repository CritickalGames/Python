# Interfaz común para motores TTS
from abc import ABC, abstractmethod

class MotorTTS(ABC):
    @abstractmethod
    def leer(self, texto: str) -> None:
        """Lee el texto en voz sin guardar."""
        pass

    @abstractmethod
    def guardar(self, texto: str, archivo: str) -> None:
        """Guarda el audio generado en un archivo."""
        pass

    @abstractmethod
    def listar_voces(self) -> list[str]:
        """Devuelve una lista de voces disponibles."""
        pass