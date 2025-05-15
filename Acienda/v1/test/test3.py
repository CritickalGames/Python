import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

# Reemplaza 'tu_api_key' con tu clave API de Alpha Vantage
api_key = '219OZ5PR7RYH775O'

# Ruta al archivo de índices
FILE_NAME = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'txt/indices.txt')
print("Ruta al archivo de índices:\n" + FILE_NAME)

# Función para leer los índices desde un archivo
def _leer_indices():
    indices = {}
    try:
        with open(FILE_NAME, 'r') as file:
            for line in file:
                if line.strip():
                    partes = line.strip().split("||")
                    indices[partes[0]] = partes[1:]
    except FileNotFoundError:
        print("Archivo de índices no encontrado.")
    return indices

# Lee los símbolos de las acciones desde el archivo
indices = _leer_indices()

# Crea un objeto TimeSeries de Alpha Vantage
ts = TimeSeries(key=api_key, output_format='pandas')

# Itera sobre los símbolos leídos y obtiene los datos de Alpha Vantage
for simbolo, datos in indices.items():
    try:
        # Obtiene los datos ajustados mensualmente para cada símbolo
        data, meta_data = ts.get_monthly_adjusted(symbol=simbolo)
        # Muestra los primeros 5 registros del DataFrame, incluyendo los dividendos
        print(f"Datos para {simbolo}:")
        print(data[['5. adjusted close', '7. dividend amount']].head())
    except Exception as e:
        print(f"Error al obtener datos para {simbolo}: {e}")
