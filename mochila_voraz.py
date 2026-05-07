import time

import time

def mochila_voraz(capacidad, objetos, update_callback=None):
    # Ordenamos los objetos por densidad (valor/peso) en orden descendente
    objetos.sort(key=lambda x: x[0] / x[1], reverse=True)
    
    valor_total = 0
    peso_total = 0
    mochila = []

    for i, (valor, peso) in enumerate(objetos):
        if peso_total + peso <= capacidad:
            mochila.append((valor, peso))
            valor_total += valor
            peso_total += peso
            if update_callback:
                update_callback(i, True)
        else:
            if update_callback:
                update_callback(i, False)
        time.sleep(ANIMATION_SPEED / 1000)  # Delay para la animación

    return mochila, valor_total
