import tkinter as tk
from tkinter import messagebox, ttk
from src.tests.montecarlo_test import montecarlo_test, show_montecarlo_results
from src.generators.nonlinear_generator import NonLinearMethodGenerator

class MonteCarloGUI:
    def __init__(self, root):
        self.root = root
        self.results = []  # Para almacenar los números generados
        self.create_widgets()

    def create_widgets(self):
        # Crear etiquetas y entradas para los parámetros
        tk.Label(self.root, text="Inversión inicial: ").grid(row=0, column=0, padx=5, pady=5)
        self.entry_investment = tk.Entry(self.root)
        self.entry_investment.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Número de simulaciones: ").grid(row=1, column=0, padx=5, pady=5)
        self.entry_simulations = tk.Entry(self.root)
        self.entry_simulations.grid(row=1, column=1, padx=5, pady=5)

        # Botón para ejecutar la simulación
        self.btn_run = tk.Button(self.root, text="Generar Números", command=self.generate_numbers)
        self.btn_run.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón para ejecutar Monte Carlo
        self.btn_montecarlo = tk.Button(self.root, text="Simulación Monte Carlo", state=tk.DISABLED, command=self.run_montecarlo_test)
        self.btn_montecarlo.grid(row=3, column=0, columnspan=2, pady=10)

        # Crear un Treeview para mostrar los resultados
        columns = ("Estadística", "Valor")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("Estadística", text="Estadística")
        self.tree.heading("Valor", text="Valor")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def generate_numbers(self):
        """Generar números usando el método no lineal"""
        try:
            # Parámetros fijos para el generador no lineal
            a, b, c, m, X0, iterations = 7, 5, 11, 16, 3, int(self.entry_simulations.get())

            # Crear una instancia del generador no lineal y generar los números
            generator = NonLinearMethodGenerator(a, b, c, m, X0)
            raw_results = generator.generate(iterations)

            # Extraer solo los valores de X_n para `self.results`
            self.results = [row[1] for row in raw_results]  # Asumiendo que X_n está en la posición 1

            # Habilitar el botón de Monte Carlo
            self.btn_montecarlo.config(state=tk.NORMAL)

            messagebox.showinfo("Éxito", "Números generados exitosamente.")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")

    def run_montecarlo_test(self):
        """Realizar la simulación de Monte Carlo"""
        try:
            investment = float(self.entry_investment.get())
            
            # Realizar la simulación de Monte Carlo
            simulated_values, expected_value, percentil_95 = montecarlo_test(investment, self.results)

            # Mostrar los resultados
            show_montecarlo_results(simulated_values, expected_value, percentil_95)

            # Limpiar la tabla anterior
            self.tree.delete(*self.tree.get_children())

            # Insertar los resultados en la tabla
            self.tree.insert("", tk.END, values=("E[V] (Valor Esperado)", f"{expected_value:.2f}"))
            self.tree.insert("", tk.END, values=("Percentil 95", f"{percentil_95:.2f}"))

        except ValueError as e:
            messagebox.showerror("Error", str(e))
