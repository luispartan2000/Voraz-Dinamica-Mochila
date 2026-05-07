import time

def mochila_voraz(capacidad, objetos):
    # Ordenamos los objetos por densidad (valor/peso) en orden descendente
    objetos.sort(key=lambda x: x[0] / x[1], reverse=True)
    
    valor_total = 0
    peso_total = 0
    mochila = []

    for valor, peso in objetos:
        if peso_total + peso <= capacidad:
            mochila.append((valor, peso))
            valor_total += valor
            peso_total += peso

    return mochila, valor_total

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
    mochila, valor_total = mochila_voraz(capacidad, objetos)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    print(f"Algoritmo Voraz")
    print(f"Tiempo de ejecución: {execution_time:.6f} segundos")
    print(f"Valor total: {valor_total}")
    print(f"Objetos en la mochila: {mochila}")
