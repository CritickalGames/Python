from alpha_vantage.timeseries import TimeSeries
import pandas as pd

# Reemplaza 'tu_api_key' con tu clave API de Alpha Vantage
api_key = '219OZ5PR7RYH775O'

# Crea un objeto TimeSeries
ts = TimeSeries(key=api_key, output_format='pandas')

# Obtén los datos de la serie de tiempo ajustada mensualmente para una acción (por ejemplo, 'AAPL')
data, meta_data = ts.get_monthly_adjusted(symbol='AAPL')

# Muestra los primeros 5 registros del DataFrame, incluyendo los dividendos
print(data[['5. adjusted close', '7. dividend amount']].head())
