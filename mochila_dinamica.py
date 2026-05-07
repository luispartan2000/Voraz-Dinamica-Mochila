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
