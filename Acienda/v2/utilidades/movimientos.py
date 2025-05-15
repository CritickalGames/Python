import json

def crear_movimiento(fecha, concepto, tipo, monto):
    return {
        'fecha': str(fecha),
        'concepto': concepto,
        'tipo': tipo,
        'monto': monto
    }

def guardar_movimiento(movimiento):
    try:
        with open('datos/movimientos.json', 'r+') as archivo:
            datos = json.load(archivo)
            datos.append(movimiento)
            archivo.seek(0)
            json.dump(datos, archivo)
            archivo.truncate()
    except FileNotFoundError:
        with open('datos/movimientos.json', 'w') as archivo:
            json.dump([movimiento], archivo)

def leer_movimientos():
    try:
        with open('datos/movimientos.json', 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []