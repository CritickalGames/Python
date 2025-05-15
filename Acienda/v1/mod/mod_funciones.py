import os
import tkinter as tk
from tkinter import messagebox, ttk

FILE_NAME = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'txt/indices.txt')
print("ruta:\n"+FILE_NAME)

def _leer_indices():
    indices = {}
    try:
        with open(FILE_NAME, 'r') as file:
            for line in file:
                if line.strip():
                    partes = line.strip().split("||")
                    indices[partes[0]] = partes[1:]
    except FileNotFoundError:
        pass
    return indices

def _limpiar_entradas(entries):
    for entry in entries:
        entry.delete(0, tk.END)

def _convertir_a_mayusculas(texto):
    return texto.upper() if texto.isalpha() else texto

def _guardar_indices(indices):
    with open(FILE_NAME, 'w') as file:
        for indice, valores in indices.items():
            file.write(f"{indice}||{'||'.join(valores)}\n")

def _ordenar_indices():
    # Leer los índices del archivo
    indices = _leer_indices()
    
    # Ordenar los índices alfabéticamente
    indices_ordenados = dict(sorted(indices.items(), key=lambda item: item[0]))

    # Guardar los índices ordenados en el archivo
    _guardar_indices(indices_ordenados)

def _colorear(indices, tree):
    blue_o_green = True
    # Configurar la etiqueta para el color de fondo
    for indice in indices.keys():
        tree.tag_configure(indice, background="lightblue") if blue_o_green else tree.tag_configure(indice, background="lightgreen")
        blue_o_green = not blue_o_green

def actualizar_tabla(tree):
    indices = _leer_indices()
    for row in tree.get_children():
        tree.delete(row)
    for indice, valores in indices.items():
        tree.insert('', 'end', values=(indice, *valores), tags=(indice))
    _colorear(indices, tree)

def agregar_indice(entradas, tree):
    entry_indice = entradas[0]
    entry_precio = entradas[1]
    entry_dividendo = entradas[2]
    entry_tipo = entradas[3]
    entry_rendimiento = entradas[4]
    entry_mi_inversion = entradas[5]
    entry_ganancia = entradas[6]

    indice = _convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return

    indices = _leer_indices()

    precio = _convertir_a_mayusculas(entry_precio.get().strip())
    dividendo = entry_dividendo.get().strip()
    tipo = _convertir_a_mayusculas(entry_tipo.get().strip())
    rendimiento = entry_rendimiento.get().strip()
    inversion = entry_mi_inversion.get().strip()
    ganancia = entry_ganancia.get().strip()

    valores = indices.get(indice, [""]*6)

    # Actualiza los valores solo si se ha introducido un nuevo valor
    valores[0] = precio if precio else valores[0]
    valores[1] = dividendo if dividendo else valores[1]
    valores[2] = tipo if tipo else valores[2]
    valores[3] = rendimiento if rendimiento else valores[3]
    valores[4] = inversion if inversion else valores[4]
    valores[5] = ganancia if ganancia else valores[5]

    indices[indice] = valores

    _guardar_indices(indices)
    _ordenar_indices()
    actualizar_tabla(tree)
    _limpiar_entradas(entradas)

def eliminar_indice(entry_indice, tree):
    indice = _convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return

    indices = _leer_indices()

    if indice in indices:
        del indices[indice]
        _guardar_indices(indices)
        actualizar_tabla(tree)
        _limpiar_entradas(entry_indice)
    else:
        messagebox.showerror("Error", f"El índice '{indice}' no existe.")

def sumar_ganancia(entradas, tree):
    entry_indice    = entradas[0]
    entry_ganancia  = entradas[6]
    indice = _convertir_a_mayusculas(entry_indice.get().strip())
    if not indice:
        messagebox.showerror("Error", "El campo de índice no puede estar vacío.")
        return
    indices = _leer_indices()
    mi_ganancia = "se va a reemplazar"
    ganancia_actual = "se va a reemplazar"
    try:
        ganancia_actual = float(entry_ganancia.get().strip())
        mi_ganancia = float(indices[indice][5])
    except ValueError:
        print("La cadena no se puede convertir a float.")
        return
    ganancia_actual += mi_ganancia
    # Actualizar el valor en el Entry
    entry_ganancia.delete(0, tk.END)  # Borra el contenido actual
    entry_ganancia.insert(0, str(ganancia_actual))  # Inserta el nuevo valor
    agregar_indice(entradas, tree)

def siguiente_entry(current_entry, entradas):    
    # Obtener el índice del campo de entrada actual
    try:
        current_index = entradas.index(current_entry)
        # Mover el foco al siguiente campo, si existe
        next_index = (current_index + 1) % len(entradas)  # Cicla al primer campo si se alcanza el último
        entradas[next_index].focus_set()
    except ValueError:
        pass

def calcular_ganancia_potencial(entry_invercion_inicial, tree):
    try:
        invercion_inicial = float(entry_invercion_inicial.get().strip())
    except ValueError:
        messagebox.showerror("Error", "El valor de ganancia potencial debe ser un número válido.")
        return
        
    def _cargar(values,dividendo_anual_total,dividendo_por_pago,tree,item):
        # Actualizar la columna "Potencial Ganancia" y la columna adicional en el Treeview
        values[7] = str(dividendo_anual_total)
        if len(values) > 8:
            values[8] = str(dividendo_por_pago)
        else:
            values.append(str(dividendo_por_pago))
        tree.item(item, values=tuple(values))

    for item in tree.get_children():
        values = list(tree.item(item, "values"))  # Convertir la tupla a lista
        
        # Asegurarse de que 'values' tenga al menos 7 elementos
        while len(values) < 7:
            values.append("0")  # O el valor que prefieras para inicializar

        try:
            indice_precio = float(values[1])  # Precio (suponiendo que está en la segunda columna)
            indice_dividendos = float(values[2])  # Dividendo (suponiendo que está en la tercera columna)
            indice_tipo = values[3]  # Tipo (suponiendo que está en la cuarta columna)
        except ValueError:
            # Si hay un error al convertir los valores, se establece "0" en las columnas correspondientes
            _cargar(values,0,0,tree,item)
            continue  # Saltar filas con valores no numéricos

        # Calcular la cantidad de acciones que se pueden comprar
        if indice_precio == 0:
            _cargar(values,0,0,tree,item)
            continue
        cantidad_acciones = invercion_inicial / indice_precio

        # Determinar el tipo de pago por acción
        try:
            tipo = float(indice_tipo)
        except ValueError:
            tipo = 12  # Si indice_tipo no es convertible a float, asumir 12

        if tipo == 0:
            _cargar(values,0,0,tree,item)
            continue  # Si el tipo es 0, no procesar esta fila

        pagos_por_anno = 12 / tipo
        # Calcular el dividendo anual por acción
        dividendo_anual_por_accion = indice_dividendos * pagos_por_anno

        # Calcular el dividendo anual total
        dividendo_anual_total = cantidad_acciones * dividendo_anual_por_accion
        dividendo_por_pago = cantidad_acciones * indice_dividendos

        _cargar(values,dividendo_anual_total,dividendo_por_pago,tree,item)

    # No es necesario guardar los cambios en el archivo si solo se actualiza la visualización
    # Si necesitas guardar estos cambios en el archivo, debes añadir lógica adicional para hacerlo
