# Problema de la Mochila

Este proyecto implementa dos soluciones para el problema de la mochila:
1. Algoritmo voraz
2. Programación dinámica

## Descripción del Proyecto

El proyecto proporciona una interfaz gráfica de usuario (GUI) que permite ejecutar y comparar los resultados de dos algoritmos para resolver el problema de la mochila: el algoritmo voraz y la programación dinámica. La interfaz incluye animaciones paso a paso para visualizar cómo funcionan cada uno de los algoritmos.

## Algoritmos Implementados

1. **Algoritmo Voraz**: Este algoritmo selecciona objetos basándose en su densidad (valor/peso) en orden descendente hasta que no se pueda agregar más objetos sin exceder la capacidad de la mochila.
2. **Programación Dinámica**: Este algoritmo utiliza una tabla para almacenar los resultados intermedios y optimiza la solución mediante un enfoque bottom-up.

## Cómo Ejecutar el Proyecto

1. Asegúrate de tener Python instalado en tu sistema.
2. Descarga o clona este repositorio.
3. Navega al directorio del proyecto.
4. Ejecuta el archivo `interface.py` utilizando el siguiente comando:
   ```
   python interface.py
   ```

## Cómo Empaquetar el Proyecto como Ejecutable

1. Instala PyInstaller si aún no lo has hecho:
   ```
   pip install pyinstaller
   ```
2. Navega al directorio del proyecto.
3. Ejecuta el siguiente comando para empaquetar el proyecto en un ejecutable:
   ```
   python -m PyInstaller --onefile --windowed interface.py
   ```
4. El ejecutable se generará en la carpeta `dist`.

## Notas

- Asegúrate de que el archivo `input.txt` esté correctamente configurado con los datos de entrada.
- La interfaz gráfica proporciona botones para ejecutar cada algoritmo individualmente, comparar ambos y reiniciar la simulación, mostrando los resultados y animaciones paso a paso.

## Robustez

El proyecto valida el archivo `input.txt` de manera segura y maneja errores comunes como entradas malformadas, pesos o valores negativos, etc., para evitar que el programa crashee.
- Se han añadido animaciones para visualizar la evaluación de objetos en el algoritmo voraz y la matriz de programación dinámica.
- Se ha implementado un manejo seguro de cierres de ventana para cancelar callbacks pendientes.
- Se han corregido errores de callbacks inválidos.

## Animaciones

- **Algoritmo Voraz**: La interfaz muestra una lista de objetos, los ordena por relación valor/peso y luego agrega objetos a la mochila uno por uno, indicando si cada objeto entra o no.
- **Programación Dinámica**: Se visualiza una matriz (grid) que se llena paso a paso. Cada celda muestra las decisiones de tomar o no tomar un objeto, y finalmente se realiza una animación de backtracking para mostrar el camino seleccionado.

## Notas

- Asegúrate de que el archivo `input.txt` esté correctamente configurado con los datos de entrada.
- La interfaz gráfica proporciona botones para ejecutar cada algoritmo individualmente, comparar ambos y reiniciar la simulación, mostrando los resultados y animaciones paso a paso.

## Robustez

El proyecto valida el archivo `input.txt` de manera segura y maneja errores comunes como entradas malformadas, pesos o valores negativos, etc., para evitar que el programa crashee.
