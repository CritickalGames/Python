exec(open("setup.py", encoding="utf-8").read())
import os

print(f"PYTHONPATH actual: {os.environ.get('PYTHONPATH')}")

from scripts.synthesize import synthesize

if __name__ == "__main__":
    text = "Hola Mundo, este es un ejemplo de síntesis de voz."
    synthesize(text, "hola_mundo.wav")
