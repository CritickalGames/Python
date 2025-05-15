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

def determinante(matriz):
    """
    Calcula el determinante de una matriz 3x3.
    """
    return (matriz[0][0] * (matriz[1][1] * matriz[2][2] - matriz[1][2] * matriz[2][1]) -
            matriz[0][1] * (matriz[1][0] * matriz[2][2] - matriz[1][2] * matriz[2][0]) +
            matriz[0][2] * (matriz[1][0] * matriz[2][1] - matriz[1][1] * matriz[2][0]))

def transpuesta(matriz):
    """
    Calcula la transpuesta de una matriz 3x3.
    """
    return [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]

def adjunta(matriz):
    """
    Calcula la adjunta de una matriz 3x3.
    """
    cofactores = []
    for i in range(3):
        fila_cof = []
        for j in range(3):
            # Crear menor (submatriz excluyendo fila i y columna j)
            menor = [[matriz[x][y] for y in range(3) if y != j] for x in range(3) if x != i]
            # Calcular determinante del menor
            det_menor = (menor[0][0] * menor[1][1] - menor[0][1] * menor[1][0])
            # Aplicar signo alternante
            signo = (-1) ** (i + j)
            fila_cof.append(signo * det_menor)
        cofactores.append(fila_cof)
    return transpuesta(cofactores)

def inversa_con_fracciones(matriz):
    """
    Calcula la inversa de una matriz 3x3, mostrando fracciones como caracteres.
    """
    det = determinante(matriz)
    if det == 0:
        raise ValueError("La matriz no es invertible (determinante = 0).")
    adj = adjunta(matriz)
    # Representar cada elemento de la inversa como fracción de caracteres
    return [[f"{adj[i][j]}/{det}" for j in range(3)] for i in range(3)]

# Ejemplo de uso con la matriz A
A = [
    [1, 1, 1],
    [1, 2, -1],
    [2, 1, 0]
]

# Resultados
imprimir_matriz(A, "Matriz A")
imprimir_matriz(transpuesta(A), "Transpuesta de A")
imprimir_matriz(adjunta(A), "Adjunta de A")
imprimir_matriz(inversa_con_fracciones(A), "Inversa de A (con fracciones)")
