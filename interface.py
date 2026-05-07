import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

# Importar las funciones de los algoritmos
from mochila_voraz import mochila_voraz
from mochila_dinamica import mochila_dinamica

def read_input():
    try:
        with open('input.txt', 'r') as file:
            lines = file.readlines()
        
        capacidad = int(lines[0].strip().split('=')[1])
        n = int(lines[1].strip().split('=')[1])
        
        pesos = []
        valores = []
        for line in lines[2:]:
            parts = line.strip().split()
            if parts[0] == 'p':
                pesos.extend(map(int, parts[1:]))
            elif parts[0] == 'b':
                valores.extend(map(int, parts[1:]))
        
        # Validar y manejar los objetos
        objetos = []
        for i in range(min(n, len(pesos))):
            if pesos[i] > 0 and valores[i] >= 0:
                objetos.append((valores[i], pesos[i]))
        
        return capacidad, objetos
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer el archivo input.txt: {e}")
        return None, None

def run_greedy():
    capacidad, objetos = read_input()
    if not objetos:
        return
    
    start_time = time.perf_counter()
    mochila, valor_total = mochila_voraz(capacidad, objetos)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Algoritmo Voraz\n")
    result_text.insert(tk.END, f"Tiempo de ejecución: {execution_time:.6f} segundos\n")
    result_text.insert(tk.END, f"Valor total: {valor_total}\n")
    result_text.insert(tk.END, f"Objetos en la mochila: {mochila}\n")

def run_dynamic():
    capacidad, objetos = read_input()
    if not objetos:
        return
    
    start_time = time.perf_counter()
    mochila, valor_total = mochila_dinamica(capacidad, objetos)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Programación Dinámica\n")
    result_text.insert(tk.END, f"Tiempo de ejecución: {execution_time:.6f} segundos\n")
    result_text.insert(tk.END, f"Valor total: {valor_total}\n")
    result_text.insert(tk.END, f"Objetos en la mochila: {mochila}\n")

def compare_algorithms():
    capacidad, objetos = read_input()
    if not objetos:
        return
    
    # Ejecutar algoritmo voraz
    start_time_voraz = time.perf_counter()
    mochila_voraz_result, valor_total_voraz = mochila_voraz(capacidad, objetos)
    end_time_voraz = time.perf_counter()
    execution_time_voraz = end_time_voraz - start_time_voraz
    
    # Ejecutar algoritmo dinámico
    start_time_dynamic = time.perf_counter()
    mochila_dynamic_result, valor_total_dynamic = mochila_dinamica(capacidad, objetos)
    end_time_dynamic = time.perf_counter()
    execution_time_dynamic = end_time_dynamic - start_time_dynamic
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Algoritmo Voraz\n")
    result_text.insert(tk.END, f"Tiempo de ejecución: {execution_time_voraz:.6f} segundos\n")
    result_text.insert(tk.END, f"Valor total: {valor_total_voraz}\n")
    result_text.insert(tk.END, f"Objetos en la mochila: {mochila_voraz_result}\n")
    
    result_text.insert(tk.END, "\n")
    
    result_text.insert(tk.END, f"Programación Dinámica\n")
    result_text.insert(tk.END, f"Tiempo de ejecución: {execution_time_dynamic:.6f} segundos\n")
    result_text.insert(tk.END, f"Valor total: {valor_total_dynamic}\n")
    result_text.insert(tk.END, f"Objetos en la mochila: {mochila_dynamic_result}\n")
    
    # Visualización
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Voraz', 'Dinámica'], [execution_time_voraz, execution_time_dynamic], color=['blue', 'green'])
    ax.set_ylabel('Tiempo de ejecución (segundos)')
    ax.set_title('Comparación de Tiempos de Ejecución')
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Crear la ventana principal
root = tk.Tk()
root.title("Problema de la Mochila")

# Estilo minimalista
style = ttk.Style(root)
style.theme_use('clam')

# Botones
button_greedy = ttk.Button(root, text="Ejecutar Voraz", command=run_greedy)
button_greedy.pack(pady=5)

button_dynamic = ttk.Button(root, text="Ejecutar Dinámica", command=run_dynamic)
button_dynamic.pack(pady=5)

button_compare = ttk.Button(root, text="Comparar Ambos", command=compare_algorithms)
button_compare.pack(pady=5)

# Texto de resultados
result_text = tk.Text(root, height=10, width=60)
result_text.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
