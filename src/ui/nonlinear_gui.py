import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import scipy.stats as stats
from src.tests.series_test import series_test, plot_series_scatter, show_frequencies_table
from src.tests.montecarlo_test import montecarlo_test  # Importar la clase MonteCarloTest
from src.generators.nonlinear_generator import NonLinearMethodGenerator
from src.tests.up_down_test import run_test_above_below, plot_runs_above_below  
from src.tests.poker_test import poker_test 

class NonLinearMethodGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Non-Linear Method Simulation")
        self.results = []  # Para almacenar los resultados generados
        self.create_widgets()

    def create_widgets(self):
        # Crear etiquetas y entradas para los parámetros
        tk.Label(self.root, text="Constant g: ").grid(row=0, column=0, padx=5, pady=5)
        self.entry_g = tk.Entry(self.root)
        self.entry_g.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Constant m: ").grid(row=1, column=0, padx=5, pady=5)
        self.entry_m = tk.Entry(self.root)
        self.entry_m.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Constant a: ").grid(row=2, column=0, padx=5, pady=5)
        self.entry_a = tk.Entry(self.root)
        self.entry_a.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Constant b: ").grid(row=3, column=0, padx=5, pady=5)
        self.entry_b = tk.Entry(self.root)
        self.entry_b.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Constant c: ").grid(row=4, column=0, padx=5, pady=5)
        self.entry_c = tk.Entry(self.root)
        self.entry_c.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.root, text="X0: ").grid(row=5, column=0, padx=5, pady=5)
        self.entry_X0 = tk.Entry(self.root)
        self.entry_X0.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Number of iterations: ").grid(row=6, column=0, padx=5, pady=5)
        self.entry_iterations = tk.Entry(self.root)
        self.entry_iterations.grid(row=6, column=1, padx=5, pady=5)

        # Botón para validar y generar tabla
        self.btn_validate = tk.Button(self.root, text="Validate and Generate Table", command=self.generate_numbers)
        self.btn_validate.grid(row=7, column=0, columnspan=2, pady=10)

        # Caja de texto para mostrar los resultados generados
        self.result_box = tk.Text(self.root, height=10, width=50)
        self.result_box.grid(row=8, column=0, columnspan=2)

        # Botón para ejecutar Monte Carlo
        self.btn_montecarlo = tk.Button(self.root, text="Simulación Monte Carlo", command=self.open_montecarlo_window, state=tk.DISABLED)
        self.btn_montecarlo.grid(row=9, column=0, columnspan=2, pady=10)

        # Botones para las pruebas
        self.btn_poker = tk.Button(self.root, text="Prueba de Póker", command=self.run_poker_test, state=tk.DISABLED)
        self.btn_poker.grid(row=10, column=0, padx=5, pady=5, sticky='ew')

        self.btn_series = tk.Button(self.root, text="Prueba de Series", command=self.run_series_test, state=tk.DISABLED)
        self.btn_series.grid(row=10, column=1, padx=5, pady=5, sticky='ew')

        self.btn_up_down = tk.Button(self.root, text="Prueba Arriba y Abajo", command=self.run_up_down_test, state=tk.DISABLED)
        self.btn_up_down.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # Vincular eventos para manejo de Enter y actualización de m
        self.entry_g.bind("<Return>", lambda event: self.focus_next(self.entry_a))  
        self.entry_a.bind("<Return>", lambda event: self.focus_next(self.entry_b))  
        self.entry_b.bind("<Return>", lambda event: self.focus_next(self.entry_c))  
        self.entry_c.bind("<Return>", lambda event: self.focus_next(self.entry_X0))  
        self.entry_X0.bind("<Return>", lambda event: self.focus_next(self.entry_iterations))  
        self.entry_iterations.bind("<Return>", lambda event: self.focus_next(self.btn_validate))  
        self.btn_validate.bind("<Return>", lambda event: self.generate_numbers())  

        # Evento para actualizar el valor de m al cambiar g
        self.entry_g.bind("<KeyRelease>", self.update_m)

    def update_m(self, event=None):
        """ Actualizar el valor de m en función de g (m = 2^g) """
        try:
            g = int(self.entry_g.get())
            m = 2 ** g
            self.entry_m.delete(0, tk.END)  # Limpiar el campo m
            self.entry_m.insert(0, str(m))  # Insertar el nuevo valor
        except ValueError:
            self.entry_m.delete(0, tk.END)  # Limpiar m si g no es válido

    def focus_next(self, next_widget):
        """ Cambiar el foco al siguiente campo """
        next_widget.focus_set()

    def generate_numbers(self):
        """ Generar números usando el método no lineal """
        try:
            # Obtener valores de los campos
            g = int(self.entry_g.get())
            m = int(self.entry_m.get())
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            c = int(self.entry_c.get())
            X0 = int(self.entry_X0.get())
            iterations = int(self.entry_iterations.get())

            # Verificar que m = 2^g
            if m != 2**g:
                messagebox.showerror("Error", "m must be 2^g")
                return

            # Crear una instancia del generador no lineal y generar los números
            generator = NonLinearMethodGenerator(a, b, c, m, X0)
            raw_results = generator.generate(iterations)

            # Extraer solo los valores de X_n para `self.results` (suponiendo que están en la segunda posición de cada fila)
            self.results = [row[1] for row in raw_results]  # Asumiendo que X_n está en la posición 1

            # Mostrar los resultados en la caja de texto
            self.result_box.delete(1.0, tk.END)
            for i, num in enumerate(self.results):
                self.result_box.insert(tk.END, f"Iteración {i+1}: {num}\n")

            # Habilitar el botón de la prueba de series
            self.btn_series.config(state=tk.NORMAL)
            self.btn_up_down.config(state=tk.NORMAL)
            self.btn_poker.config(state=tk.NORMAL)
            self.btn_montecarlo.config(state=tk.NORMAL)

        except ValueError:
            messagebox.showerror("Error", "All parameters must be integers")

    def open_montecarlo_window(self):
        """Abrir la ventana de Monte Carlo para realizar la simulación"""
        if not self.results:
            messagebox.showerror("Error", "Por favor, genera los números antes de ejecutar Monte Carlo.")
            return

        # Crear una nueva ventana para la simulación de Monte Carlo
        montecarlo_window = tk.Toplevel(self.root)
        montecarlo_test(montecarlo_window, self.results)  # Pasar los resultados generados a la clase MonteCarloTest

    def run_series_test(self):
        """ Ejecutar la prueba de series """
        try:
            k = 5  # Dividir en una cuadrícula de 5x5
            chi_square, frequencies, pairs, expected = series_test(self.results, k)

            # Mostrar la tabla de frecuencias
            df_frequencies = show_frequencies_table(frequencies)

            # Mostrar la gráfica de dispersión
            plot_series_scatter(pairs)

            # Calcular el valor crítico de Chi-cuadrado
            degrees_of_freedom = (k * k) - 1
            alpha = 0.05  # Nivel de significancia del 5%
            chi_critical = stats.chi2.ppf(1 - alpha, degrees_of_freedom)

            # Determinar si cumple o no
            cumple = "Sí" if chi_square <= chi_critical else "No"

            # Mostrar resultados
            result = (f"Valor de Chi-cuadrado: {chi_square:.4f}\n"
                      f"Valor crítico (alfa={alpha}): {chi_critical:.4f}\n"
                      f"Frecuencia esperada: {expected:.4f}\n"
                      f"¿Cumple con la independencia esperada?: {cumple}")
            messagebox.showinfo("Resultado de la Prueba de Series", result)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def run_up_down_test(self):
        """ Ejecutar la prueba arriba y abajo """
        try:
            z_value, runs, expected_mean, expected_std_dev = run_test_above_below(self.results)

            # Mostrar la gráfica de la prueba arriba-abajo
            plot_runs_above_below(self.results)

            # Mostrar los resultados
            result = (f"Valor de Z: {z_value:.4f}\n"
                      f"Corridas observadas: {runs}\n"
                      f"Media esperada: {expected_mean:.4f}\n"
                      f"Desviación estándar esperada: {expected_std_dev:.4f}")
            messagebox.showinfo("Resultado de la Prueba Arriba y Abajo", result)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def run_poker_test(self):
        """ Ejecutar la prueba de Póker """
        try:
            # Usamos los resultados generados como entradas para la prueba de Póker
            if not self.results:
                messagebox.showerror("Error", "No hay números generados para realizar la prueba de Póker.")
                return

            # Ejecutamos la prueba de Póker
            poker_result = poker_test(self.results)

            # Mostramos el resultado en un cuadro de diálogo
            messagebox.showinfo("Resultado de la Prueba de Póker", poker_result)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

# Ejecución de la GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = NonLinearMethodGUI(root)
    root.mainloop()
