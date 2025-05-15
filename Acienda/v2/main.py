import sys
from ventanas.principal import VentanaPrincipal
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    sys.exit(app.exec_())

#! Hacer que la pestaña 2 sea un analicis de la información de la pestaña 1
#! Hacer que la tabla de la pestaña muestre las filas según el mes elegido por el calendario