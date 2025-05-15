from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QCalendarWidget, QTabWidget
from utilidades.movimientos import crear_movimiento, guardar_movimiento, leer_movimientos
from utilidades.fecha import obtener_fecha_actual

def ordenar(datos):
    return sorted(datos, key=lambda x: x['fecha'])

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.datos_originales = []  # Almacena los datos originales
        self.orden_actual = -1
        self.columnas = ['fecha', 'concepto', 'tipo', "monto"]
        self.datos_originales = leer_movimientos()
        self.rango_columnas = 3
        self.initUI()
        
            

    def invertir_valor(self, columna):
        if self.orden_actual != columna:
            self.orden_actual = columna
        else:
            self.orden_actual = -1

    def initUI(self):
        self.setGeometry(100, 50, 400, 650)  # posición(x,y), tamaño(x,y)
        self.setWindowTitle('Movimientos')

        def crear_etiqueta_fecha(layout):
            etiqueta_fecha = QLabel('Fecha:')
            layout.addWidget(etiqueta_fecha)
            return etiqueta_fecha

        def crear_campo_fecha( layout):
            self.campo_fecha = QCalendarWidget(self)
            self.campo_fecha.setGridVisible(True)
            self.campo_fecha.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
            self.campo_fecha.setSelectedDate(obtener_fecha_actual())
            layout.addWidget(self.campo_fecha)

        def crear_etiqueta_concepto(layout):
            etiqueta_concepto = QLabel('Concepto:')
            layout.addWidget(etiqueta_concepto)
            return etiqueta_concepto

        def crear_campo_concepto( layout):
            self.campo_concepto = QLineEdit()
            layout.addWidget(self.campo_concepto)

        def crear_etiqueta_tipo(layout):
            etiqueta_tipo = QLabel('Tipo:')
            layout.addWidget(etiqueta_tipo)
            return etiqueta_tipo

        def crear_campo_tipo( layout):
            self.campo_tipo = QComboBox()
            self.campo_tipo.addItem('Ingreso')
            self.campo_tipo.addItem('Egreso')
            layout.addWidget(self.campo_tipo)

        def crear_etiqueta_monto(layout):
            etiqueta_monto = QLabel('Monto:')
            layout.addWidget(etiqueta_monto)
            return etiqueta_monto

        def crear_campo_monto( layout):
            self.campo_monto = QLineEdit()
            layout.addWidget(self.campo_monto)

        def crear_boton_crear_movimiento( layout):
            boton_crear_movimiento = QPushButton('Crear movimiento')
            boton_crear_movimiento.clicked.connect(self.crear_movimiento)
            layout.addWidget(boton_crear_movimiento)

        def crear_tabla_movimientos( layout):
            self.tabla_movimientos = QTableWidget()
            self.tabla_movimientos.setRowCount(0)
            self.tabla_movimientos.setColumnCount(3)
            self.tabla_movimientos.setHorizontalHeaderLabels(['Fecha', 'Concepto', 'Monto'])
            layout.addWidget(self.tabla_movimientos)

        def configurar_tabla_movimientos(self):
            header = self.tabla_movimientos.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            header.sectionClicked.connect(self.ordenar_tabla)

        

        def crear_layout_pestañas():
            def crear_pestañas():
                self.tab_widget = QTabWidget()
                self.tab_widget.addTab(QWidget(), 'Movimientos')
                self.tab_widget.addTab(QWidget(), 'Otra pestaña')        
            crear_pestañas()
            layout = QVBoxLayout()
            layout.addWidget(self.tab_widget)
            self.setLayout(layout)

        crear_layout_pestañas()

        def crear_layout_movimientos(id):
            layout = QVBoxLayout()
            self.tab_widget.widget(id).setLayout(layout)

            crear_etiqueta_fecha(layout)
            crear_campo_fecha(layout)
            crear_etiqueta_concepto(layout)
            crear_campo_concepto(layout)
            crear_etiqueta_tipo(layout)
            crear_campo_tipo(layout)
            crear_etiqueta_monto(layout)
            crear_campo_monto(layout)
            crear_boton_crear_movimiento(layout)
            crear_tabla_movimientos(layout)
            configurar_tabla_movimientos(self)

            layout.addWidget(self.tabla_movimientos)

            self.cargar_datos_en_tabla(self.datos_originales)
        crear_layout_movimientos(0)
        self.show()

    def cargar_datos_en_tabla(self, datos):
        self.tabla_movimientos.setRowCount(len(datos))
        for i, movimiento in enumerate(datos):
            self.tabla_movimientos.setItem(i, 0, QTableWidgetItem(movimiento['fecha']))
            self.tabla_movimientos.setItem(i, 1, QTableWidgetItem(movimiento['concepto']))
            self.tabla_movimientos.setItem(i, 2, QTableWidgetItem(str(movimiento['monto'])))
            if movimiento['tipo'] == 'Egreso':
                for j in range(self.rango_columnas):
                    item = self.tabla_movimientos.item(i, j)
                    item.setBackground(QtGui.QColor(200, 50, 70))  # Rojo
                    #item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # Blanco
    def crear_movimiento(self):
        fecha = self.campo_fecha.selectedDate().toString("dd/MM/yyyy")
        concepto = self.campo_concepto.text()
        tipo = self.campo_tipo.currentText()
        monto = float(self.campo_monto.text())

        movimiento = crear_movimiento(fecha, concepto, tipo, monto)
        guardar_movimiento(movimiento)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.datos_originales = leer_movimientos()
        self.cargar_datos_en_tabla(self.datos_originales)
        self.ordenar_tabla(-1)

    def ordenar_tabla(self, columna):
        datos = self.datos_originales.copy()  # Copiar los datos originales
        if columna > -1:
            self.invertir_valor(columna)
        if self.orden_actual == -1:
            datos.sort(key=lambda x: x[self.columnas[columna]])
        else:
            datos.sort(key=lambda x: x[self.columnas[columna]], reverse=True)

        self.cargar_datos_en_tabla(datos)