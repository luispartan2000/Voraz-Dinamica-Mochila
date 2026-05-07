import customtkinter as ctk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

# Importar las funciones de los algoritmos
from mochila_voraz import mochila_voraz
from mochila_dinamica import mochila_dinamica

ANIMATION_SPEED = 700  # Delay en milisegundos para la animación visual
DP_SPEED = 50  # Delay en milisegundos para la animación de programación dinámica

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.after_ids = []

        # LEFT SIDEBAR (Botones)
        frame_left = ctk.CTkFrame(self, width=200)
        frame_left.grid(row=0, column=0, sticky="ns")  # Usar grid en lugar de pack

        button_greedy = ctk.CTkButton(frame_left, text="Ejecutar Mochila Voraz", command=self.run_greedy)
        button_greedy.grid(pady=10)  # Usar grid en lugar de pack

        button_dynamic = ctk.CTkButton(frame_left, text="Ejecutar Mochila Dinámica", command=self.run_dynamic)
        button_dynamic.grid(pady=10)  # Usar grid en lugar de pack

        button_compare = ctk.CTkButton(frame_left, text="Comparar Resultados", command=self.compare_algorithms)
        button_compare.grid(pady=10)  # Usar grid en lugar de pack

        # CENTER MAIN AREA
        self.tabview = ttk.Notebook(self)  # Crear el tabview aquí mismo
        self.tabview.grid(row=1, column=0, sticky="ew")  # Usar grid en lugar de pack

        tab_greedy = ctk.CTkTabview(self.tabview, width=950)
        tab_dynamic = ctk.CTkTabview(self.tabview, width=950)
        tab_compare = ctk.CTkTabview(self.tabview, width=950)

        # Agregar un Text widget para mostrar resultados
        self.result_text_greedy = ctk.CTkTextbox(tab_greedy, width=950, height=400)
        self.result_text_greedy.pack(side="top", fill="both", expand=True)  # Usar pack en lugar de grid para este caso específico

        self.result_text_dynamic = ctk.CTkTextbox(tab_dynamic, width=950, height=400)
        self.result_text_dynamic.pack(side="top", fill="both", expand=True)  # Usar pack en lugar de grid para este caso específico

        self.result_text_compare = ctk.CTkTextbox(tab_compare, width=950, height=400)
        self.result_text_compare.pack(side="top", fill="both", expand=True)  # Usar pack en lugar de grid para este caso específico

    def run_greedy(self):
        self.cancelar_animaciones()
        self.clear_dashboard(self.result_text_greedy)
        self.tabview.select(0)  # Seleccionar la pestaña "Simulación Algoritmo Voraz"
        capacidad, objetos = self.read_input()
        if not objetos:
            return
        
        start_time_real = time.perf_counter()
        mochila, valor_total = mochila_voraz(capacidad, objetos)
        end_time_real = time.perf_counter()
        real_execution_time = end_time_real - start_time_real
        
        self.display_results(self.result_text_greedy, "Algoritmo Voraz", real_execution_time, valor_total, mochila)

    def run_dynamic(self):
        self.cancelar_animaciones()
        self.clear_dashboard(self.result_text_dynamic)
        self.tabview.select(1)  # Seleccionar la pestaña "Simulación Algoritmo Dinámico"
        capacidad, objetos = self.read_input()
        if not objetos:
            return
        
        start_time_real = time.perf_counter()
        mochila, valor_total = mochila_dinamica(capacidad, objetos)
        end_time_real = time.perf_counter()
        real_execution_time = end_time_real - start_time_real
        
        self.display_results(self.result_text_dynamic, "Programación Dinámica", real_execution_time, valor_total, mochila)

    def compare_algorithms(self):
        self.cancelar_animaciones()
        self.clear_dashboard(self.result_text_compare)
        self.tabview.select(2)  # Seleccionar la pestaña "Comparar Resultados"
        capacidad, objetos = self.read_input()
        if not objetos:
            return
        
        # Ejecutar algoritmo voraz
        start_time_voraz_real = time.perf_counter()
        mochila_voraz_result, valor_total_voraz = mochila_voraz(capacidad, objetos)
        end_time_voraz_real = time.perf_counter()
        execution_time_voraz_real = end_time_voraz_real - start_time_voraz_real
        
        # Ejecutar algoritmo dinámico
        start_time_dynamic_real = time.perf_counter()
        mochila_dynamic_result, valor_total_dynamic = mochila_dinamica(capacidad, objetos)
        end_time_dynamic_real = time.perf_counter()
        execution_time_dynamic_real = end_time_dynamic_real - start_time_dynamic_real
        
        self.display_results(self.result_text_compare, "Algoritmo Voraz", execution_time_voraz_real, valor_total_voraz, mochila_voraz_result)
        self.result_text_compare.insert(ctk.END, "\n")
        self.display_results(self.result_text_compare, "Programación Dinámica", execution_time_dynamic_real, valor_total_dynamic, mochila_dynamic_result)
        
        # Visualización
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(['Voraz', 'Dinámica'], [execution_time_voraz_real, execution_time_dynamic_real], color=['blue', 'green'])
        ax.set_ylabel('Tiempo de ejecución (segundos)')
        ax.set_title('Comparación de Tiempos de Ejecución')
        
        canvas = FigureCanvasTkAgg(fig, master=self.tabview)
        canvas.draw()
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    def on_closing(self):
        self.cancelar_animaciones()
        self.destroy()

    def cancelar_animaciones(self):
        for after_id in self.after_ids:
            self.after_cancel(after_id)
        self.after_ids.clear()

    def clear_dashboard(self, text_widget):
        text_widget.delete(1.0, ctk.END)

    def display_results(self, text_widget, algorithm_name, execution_time, total_value, items):
        text_widget.insert(ctk.END, f"{algorithm_name}\n")
        text_widget.insert(ctk.END, f"Tiempo de ejecución: {execution_time:.6f} segundos\n")
        text_widget.insert(ctk.END, f"Valor total: {total_value}\n")
        text_widget.insert(ctk.END, f"Objetos en la mochila: {items}\n")

    def read_input(self):
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

if __name__ == "__main__":
    app = App()
    app.mainloop()
