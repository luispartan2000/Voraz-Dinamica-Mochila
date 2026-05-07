# Problema de la Mochila

Este proyecto implementa dos soluciones para el problema de la mochila:
1. Algoritmo voraz
2. Programación dinámica

## Descripción del Proyecto

El proyecto proporciona una interfaz gráfica de usuario (GUI) que permite ejecutar y comparar los resultados de dos algoritmos para resolver el problema de la mochila: el algoritmo voraz y la programación dinámica.

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
- La interfaz gráfica proporciona botones para ejecutar cada algoritmo individualmente o comparar ambos, mostrando los resultados y un gráfico de comparación de tiempos de ejecución.

