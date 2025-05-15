import subprocess
import os

def run_command(command):
    """
    Ejecuta un comando en la línea de comandos y captura la salida.
    """
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error durante la ejecución del comando:")
        print(e.stdout)
        print(e.stderr)
        raise

def preprocess_data(train_src, train_tgt, valid_src, valid_tgt, save_data):
    """
    Preprocesa los datos para OpenNMT.
    """
    preprocess_command = [
        'python', '-m', 'onmt.bin.preprocess',
        '-train_src', train_src,
        '-train_tgt', train_tgt,
        '-valid_src', valid_src,
        '-valid_tgt', valid_tgt,
        '-save_data', save_data
    ]
    
    run_command(preprocess_command)
    print("Preprocessing completed successfully.")

def train_model(data_path, save_model):
    """
    Entrena el modelo de traducción.
    """
    train_command = [
        'python', '-m', 'onmt.bin.train',
        '-data', data_path,
        '-save_model', save_model,
        '-train_steps', '10000',  # Ajusta el número de pasos de entrenamiento según tus necesidades
        '-gpu_ranks', '0'  # Usa la GPU 0 si está disponible
    ]
    
    run_command(train_command)
    print("Training completed successfully.")

if __name__ == "__main__":
    # Define las rutas de los archivos de entrada y salida
    base_path = 'C:/Users/zgtal'  # Cambia esta ruta al directorio correcto
    train_src = os.path.join(base_path, 'src-train.txt')
    train_tgt = os.path.join(base_path, 'tgt-train.txt')
    valid_src = os.path.join(base_path, 'src-val.txt')
    valid_tgt = os.path.join(base_path, 'tgt-val.txt')
    save_data = os.path.join(base_path, 'data/demo')
    save_model = os.path.join(base_path, 'models/demo_model')
    
    # Preprocesa los datos
    preprocess_data(train_src, train_tgt, valid_src, valid_tgt, save_data)
    
    # Entrena el modelo
    train_model(save_data, save_model)
