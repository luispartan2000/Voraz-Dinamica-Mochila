# Explicación del Problema de la Mochila

El problema de la mochila es un clásico en el campo de la optimización combinatoria. Se trata de seleccionar una combinación de objetos para maximizar su valor total, sin exceder una capacidad máxima de peso.

## Algoritmo Voraz

El algoritmo voraz resuelve el problema de la mochila eligiendo siempre el objeto con la mayor densidad (valor/peso) hasta que no se pueda añadir más objetos sin superar la capacidad de la mochila.

### Ventajas
- Simple y fácil de implementar.
- Eficiente para problemas pequeños o cuando los objetos tienen una gran variación en su densidad.

### Desventajas
- No siempre proporciona la solución óptima, especialmente para problemas más grandes o con objetos similares en densidad.

## Programación Dinámica

La programación dinámica resuelve el problema de la mochila utilizando un enfoque bottom-up, construyendo una tabla que almacena los valores máximos posibles para cada capacidad y combinación de objetos.

### Ventajas
- Proporciona la solución óptima para cualquier instancia del problema.
- Es más eficiente que el algoritmo voraz para problemas más grandes o con objetos similares en densidad.

### Desventajas
- Puede ser más complejo de implementar y requerir más recursos computacionales.
