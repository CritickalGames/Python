from alpha_vantage.timeseries import TimeSeries

# Reemplaza 'tu_api_key' con tu clave API de Alpha Vantage
api_key = 'tu_api_key'

# Crea un objeto TimeSeries
ts = TimeSeries(key=api_key, output_format='pandas')

# Obtén datos históricos de una acción (por ejemplo, 'AAPL' para Apple Inc.)
data, meta_data = ts.get_daily(symbol='AAPL', outputsize='full')

# Muestra los primeros 5 registros de los datos
print(data.head())
