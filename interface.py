import customtkinter as ctk
from tkinter import messagebox, ttk
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
    
    result_text.delete(1.0, ctk.END)
    result_text.insert(ctk.END, f"Algoritmo Voraz\n")
    result_text.insert(ctk.END, f"Tiempo de ejecución: {execution_time:.6f} segundos\n")
    result_text.insert(ctk.END, f"Valor total: {valor_total}\n")
    result_text.insert(ctk.END, f"Objetos en la mochila: {mochila}\n")

def run_dynamic():
    capacidad, objetos = read_input()
    if not objetos:
        return
    
    start_time = time.perf_counter()
    mochila, valor_total = mochila_dinamica(capacidad, objetos)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    result_text.delete(1.0, ctk.END)
    result_text.insert(ctk.END, f"Programación Dinámica\n")
    result_text.insert(ctk.END, f"Tiempo de ejecución: {execution_time:.6f} segundos\n")
    result_text.insert(ctk.END, f"Valor total: {valor_total}\n")
    result_text.insert(ctk.END, f"Objetos en la mochila: {mochila}\n")

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
    
    result_text.delete(1.0, ctk.END)
    result_text.insert(ctk.END, f"Algoritmo Voraz\n")
    result_text.insert(ctk.END, f"Tiempo de ejecución: {execution_time_voraz:.6f} segundos\n")
    result_text.insert(ctk.END, f"Valor total: {valor_total_voraz}\n")
    result_text.insert(ctk.END, f"Objetos en la mochila: {mochila_voraz_result}\n")
    
    result_text.insert(ctk.END, "\n")
    
    result_text.insert(ctk.END, f"Programación Dinámica\n")
    result_text.insert(ctk.END, f"Tiempo de ejecución: {execution_time_dynamic:.6f} segundos\n")
    result_text.insert(ctk.END, f"Valor total: {valor_total_dynamic}\n")
    result_text.insert(ctk.END, f"Objetos en la mochila: {mochila_dynamic_result}\n")
    
    # Visualización
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Voraz', 'Dinámica'], [execution_time_voraz, execution_time_dynamic], color=['blue', 'green'])
    ax.set_ylabel('Tiempo de ejecución (segundos)')
    ax.set_title('Comparación de Tiempos de Ejecución')
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

# Crear la ventana principal
root = ctk.CTk()
root.title("Simulador Mochila 0/1")
root.geometry("1500x950")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# LEFT SIDEBAR
sidebar_frame = ctk.CTkFrame(root, width=200)
sidebar_frame.pack(side="left", fill="y")

title_label = ctk.CTkLabel(sidebar_frame, text="Simulador Mochila 0/1", font=("Arial", 24))
title_label.pack(pady=10)

subtitle_label = ctk.CTkLabel(sidebar_frame, text="Elija una opción", font=("Arial", 18))
subtitle_label.pack(pady=5)

button_greedy = ctk.CTkButton(sidebar_frame, text="Ejecutar Voraz", command=run_greedy)
button_greedy.pack(pady=10)

button_dynamic = ctk.CTkButton(sidebar_frame, text="Ejecutar Dinámica", command=run_dynamic)
button_dynamic.pack(pady=10)

button_compare = ctk.CTkButton(sidebar_frame, text="Comparar Ambos", command=compare_algorithms)
button_compare.pack(pady=10)

# CENTER MAIN AREA
tabview = ctk.CTkTabview(root, width=950)
tabview.pack(side="left", fill="both", expand=True)

tab_1 = tabview.add("Simulación Voraz")
tab_2 = tabview.add("Simulación Dinámica")
tab_3 = tabview.add("Dashboard Comparativo")

# RIGHT PANEL
right_panel_frame = ctk.CTkFrame(root, width=350)
right_panel_frame.pack(side="right", fill="y")

time_label = ctk.CTkLabel(right_panel_frame, text="Tiempo actual: 0.0 segundos")
time_label.pack(pady=10)

value_label = ctk.CTkLabel(right_panel_frame, text="Valor total: 0")
value_label.pack(pady=10)

weight_label = ctk.CTkLabel(right_panel_frame, text="Peso acumulado: 0")
weight_label.pack(pady=10)

capacity_label = ctk.CTkLabel(right_panel_frame, text="Capacidad restante: 0")
capacity_label.pack(pady=10)

selected_objects_label = ctk.CTkLabel(right_panel_frame, text="Objetos seleccionados: []")
selected_objects_label.pack(pady=10)

# Agregar un Text widget para mostrar resultados
result_text = ctk.CTkTextbox(tab_3, width=950, height=400)
result_text.pack(side="top", fill="both", expand=True)

# Ejecutar la aplicación
root.mainloop()
