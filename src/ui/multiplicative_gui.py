import tkinter as tk
from tkinter import messagebox
from src.generators.multiplicative_generator import MultiplicativeGenerator
from src.tests.series_test import series_test, plot_series_scatter, show_frequencies_table
from src.tests.up_down_test import run_test_above_below, plot_runs_above_below  
from src.tests.montecarlo_test import montecarlo_test  
from src.tests.poker_test import poker_test  # Importar la prueba de Póker
import scipy.stats as stats

class MultiplicativeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador Multiplicativo")
        self.results = []  # Para almacenar los números generados
        self.create_widgets()

    def create_widgets(self):
        # Entradas de parámetros
        tk.Label(self.root, text="Constante a:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_a = tk.Entry(self.root)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Módulo m:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_m = tk.Entry(self.root)
        self.entry_m.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Semilla:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_seed = tk.Entry(self.root)
        self.entry_seed.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Número de Iteraciones:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_n = tk.Entry(self.root)
        self.entry_n.grid(row=3, column=1, padx=5, pady=5)

        # Botón para generar los números
        btn_generar = tk.Button(self.root, text="Generar Números", command=self.generar_numeros)
        btn_generar.grid(row=4, column=0, columnspan=2, pady=10)

        # Área de texto para mostrar los números generados
        self.resultado = tk.Text(self.root, height=10, width=50)
        self.resultado.grid(row=5, column=0, columnspan=2)

        # Botón para ejecutar Monte Carlo
        self.btn_montecarlo = tk.Button(self.root, text="Simulación Monte Carlo", command=self.open_montecarlo_window, state=tk.DISABLED)
        self.btn_montecarlo.grid(row=6, column=0, columnspan=2, pady=10)

        # Botones para las pruebas
        self.btn_series = tk.Button(self.root, text="Prueba de Series", command=self.run_series_test, state=tk.DISABLED)
        self.btn_series.grid(row=7, column=0, columnspan=1, padx=5, pady=5)

        self.btn_up_down = tk.Button(self.root, text="Prueba Arriba y Abajo", command=self.run_up_down_test, state=tk.DISABLED)
        self.btn_up_down.grid(row=7, column=1, columnspan=1, padx=5, pady=5)

        self.btn_poker = tk.Button(self.root, text="Prueba de Póker", command=self.run_poker_test, state=tk.DISABLED)
        self.btn_poker.grid(row=8, column=0, columnspan=2, pady=10)

    def generar_numeros(self):
        try:
            a = int(self.entry_a.get())
            m = int(self.entry_m.get())
            seed = int(self.entry_seed.get())
            n = int(self.entry_n.get())

            # Crear una instancia del generador multiplicativo
            generator = MultiplicativeGenerator(a, m, seed)
            self.results = generator.generate(n)

            # Mostrar los resultados
            self.resultado.delete(1.0, tk.END)
            for i, num in enumerate(self.results):
                self.resultado.insert(tk.END, f"Iteración {i+1}: {num:.6f}\n")

            # Habilitar los botones de las pruebas
            self.btn_series.config(state=tk.NORMAL)
            self.btn_up_down.config(state=tk.NORMAL)
            self.btn_montecarlo.config(state=tk.NORMAL)
            self.btn_poker.config(state=tk.NORMAL)

        except ValueError:
            messagebox.showerror("Error", "Todos los parámetros deben ser números enteros.")

    def run_series_test(self):
        try:
            k = 5  # Dividir en una cuadrícula de 5x5
            chi_square, frequencies, pairs, expected = series_test(self.results, k)

            # Mostrar la tabla de frecuencias
            df_frequencies = show_frequencies_table(frequencies)

            # Mostrar la gráfica de dispersión
            plot_series_scatter(pairs)

            # Determinar si cumple con la independencia esperada
            result = f"Valor de Chi-cuadrado: {chi_square:.4f}\nFrecuencia esperada: {expected:.4f}"
            messagebox.showinfo("Resultado de la Prueba de Series", result)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def run_up_down_test(self):
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

    def open_montecarlo_window(self):
        """Abrir la ventana de Monte Carlo para realizar la simulación"""
        if not self.results:
            messagebox.showerror("Error", "Por favor, genera los números antes de ejecutar Monte Carlo.")
            return

        # Crear una nueva ventana para la simulación de Monte Carlo
        montecarlo_window = tk.Toplevel(self.root)
        montecarlo_test(montecarlo_window, self.results)  # Pasar los resultados generados a la clase MonteCarloTest

    def run_poker_test(self):
        try:
            # Verificar si hay resultados generados
            if not self.results:
                messagebox.showerror("Error", "No hay números generados para realizar la prueba de Póker.")
                return

            # Ejecutar la prueba de Póker
            poker_result = poker_test(self.results)

            # Mostrar el resultado en un cuadro de diálogo
            messagebox.showinfo("Resultado de la Prueba de Póker", poker_result)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def run_series_test(self):
        """Ejecutar la prueba de series"""
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
