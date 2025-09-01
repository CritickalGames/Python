# Punto de entrada
from .tts.registry import cargar_motor

def demo():
    motor = cargar_motor()

    print("🎙️ Voces disponibles:")
    for voz in motor.listar_voces():
        print(f" - {voz}")

    print("\n🗣️ Leyendo texto de prueba...")
    motor.leer("Hola Zeta, este es un test de síntesis de voz.")

    print("\n💾 Guardando audio en 'salida.mp3'...")
    motor.guardar("Este audio fue generado por el motor activo.", "salida.mp3")

    print("\n✅ Prueba completada.")

if __name__ == "__main__":
    demo()