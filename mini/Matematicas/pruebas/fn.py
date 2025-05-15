def imprimir_matriz(matriz, nombre="Matriz"):
    """
    Imprime una matriz en un formato organizado.
    
    :param matriz: Lista de listas que representa la matriz.
    :param nombre: Nombre opcional de la matriz.
    """
    print(f"{nombre}:")
    for fila in matriz:
        print("  [" + " ".join(f"{elemento:>7}" for elemento in fila) + "]")
    print()  # Línea en blanco para separar

def calcular_determinante(matriz):
    if len(matriz) == 1:
        return matriz[0][0]
    elif len(matriz) == 2:
        return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]
    else:
        det = 0
        for i in range(len(matriz)):
            submatriz = [fila[:i] + fila[i+1:] for fila in matriz[1:]]
            det += ((-1)**i)*matriz[0][i]*calcular_determinante(submatriz)
        return det

def transpuesta(matriz):
    """
    Calcula la transpuesta de una matriz 3x3.
    """
    return [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]

def adjunta(matriz):
    """
    Calcula la adjunta de una matriz.
    """
    cofactores = []
    for i in range(len(matriz)):
        fila_cof = []
        for j in range(len(matriz[0])):
            # Crear menor (submatriz excluyendo fila i y columna j)
            menor = [[matriz[x][y] for y in range(len(matriz[0])) if y != j] for x in range(len(matriz)) if x != i]
            # Calcular determinante del menor
            det_menor = calcular_determinante(menor)
            # Aplicar signo alternante
            signo = (-1) ** (i + j)
            fila_cof.append(signo * det_menor)
        cofactores.append(fila_cof)
    return transpuesta(cofactores)

def inversa_con_fracciones(matriz):
    """
    Calcula la inversa de una matriz de cualquier tamaño, mostrando fracciones como caracteres.
    """
    det = calcular_determinante(matriz)
    if det == 0:
        raise ValueError("La matriz no es invertible (determinante = 0).")
    adj = adjunta(matriz)
    # Representar cada elemento de la inversa como fracción de caracteres
    return [[f"{adj[i][j]}/{det}" for j in range(len(matriz))] for i in range(len(matriz))]

def inversa_normal(matriz):
    """
    Calcula la inversa de una matriz de cualquier tamaño, mostrando fracciones como caracteres.
    """
    det = calcular_determinante(matriz)
    if det == 0:
        raise ValueError("La matriz no es invertible (determinante = 0).")
    adj = adjunta(matriz)
    # Representar cada elemento de la inversa como fracción de caracteres
    return [[f"{adj[i][j]/det}" for j in range(len(matriz))] for i in range(len(matriz))]


def suma_matrices(matriz1, matriz2):
    if len(matriz1) != len(matriz2):
        raise ValueError("Las matrices deben tener el mismo tamaño")

    resultado = []
    for i in range(len(matriz1)):
        fila = []
        for j in range(len(matriz1[0])):
            fila.append(matriz1[i][j] + matriz2[i][j])
        resultado.append(fila)

    return resultado

def producto_escalar_matriz(num, matriz):
    producto = []
    for i in range(len(matriz)):
        fila = []
        for j in range(len(matriz[0])):
            fila.append(matriz[i][j]*num)
        producto.append(fila)
    return producto

def producto_matrices(matriz1, matriz2):
    if len(matriz1[0]) != len(matriz2):
        raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz")

    return [[sum(a * b for a, b in zip(fila1, columna2)) for columna2 in zip(*matriz2)] for fila1 in matriz1]

matriz1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matriz2 = [[10, 11, 12], [13, 14, 15], [16, 17, 18]]    
m_A  = [[3,-1],[2,-3]]
m_B  = [[-1,-2],[0,2]]
det     = calcular_determinante(m_A)
inversa_A = inversa_con_fracciones(m_A)
imprimir_matriz(m_A, "A")
imprimir_matriz(inversa_A)
print("Determinante:", det)