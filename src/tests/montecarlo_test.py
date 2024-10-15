import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd

class montecarlo_test:
    def __init__(self, root, results):
        self.root = root
        self.root.title("Simulación Monte Carlo")
        self.results = results 

        # Entradas para los parámetros de Monte Carlo
        tk.Label(self.root, text="Inversión Inicial:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_investment = tk.Entry(self.root)
        self.entry_investment.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Media:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_mean = tk.Entry(self.root)
        self.entry_mean.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Desviación Estándar:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_stddev = tk.Entry(self.root)
        self.entry_stddev.grid(row=2, column=1, padx=5, pady=5)

        # Botón para ejecutar la simulación
        self.btn_simulate = tk.Button(self.root, text="Ejecutar Simulación", command=self.run_montecarlo_test)
        self.btn_simulate.grid(row=3, column=0, columnspan=2, pady=10)

        # Área de texto para mostrar los resultados
        self.result_box = tk.Text(self.root, height=10, width=50)
        self.result_box.grid(row=4, column=0, columnspan=2)

    def run_montecarlo_test(self):
        """Realizar la simulación de Monte Carlo"""
        try:
            # Obtener los parámetros de entrada
            investment = float(self.entry_investment.get())
            mean = float(self.entry_mean.get())
            stddev = float(self.entry_stddev.get())

            # Convertir los resultados generados en valores R
            R = [mean + stddev * (2 * ri - 1) for ri in self.results]

            # Calcular los valores de inversión V = inversión inicial * (1 + R)
            V = [investment * (1 + r) for r in R]

            # Calcular estadísticas
            expected_value = np.mean(V)
            percentil_95 = np.percentile(V, 95)

            # Mostrar los resultados en el área de texto
            self.result_box.delete(1.0, tk.END)
            for i, v in enumerate(V):
                self.result_box.insert(tk.END, f"Iteración {i+1}: Valor de Inversión = {v:.2f}\n")

            # Mostrar estadísticas
            self.result_box.insert(tk.END, f"\nValor Esperado E[V]: {expected_value:.2f}\n")
            self.result_box.insert(tk.END, f"Percentil 95: {percentil_95:.2f}\n")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos para todos los parámetros.")
