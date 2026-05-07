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
    
    capacidad = int(lines[0].strip())
    objetos = []
    for line in lines[1:]:
        valor, peso = map(int, line.strip().split())
        objetos.append((valor, peso))
    
    mochila, valor_total = mochila_voraz(capacidad, objetos)
    print(f"Objetos en la mochila: {mochila}")
    print(f"Valor total: {valor_total}")
