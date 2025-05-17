import os
import torch
import collections
from TTS.api import TTS
from TTS.utils.radam import RAdam

# Permitir la carga segura de `RAdam`, `collections.defaultdict` y `dict`
torch.serialization.add_safe_globals([RAdam, collections.defaultdict, dict, TTS.tts.configs.xtts_config.XttsConfig])

def synthesize(text, output_file="output.wav"):
    """Convierte texto en audio usando Coqui TTS."""
    
    # Asegurar que la carpeta 'output/' existe antes de guardar el archivo
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  
    
    # Inicializar el modelo de TTS
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
    
    # Definir la ruta de salida dentro de 'output/'
    output_path = os.path.join(output_dir, output_file)
    
    # Generar el audio
    tts.tts_to_file(text=text, file_path=output_path)
    
    print(f"✅ Audio generado: {output_path}")

if __name__ == "__main__":
    synthesize("Hola, este es un ejemplo de síntesis de voz.")
