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

        button_greedy = ctk.CTkButton(self.sidebar_frame, text="Voraz", command=lambda: self.show_tab("Voraz"))
        button_greedy.grid(pady=10)  # Usar grid en lugar de pack

        button_dynamic = ctk.CTkButton(self.sidebar_frame, text="Dinámica", command=lambda: self.show_tab("Dinámica"))
        button_dynamic.grid(pady=10)  # Usar grid en lugar de pack

        button_compare = ctk.CTkButton(self.sidebar_frame, text="Comparación", command=lambda: self.show_tab("Comparación"))
        button_compare.grid(pady=10)  # Usar grid en lugar de pack

        # CENTER MAIN FRAME
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Tabs
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(expand=True, fill='both')

        self.tab_voraz = ttk.Frame(self.tab_control)
        self.tab_dinamica = ttk.Frame(self.tab_control)
        self.tab_comparacion = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_voraz, text="Voraz")
        self.tab_control.add(self.tab_dinamica, text="Dinámica")
        self.tab_control.add(self.tab_comparacion, text="Comparación")

        # Initialize tabs
        self.init_tab_voraz()
        self.init_tab_dinamica()
        self.init_tab_comparacion()

        # Configure grid weights to allow resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def init_tab_voraz(self):
        # Top: "Ejecutar" button + Input File loader
        self.button_run_greedy = ctk.CTkButton(self.tab_voraz, text="Ejecutar", command=self.run_greedy)
        self.button_run_greedy.pack(pady=10)

        # Middle: Table animation area
        self.scrollable_frame_greedy = ctk.CTkScrollableFrame(self.tab_voraz)
        self.scrollable_frame_greedy.pack(padx=10, pady=10, fill="both", expand=True)

        # Bottom: Metrics (Time, Value)
        self.result_text_greedy = ctk.CTkTextbox(self.tab_voraz, width=400, height=100)
        self.result_text_greedy.pack(padx=10, pady=10)

    def init_tab_dinamica(self):
        # Top: "Ejecutar" button + Input File loader
        self.button_run_dynamic = ctk.CTkButton(self.tab_dinamica, text="Ejecutar", command=self.run_dynamic)
        self.button_run_dynamic.pack(pady=10)

        # Middle: DP Matrix animation area (scrollable)
        self.scrollable_frame_dynamic = ctk.CTkScrollableFrame(self.tab_dinamica)
        self.scrollable_frame_dynamic.pack(padx=10, pady=10, fill="both", expand=True)

        # Bottom: Metrics (Time, Value)
        self.result_text_dynamic = ctk.CTkTextbox(self.tab_dinamica, width=400, height=100)
        self.result_text_dynamic.pack(padx=10, pady=10)

    def init_tab_comparacion(self):
        # No "Ejecutar" button here; only displays the charts comparing the last saved results of both algorithms
        self.canvas_compare = FigureCanvasTkAgg(None, master=self.tab_comparacion)
        self.canvas_compare.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)

    def show_tab(self, tab_name):
        self.cancelar_animaciones()
        if tab_name == "Voraz":
            self.tab_control.select(self.tab_voraz)
        elif tab_name == "Dinámica":
            self.tab_control.select(self.tab_dinamica)
        elif tab_name == "Comparación":
            self.tab_control.select(self.tab_comparacion)
            self.compare_algorithms()

    def run_greedy(self):
        self.cancelar_animaciones()
        self.clear_dashboard("Voraz")
        capacidad, objetos = self.read_input()
        if not objetos:
            return
        
        # Start timer for pure logic
        start_time_real = time.perf_counter()
        mochila, valor_total, steps = mochila_voraz(capacidad, objetos)
        end_time_real = time.perf_counter()
        real_execution_time = end_time_real - start_time_real
        
        self.display_results("Voraz", real_execution_time, valor_total, mochila, "Voraz")
        
        # Draw step-by-step animation
        self.draw_greedy_step_by_step(steps, objetos)

    def run_dynamic(self):
        self.cancelar_animaciones()
        self.clear_dashboard("Dinámica")
        capacidad, objetos = self.read_input()
        if not objetos:
            return
        
        # Start timer for pure logic
        start_time_real = time.perf_counter()
        mochila, valor_total, dp_matrix = mochila_dinamica(capacidad, objetos)
        end_time_real = time.perf_counter()
        real_execution_time = end_time_real - start_time_real
        
        self.display_results("Dinámica", real_execution_time, valor_total, mochila, "Dinámica")
        
        # Draw DP matrix
        self.draw_dp_matrix(dp_matrix)

    def compare_algorithms(self):
        if not hasattr(self, 'last_voraz_results') or not hasattr(self, 'last_dinamica_results'):
            messagebox.showwarning("Advertencia", "No hay resultados para comparar. Ejecuta ambos algoritmos primero.")
            return
        
        # Visualización
        fig, ax = plt.subplots(1, 2, figsize=(16, 4))
        
        # Chart A: Execution Time
        ax[0].bar(['Voraz', 'Dinámica'], [self.last_voraz_results['execution_time'], self.last_dinamica_results['execution_time']], color=['blue', 'green'])
        ax[0].set_ylabel('Tiempo de ejecución (segundos)')
        ax[0].set_title('Comparación de Tiempos de Ejecución')
        
        # Chart B: Total Value
        ax[1].bar(['Voraz', 'Dinámica'], [self.last_voraz_results['total_value'], self.last_dinamica_results['total_value']], color=['blue', 'green'])
        ax[1].set_ylabel('Valor total')
        ax[1].set_title('Comparación de Valores Totales')
        
        canvas = FigureCanvasTkAgg(fig, master=self.tab_comparacion)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def on_closing(self):
        self.cancelar_animaciones()
        self.destroy()

    def cancelar_animaciones(self):
        for after_id in self.after_ids:
            self.after_cancel(after_id)
        self.after_ids.clear()

        for animation_id in self.animation_ids:
            self.after_cancel(animation_id)
        self.animation_ids.clear()

    def clear_dashboard(self, tab_name):
        if tab_name == "Voraz":
            self.result_text_greedy.delete(1.0, ctk.END)
            # Cancel all pending animations
            for animation_id in self.animation_ids:
                self.after_cancel(animation_id)
            self.animation_ids.clear()
        elif tab_name == "Dinámica":
            self.result_text_dynamic.delete(1.0, ctk.END)
            # Cancel all pending animations
            for animation_id in self.animation_ids:
                self.after_cancel(animation_id)
            self.animation_ids.clear()

    def display_results(self, algorithm_name, execution_time, total_value, items, tab_name):
        if tab_name == "Voraz":
            self.result_text_greedy.insert(ctk.END, f"{algorithm_name}\n")
            self.result_text_greedy.insert(ctk.END, f"Tiempo de ejecución: {execution_time:.6f} segundos\n")
            self.result_text_greedy.insert(ctk.END, f"Valor total: {total_value}\n")
            self.result_text_greedy.insert(ctk.END, f"Objetos en la mochila: {items}\n")
            self.last_voraz_results = {
                'execution_time': execution_time,
                'total_value': total_value
            }
        elif tab_name == "Dinámica":
            self.result_text_dynamic.insert(ctk.END, f"{algorithm_name}\n")
            self.result_text_dynamic.insert(ctk.END, f"Tiempo de ejecución: {execution_time:.6f} segundos\n")
            self.result_text_dynamic.insert(ctk.END, f"Valor total: {total_value}\n")
            self.result_text_dynamic.insert(ctk.END, f"Objetos en la mochila: {items}\n")
            self.last_dinamica_results = {
                'execution_time': execution_time,
                'total_value': total_value
            }

    def draw_greedy_step_by_step(self, steps, objetos):
        # Create headers
        header_labels = ["ID", "Valor", "Peso", "Ratio"]
        for i, label in enumerate(header_labels):
            ctk.CTkLabel(self.scrollable_frame_greedy, text=label).grid(row=0, column=i, padx=5, pady=5)

        # Create rows for each object
        self.rows_greedy = []
        for step in steps:
            row = {}
            row["id"] = ctk.CTkLabel(self.scrollable_frame_greedy, text=str(step["obj"]))
            row["id"].grid(row=len(steps) + 1, column=0)
            row["value"] = ctk.CTkLabel(self.scrollable_frame_greedy, text=str(objetos[step["obj"]][0]))
            row["value"].grid(row=len(steps) + 1, column=1)
            row["weight"] = ctk.CTkLabel(self.scrollable_frame_greedy, text=str(objetos[step["obj"]][1]))
            row["weight"].grid(row=len(steps) + 1, column=2)
            row["ratio"] = ctk.CTkLabel(self.scrollable_frame_greedy, text=f"{objetos[step['obj']][0] / objetos[step['obj']][1]:.2f}")
            row["ratio"].grid(row=len(steps) + 1, column=3)
            self.rows_greedy.append(row)

        # Animate the steps
        for i, step in enumerate(steps):
            def highlight_row(step_index=i):
                if step_index < len(self.rows_greedy):
                    row = self.rows_greedy[step_index]
                    color = "green" if step["fit"] else "red"
                    row["id"].configure(fg_color=color)
                    row["value"].configure(fg_color=color)
                    row["weight"].configure(fg_color=color)
                    row["ratio"].configure(fg_color=color)
            self.after(ANIMATION_SPEED * i, highlight_row)

    def draw_dp_matrix(self, matrix):
        # Create headers
        header_labels = [""] + list(range(len(matrix[0])))
        for i, label in enumerate(header_labels):
            ctk.CTkLabel(self.scrollable_frame_dynamic, text=str(label)).grid(row=0, column=i, padx=5, pady=5)

        # Create rows for each capacity
        self.rows_dynamic = []
        for i, row in enumerate(matrix):
            row_data = {}
            row_data["id"] = ctk.CTkLabel(self.scrollable_frame_dynamic, text=str(i))
            row_data["id"].grid(row=i + 1, column=0)
            for j, value in enumerate(row):
                label = ctk.CTkLabel(self.scrollable_frame_dynamic, text=str(value))
                label.grid(row=i + 1, column=j + 1)
                row_data[j] = label
            self.rows_dynamic.append(row_data)

        # Animate the backtracking path
        def animate_backtracking(i=len(matrix) - 1, w=len(matrix[0]) - 1):
            if i >= 0 and w >= 0:
                if matrix[i][w] != (matrix[i - 1][w] if i > 0 else 0):
                    self.rows_dynamic[i][w].configure(fg_color="gold")
                    self.after(DP_SPEED, animate_backtracking, i - 1, w - (matrix[i-1][1] if i > 0 else 0))
                else:
                    self.after(DP_SPEED, animate_backtracking, i - 1, w)

        animate_backtracking()

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
