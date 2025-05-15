from datetime import date
from typing import Literal

class Movimiento:
    def __init__(self, fecha: date, concepto: str, tipo: Literal['ingreso', 'egreso'], monto: float):
        self.fecha = fecha
        self.concepto = concepto
        self.tipo = tipo
        self.monto = monto

    def __str__(self):
        return f"{self.fecha} - {self.concepto} - {self.tipo} - {self.monto}"