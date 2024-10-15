import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox

def run_test_above_below(numbers):
    """
    Realiza la prueba de corridas arriba-abajo y devuelve el valor de Z, la cantidad de corridas y la media esperada.
    :param numbers: Lista de números generados.
    :return: valor de Z, cantidad de corridas, media esperada y desviación estándar esperada.
    """
    if len(numbers) < 2:
        raise ValueError("Se necesitan al menos dos números para realizar la prueba de corridas.")

    # Crear una secuencia de arriba-abajo (1 = arriba, -1 = abajo)
    median = np.median(numbers)
    sequence = [1 if num > median else -1 for num in numbers]

    # Contar el número de corridas
    runs = 1  # La primera siempre cuenta como corrida
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i-1]:
            runs += 1

    # Cálculo de la media y la desviación estándar esperadas
    n = len(numbers)
    n1 = sum(1 for num in numbers if num > median)  # Elementos arriba de la mediana
    n2 = n - n1  # Elementos abajo de la mediana

    expected_mean = (2 * n1 * n2 / n) + 1
    expected_std_dev = np.sqrt((2 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1)))

    # Cálculo del valor Z
    z_value = (runs - expected_mean) / expected_std_dev

    return z_value, runs, expected_mean, expected_std_dev

def plot_runs_above_below(numbers):
    """
    Genera una gráfica que muestra los valores por encima y por debajo de la mediana.
    """
    median = np.median(numbers)
    above = [num if num > median else np.nan for num in numbers]
    below = [num if num <= median else np.nan for num in numbers]

    plt.figure(figsize=(10, 6))
    plt.plot(numbers, label='Valores')
    plt.plot(above, 'go', label='Por Encima de la Mediana', markersize=8)
    plt.plot(below, 'ro', label='Por Debajo de la Mediana', markersize=8)
    plt.axhline(median, color='blue', linestyle='--', label=f'Mediana = {median:.4f}')
    plt.title('Prueba de Corridas Arriba-Abajo')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid(True)
    plt.show()
