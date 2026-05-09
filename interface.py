import customtkinter as ctk
from tkinter import messagebox, ttk, TclError
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import sys

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

        # Configure the main window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Problema de la Mochila")
        self.geometry("1200x800")
        self.configure(bg="#000000")

        # TOP NAVIGATION (Tabs)
        self.tab_control = ttk.Notebook(self, style="TNotebook")
        self.tab_control.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

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
        self.grid_columnconfigure(0, weight=1)

        # Add exit protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def init_tab_voraz(self):
        # Top (Controls): Centered button "Ejecutar"
        self.button_run_greedy = ctk.CTkButton(self.tab_voraz, text="Ejecutar", command=self.run_greedy)
        self.button_run_greedy.grid(row=0, column=0, padx=10, pady=10)

        # Center (Visuals): A frame that takes the most space (weight=1) to show the animation
        self.scrollable_frame_greedy = ctk.CTkScrollableFrame(self.tab_voraz, fg_color="#000000")
        self.scrollable_frame_greedy.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Bottom (Stats): A horizontal frame with "Cards" showing Total Value, Weight, and Time in big, centered text
        self.stats_frame_greedy = ctk.CTkFrame(self.tab_voraz, fg_color="#000000")
        self.stats_frame_greedy.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.total_value_label_greedy = ctk.CTkLabel(self.stats_frame_greedy, text="Valor Total: 0", font=("Arial", 24), anchor="center")
        self.total_value_label_greedy.grid(row=0, column=0, padx=10, pady=10)

        self.total_weight_label_greedy = ctk.CTkLabel(self.stats_frame_greedy, text="Peso Total: 0", font=("Arial", 24), anchor="center")
        self.total_weight_label_greedy.grid(row=0, column=1, padx=10, pady=10)

        self.execution_time_label_greedy = ctk.CTkLabel(self.stats_frame_greedy, text="Tiempo: 0.00 s", font=("Arial", 24), anchor="center")
        self.execution_time_label_greedy.grid(row=0, column=2, padx=10, pady=10)

        # Result Text
        self.result_text_greedy = ctk.CTkTextbox(self.tab_voraz, width=400, height=100, fg_color="#000000", corner_radius=10)
        self.result_text_greedy.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

    def init_tab_dinamica(self):
        # Top (Controls): Centered button "Ejecutar"
        self.button_run_dynamic = ctk.CTkButton(self.tab_dinamica, text="Ejecutar", command=self.run_dynamic)
        self.button_run_dynamic.grid(row=0, column=0, padx=10, pady=10)

        # Middle (Visuals): DP Matrix animation area (scrollable)
        self.scrollable_frame_dynamic = ctk.CTkScrollableFrame(self.tab_dinamica, fg_color="#000000")
        self.scrollable_frame_dynamic.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Bottom (Stats): A horizontal frame with "Cards" showing Total Value, Weight, and Time in big, centered text
        self.stats_frame_dynamic = ctk.CTkFrame(self.tab_dinamica, fg_color="#000000")
        self.stats_frame_dynamic.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.total_value_label_dynamic = ctk.CTkLabel(self.stats_frame_dynamic, text="Valor Total: 0", font=("Arial", 24), anchor="center")
        self.total_value_label_dynamic.grid(row=0, column=0, padx=10, pady=10)

        self.total_weight_label_dynamic = ctk.CTkLabel(self.stats_frame_dynamic, text="Peso Total: 0", font=("Arial", 24), anchor="center")
        self.total_weight_label_dynamic.grid(row=0, column=1, padx=10, pady=10)

        self.execution_time_label_dynamic = ctk.CTkLabel(self.stats_frame_dynamic, text="Tiempo: 0.00 s", font=("Arial", 24), anchor="center")
        self.execution_time_label_dynamic.grid(row=0, column=2, padx=10, pady=10)

        # Result Text
        self.result_text_dynamic = ctk.CTkTextbox(self.tab_dinamica, width=400, height=100, fg_color="#000000", corner_radius=10)
        self.result_text_dynamic.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

    def init_tab_comparacion(self):
        # Add a CTkButton labeled "Generar Gráficas"
        self.button_generate_graphs = ctk.CTkButton(self.tab_comparacion, text="Generar Gráficas", command=self.compare_algorithms)
        self.button_generate_graphs.grid(row=0, column=0, padx=10, pady=10)

        # Canvas for the comparison charts
        self.canvas_compare = FigureCanvasTkAgg(None, master=self.tab_comparacion)
        self.canvas_compare.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

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
        plt.style.use('dark_background')
        fig, ax = plt.subplots(1, 2, figsize=(16, 4), facecolor="#000000")
        
        # Chart A: Execution Time
        ax[0].bar(['Voraz', 'Dinámica'], [self.last_voraz_results['execution_time'], self.last_dinamica_results['execution_time']], color=['blue', 'green'])
        ax[0].set_ylabel('Tiempo de ejecución (segundos)', color='white')
        ax[0].tick_params(axis='y', colors='white')
        ax[0].set_title('Comparación de Tiempos de Ejecución', color='white')
        
        # Chart B: Total Value
        ax[1].bar(['Voraz', 'Dinámica'], [self.last_voraz_results['total_value'], self.last_dinamica_results['total_value']], color=['blue', 'green'])
        ax[1].set_ylabel('Valor total', color='white')
        ax[1].tick_params(axis='y', colors='white')
        ax[1].set_title('Comparación de Valores Totales', color='white')
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.tab_comparacion)
        canvas.draw()
        self.canvas_compare.get_tk_widget().grid_forget()  # Remove previous canvas
        self.canvas_compare = canvas
        self.canvas_compare.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def on_closing(self):
        # 1. Cancelar todas las animaciones pendientes
        self.cancelar_animaciones()

        # 2. Detener cualquier actualización de GUI pendiente
        self.update_idletasks()

        # 3. Cerrar todos los gráficos de Matplotlib
        plt.close('all')

        # 4. Destruir la ventana de forma segura
        self.destroy()

        # 5. Matar el proceso de Python por completo
        sys.exit(0)

    def cancelar_animaciones(self):
        for after_id in self.animation_ids:
            try:
                self.after_cancel(after_id)
            except TclError:
                pass
        self.animation_ids = []

    def clear_dashboard(self, tab_name):
        if tab_name == "Voraz":
            self.result_text_greedy.delete(1.0, ctk.END)
            # Cancel all pending animations
            for animation_id in self.animation_ids:
                try:
                    self.after_cancel(animation_id)
                except TclError:
                    pass
            self.animation_ids.clear()
        elif tab_name == "Dinámica":
            self.result_text_dynamic.delete(1.0, ctk.END)
            # Cancel all pending animations
            for animation_id in self.animation_ids:
                try:
                    self.after_cancel(animation_id)
                except TclError:
                    pass
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
            ctk.CTkLabel(self.scrollable_frame_greedy, text=label, fg_color="#1f538d").grid(row=0, column=i, padx=5, pady=5)

        # Create rows for each object
        self.rows_greedy = []
        self.current_step_index = 0

        def add_next_row():
            if self.current_step_index < len(steps):
                step = steps[self.current_step_index]
                row = {}
                row["id"] = ctk.CTkLabel(self.scrollable_frame_greedy, text=str(step["obj"]), fg_color="#000000", anchor="center")
                row["id"].grid(row=self.current_step_index + 1, column=0)
                row["value"] = ctk.CTkLabel(self.scrollable_frame_greedy, text=str(objetos[step["obj"]][0]), fg_color="#000000", anchor="center")
                row["value"].grid(row=self.current_step_index + 1, column=1)
                row["weight"] = ctk.CTkLabel(self.scrollable_frame_greedy, text=str(objetos[step["obj"]][1]), fg_color="#000000", anchor="center")
                row["weight"].grid(row=self.current_step_index + 1, column=2)
                row["ratio"] = ctk.CTkLabel(self.scrollable_frame_greedy, text=f"{objetos[step['obj']][0] / objetos[step['obj']][1]:.2f}", fg_color="#000000", anchor="center")
                row["ratio"].grid(row=self.current_step_index + 1, column=3)
                self.rows_greedy.append(row)

                # Update stats
                if step["fit"]:
                    valor_total = float(self.total_value_label_greedy.cget("text").split(": ")[1])
                    peso_total = float(self.total_weight_label_greedy.cget("text").split(": ")[1])
                    valor_total += objetos[step["obj"]][0]
                    peso_total += objetos[step["obj"]][1]
                    self.total_value_label_greedy.configure(text=f"Valor Total: {valor_total:.2f}")
                    self.total_weight_label_greedy.configure(text=f"Peso Total: {peso_total:.2f}")

                # Highlight the row
                color = "green" if step["fit"] else "red"
                row["id"].configure(fg_color=color)
                row["value"].configure(fg_color=color)
                row["weight"].configure(fg_color=color)
                row["ratio"].configure(fg_color=color)

                self.current_step_index += 1
                self.after(ANIMATION_SPEED, add_next_row)

        add_next_row()

    def draw_dp_matrix(self, matrix):
        # Create headers
        header_labels = [""] + list(range(len(matrix[0])))
        for i, label in enumerate(header_labels):
            ctk.CTkLabel(self.scrollable_frame_dynamic, text=str(label), fg_color="#1f538d").grid(row=0, column=i, padx=5, pady=5)

        # Create rows for each capacity
        self.rows_dynamic = []
        for i, row in enumerate(matrix):
            row_data = {}
            row_data["id"] = ctk.CTkLabel(self.scrollable_frame_dynamic, text=str(i), fg_color="#000000", anchor="center")
            row_data["id"].grid(row=i + 1, column=0)
            for j, value in enumerate(row):
                label = ctk.CTkLabel(self.scrollable_frame_dynamic, text=str(value), fg_color="#000000", anchor="center")
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
