import time

ANIMATION_SPEED = 700

def mochila_voraz(capacidad, objetos):
    # Ordenamos los objetos por densidad (valor/peso) en orden descendente
    objetos.sort(key=lambda x: x[0] / x[1], reverse=True)
    
    valor_total = 0
    peso_total = 0
    mochila = []
    steps = []

    for i, (valor, peso) in enumerate(objetos):
        if peso_total + peso <= capacidad:
            mochila.append((valor, peso))
            valor_total += valor
            peso_total += peso
            steps.append({"obj": i, "fit": True, "current_weight": peso_total})
        else:
            steps.append({"obj": i, "fit": False, "current_weight": peso_total})

    return mochila, valor_total, steps
