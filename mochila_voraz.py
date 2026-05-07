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
