import tkinter as tk
from tkinter import ttk, messagebox
from src.tests.poker_test import poker_test  # Asegúrate de que esta importación sea correcta
from src.tests.montecarlo_test import montecarlo_test  # Importar la clase MonteCarloTest
from src.tests.series_test import series_test, plot_series_scatter, show_frequencies_table
import scipy.stats as stats
from src.tests.up_down_test import run_test_above_below, plot_runs_above_below 

class AdditiveGeneratorGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.result = []  # Array para almacenar los valores Rs generados
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta para el valor de 'm'
        self.m_label = tk.Label(self, text="Ingrese el valor de m (módulo):")
        self.m_label.pack(pady=5)

        # Entrada para el valor de 'm'
        self.m_entry = tk.Entry(self)
        self.m_entry.pack(pady=5)

        # Etiqueta para las semillas iniciales
        self.seed_label = tk.Label(self, text="Ingrese las semillas separadas por comas (ej: 65,98,89,3,69):")
        self.seed_label.pack(pady=5)

        # Entrada para las semillas
        self.seed_entry = tk.Entry(self)
        self.seed_entry.pack(pady=5)

        # Botón para generar números
        self.generate_btn = tk.Button(self, text="Generar Números Aleatorios", command=self.generate_numbers)
        self.generate_btn.pack(pady=10)

        # Crear tablas con scrollbar para las semillas, los números generados y los Rs
        self.seed_table, self.seed_scrollbar = self.create_table_with_scrollbar("Semillas Iniciales")
        self.generated_table, self.generated_scrollbar = self.create_table_with_scrollbar("Números Generados")
        self.rs_table, self.rs_scrollbar = self.create_table_with_scrollbar("Valores Rs")

        # Botones para las pruebas
        self.poker_test_btn = tk.Button(self, text="Prueba de Póker", command=self.run_poker_test)
        self.poker_test_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.series_test_btn = tk.Button(self, text="Prueba de Series", command=self.run_series_test)
        self.series_test_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.up_down_test_btn = tk.Button(self, text="Prueba de Arriba/Abajo", command=self.run_up_down_test)
        self.up_down_test_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_montecarlo = tk.Button(self, text="Simulación Montecarlo", command=self.open_montecarlo_window)
        self.btn_montecarlo.pack(side=tk.LEFT, padx=5, pady=10)

    def create_table_with_scrollbar(self, title):
        # Crear un marco (frame) para organizar el Treeview y el Scrollbar
        frame = tk.Frame(self)
        frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Etiqueta para el título de la tabla
        label = tk.Label(frame, text=title)
        label.pack()

        # Crear el Treeview para la tabla
        table = ttk.Treeview(frame, columns=("Valor"), show="headings", height=5)
        table.heading("Valor", text="Valor")
        table.column("Valor", anchor=tk.CENTER)

        # Crear el Scrollbar y vincularlo con el Treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar los widgets (Treeview y Scrollbar)
        table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return table, scrollbar

    def generate_numbers(self):
        try:
            # Obtener los valores ingresados
            m = int(self.m_entry.get())
            seeds = list(map(int, self.seed_entry.get().split(',')))

            # Validar el tamaño de la semilla
            if len(seeds) < 2:
                raise ValueError("Se necesitan al menos 2 semillas.")

            # Llamar al método aditivo para generar los números
            generated_numbers = self.additive_method(seeds, m, len(seeds) * 2)  # Duplicar la cantidad de números

            # Calcular los Rs
            rs_values = [round(num / (m - 1), 4) for num in generated_numbers]
            self.result = rs_values  # Guardar los Rs generados en self.result

            # Limpiar tablas antes de insertar los nuevos resultados
            self.clear_table(self.seed_table)
            self.clear_table(self.generated_table)
            self.clear_table(self.rs_table)

            # Insertar semillas iniciales
            for seed in seeds:
                self.seed_table.insert("", "end", values=(seed,))

            # Insertar números generados
            for num in generated_numbers:
                self.generated_table.insert("", "end", values=(num,))

            # Insertar valores Rs
            for rs in rs_values:
                self.rs_table.insert("", "end", values=(rs,))

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_table(self, table):
        # Limpiar todas las filas de una tabla
        for row in table.get_children():
            table.delete(row)

    def additive_method(self, seeds, m, total):
        # Implementación del método aditivo
        vArranque = seeds[:]
        resultado = []

        for i in range(total - len(seeds)):
            # Sumamos el primer valor con el último y aplicamos el módulo
            nuevo_valor = (vArranque[0] + vArranque[-1]) % m
            resultado.append(nuevo_valor)
            # Actualizamos el array, removemos el más antiguo y añadimos el nuevo valor
            vArranque.append(nuevo_valor)
            vArranque.pop(0)

        # Retornar los valores generados
        return resultado

    # Métodos para las pruebas
    def run_poker_test(self):
        # Llama a la función de prueba de Póker con los valores Rs almacenados en self.result
        if self.result:
            poker_result = poker_test(self.result)
            messagebox.showinfo("Resultado de la Prueba de Póker", poker_result)
        else:
            messagebox.showwarning("Advertencia", "No hay valores Rs generados para la prueba.")

    def run_series_test(self):
        """ Ejecutar la prueba de series """
        try:
            k = 5  # Dividir en una cuadrícula de 5x5
            chi_square, frequencies, pairs, expected = series_test(self.result, k)

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
        try:
            z_value, runs, expected_mean, expected_std_dev = run_test_above_below(self.result)

            # Mostrar la gráfica de la prueba arriba-abajo
            plot_runs_above_below(self.result)

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
        if not self.result:
            messagebox.showerror("Error", "Por favor, genera los números antes de ejecutar Monte Carlo.")
            return

        # Crear una nueva ventana para la simulación de Monte Carlo
        montecarlo_window = tk.Toplevel(self.master)  # Cambié self.root a self.master
        montecarlo_test(montecarlo_window, self.result)  # Pasar los resultados generados a la clase MonteCarloTest

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = AdditiveGeneratorGUI(master=root)
    app.master.title("Generador Aditivo")
    app.mainloop()
