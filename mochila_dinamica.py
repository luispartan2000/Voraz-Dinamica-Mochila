import time

def mochila_dinamica(capacidad, objetos):
    n = len(objetos)
    dp = [[0 for _ in range(capacidad + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        valor, peso = objetos[i - 1]
        for w in range(1, capacidad + 1):
            if peso <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - peso] + valor)
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruir la mochila
    mochila = []
    w = capacidad
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            valor, peso = objetos[i - 1]
            mochila.append((valor, peso))
            w -= peso

    return mochila, dp[n][capacidad]

if __name__ == "__main__":
    # Leer la entrada desde input.txt
    with open('input.txt', 'r') as file:
        lines = file.readlines()
    
    capacidad = int(lines[0].strip().split('=')[1])
    n = int(lines[1].strip().split('=')[1])
    
    objetos = []
    for line in lines[2:]:
        parts = line.strip().split()
        if parts[0] == 'p':
            pesos = list(map(int, parts[1:]))
        elif parts[0] == 'b':
            valores = list(map(int, parts[1:]))
    
    # Validar y manejar los objetos
    for i in range(min(n, len(pesos))):
        if pesos[i] >= 0 and valores[i] >= 0:
            objetos.append((valores[i], pesos[i]))
    
    start_time = time.time()
    mochila, valor_total = mochila_dinamica(capacidad, objetos)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    print(f"Programación Dinámica")
    print(f"Tiempo de ejecución: {execution_time:.6f} segundos")
    print(f"Valor total: {valor_total}")
    print(f"Objetos en la mochila: {mochila}")
