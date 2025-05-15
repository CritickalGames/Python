from TTS.api import TTS

def synthesize(text, output_file="output.wav"):
    """Convierte texto en audio usando Coqui TTS."""
    tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=False)
    output_file = f"output/{output_file}" # Lo guarda en raíz/output/
    tts.tts_to_file(text=text, file_path=output_file)
    print(f"✅ Audio generado: {output_file}")

if __name__ == "__main__":
    synthesize("Hola, este es un ejemplo de síntesis de voz.")
