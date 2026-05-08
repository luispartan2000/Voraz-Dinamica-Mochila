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
        self.animation_ids = []

        # LEFT SIDEBAR (Botones)
        self.sidebar_frame = ctk.CTkFrame(self, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")  # Usar grid en lugar de pack

        button_greedy = ctk.CTkButton(self.sidebar_frame, text="Ejecutar Mochila Voraz", command=self.run_greedy)
        button_greedy.grid(pady=10)  # Usar grid en lugar de pack

        button_dynamic = ctk.CTkButton(self.sidebar_frame, text="Ejecutar Mochila Dinámica", command=self.run_dynamic)
        button_dynamic.grid(pady=10)  # Usar grid en lugar de pack

        button_compare = ctk.CTkButton(self.sidebar_frame, text="Comparar Resultados", command=self.compare_algorithms)
        button_compare.grid(pady=10)  # Usar grid en lugar de pack

        # CENTER MAIN FRAME
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Result Text Widget
        self.result_text = ctk.CTkTextbox(self.main_frame, width=400, height=200)
        self.result_text.pack(padx=10, pady=10)

        # Configure grid weights to allow resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def run_greedy(self):
        self.cancelar_animaciones()
        self.clear_dashboard()
        capacidad, objetos = self.read_input()
        if not objetos:
            return
        
        # Start timer for pure logic
        start_time_real = time.perf_counter()
        mochila, valor_total, steps = mochila_voraz(capacidad, objetos)
        end_time_real = time.perf_counter()
        real_execution_time = end_time_real - start_time_real
        
        self.display_results("Algoritmo Voraz", real_execution_time, valor_total, mochila)
        
        # Draw step-by-step animation
        self.draw_greedy_step_by_step(steps, objetos)

    def run_dynamic(self):
        self.cancelar_animaciones()
        self.clear_dashboard()
        capacidad, objetos = self.read_input()
        if not objetos:
            return
        
        # Start timer for pure logic
        start_time_real = time.perf_counter()
        mochila, valor_total, dp_matrix = mochila_dinamica(capacidad, objetos)
        end_time_real = time.perf_counter()
        real_execution_time = end_time_real - start_time_real
        
        self.display_results("Programación Dinámica", real_execution_time, valor_total, mochila)
        
        # Draw DP matrix
        self.draw_dp_matrix(dp_matrix)

    def compare_algorithms(self):
        self.cancelar_animaciones()
        self.clear_dashboard()
        capacidad, objetos = self.read_input()
        if not objetos:
            return
        
        # Ejecutar algoritmo voraz
        start_time_voraz_real = time.perf_counter()
        mochila_voraz_result, valor_total_voraz, steps_voraz = mochila_voraz(capacidad, objetos)
        end_time_voraz_real = time.perf_counter()
        execution_time_voraz_real = end_time_voraz_real - start_time_voraz_real
        
        # Ejecutar algoritmo dinámico
        start_time_dynamic_real = time.perf_counter()
        mochila_dynamic_result, valor_total_dynamic, dp_matrix = mochila_dinamica(capacidad, objetos)
        end_time_dynamic_real = time.perf_counter()
        execution_time_dynamic_real = end_time_dynamic_real - start_time_dynamic_real
        
        self.display_results("Algoritmo Voraz", execution_time_voraz_real, valor_total_voraz, mochila_voraz_result)
        self.result_text.insert(ctk.END, "\n")
        self.display_results("Programación Dinámica", execution_time_dynamic_real, valor_total_dynamic, mochila_dynamic_result)
        
        # Visualización
        fig, ax = plt.subplots(1, 2, figsize=(16, 4))
        
        # Chart A: Execution Time
        ax[0].bar(['Voraz', 'Dinámica'], [execution_time_voraz_real, execution_time_dynamic_real], color=['blue', 'green'])
        ax[0].set_ylabel('Tiempo de ejecución (segundos)')
        ax[0].set_title('Comparación de Tiempos de Ejecución')
        
        # Chart B: Total Value
        ax[1].bar(['Voraz', 'Dinámica'], [valor_total_voraz, valor_total_dynamic], color=['blue', 'green'])
        ax[1].set_ylabel('Valor total')
        ax[1].set_title('Comparación de Valores Totales')
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    def on_closing(self):
        self.cancelar_animaciones()
        self.destroy()

    def cancelar_animaciones(self):
        for after_id in self.after_ids:
            self.after_cancel(after_id)
        self.after_ids.clear()

    def clear_dashboard(self):
        if hasattr(self, 'result_text'):
            self.result_text.delete(1.0, ctk.END)
        
        # Cancel all pending animations
        for animation_id in self.animation_ids:
            self.after_cancel(animation_id)
        self.animation_ids.clear()

    def display_results(self, algorithm_name, execution_time, total_value, items):
        self.result_text.insert(ctk.END, f"{algorithm_name}\n")
        self.result_text.insert(ctk.END, f"Tiempo de ejecución: {execution_time:.6f} segundos\n")
        self.result_text.insert(ctk.END, f"Valor total: {total_value}\n")
        self.result_text.insert(ctk.END, f"Objetos en la mochila: {items}\n")

    def draw_greedy_step_by_step(self, steps, objetos):
        # Create a scrollable frame for the table
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create headers
        header_labels = ["ID", "Valor", "Peso", "Ratio"]
        for i, label in enumerate(header_labels):
            ctk.CTkLabel(self.scrollable_frame, text=label).grid(row=0, column=i, padx=5, pady=5)

        # Create rows for each object
        self.rows = []
        for step in steps:
            row = {}
            row["id"] = ctk.CTkLabel(self.scrollable_frame, text=str(step["obj"]))
            row["id"].grid(row=len(steps) + 1, column=0)
            row["value"] = ctk.CTkLabel(self.scrollable_frame, text=str(objetos[step["obj"]][0]))
            row["value"].grid(row=len(steps) + 1, column=1)
            row["weight"] = ctk.CTkLabel(self.scrollable_frame, text=str(objetos[step["obj"]][1]))
            row["weight"].grid(row=len(steps) + 1, column=2)
            row["ratio"] = ctk.CTkLabel(self.scrollable_frame, text=f"{objetos[step['obj']][0] / objetos[step['obj']][1]:.2f}")
            row["ratio"].grid(row=len(steps) + 1, column=3)
            self.rows.append(row)

        # Animate the steps
        for i, step in enumerate(steps):
            def highlight_row(step_index=i):
                if step_index < len(self.rows):
                    row = self.rows[step_index]
                    color = "green" if step["fit"] else "red"
                    row["id"].configure(fg_color=color)
                    row["value"].configure(fg_color=color)
                    row["weight"].configure(fg_color=color)
                    row["ratio"].configure(fg_color=color)
            self.after(ANIMATION_SPEED * i, highlight_row)

    def draw_dp_matrix(self, matrix):
        # Create a scrollable frame for the matrix
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create headers
        header_labels = [""] + list(range(len(matrix[0])))
        for i, label in enumerate(header_labels):
            ctk.CTkLabel(self.scrollable_frame, text=str(label)).grid(row=0, column=i, padx=5, pady=5)

        # Create rows for each capacity
        self.rows = []
        for i, row in enumerate(matrix):
            row_data = {}
            row_data["id"] = ctk.CTkLabel(self.scrollable_frame, text=str(i))
            row_data["id"].grid(row=i + 1, column=0)
            for j, value in enumerate(row):
                label = ctk.CTkLabel(self.scrollable_frame, text=str(value))
                label.grid(row=i + 1, column=j + 1)
                row_data[j] = label
            self.rows.append(row_data)

        # Animate the backtracking path
        def animate_backtracking(i=0, w=len(matrix[0]) - 1):
            if i < len(matrix) and w >= 0:
                if matrix[i][w] != matrix[i - 1][w]:
                    self.rows[i][w].configure(fg_color="gold")
                    self.after(DP_SPEED, animate_backtracking, i - 1, w - matrix[i-1][1])
                else:
                    self.after(DP_SPEED, animate_backtracking, i - 1, w)

        animate_backtracking(len(matrix) - 1, len(matrix[0]) - 1)

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
