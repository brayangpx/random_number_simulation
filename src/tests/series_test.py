# tests/series_test.py
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
import pandas as pd

def series_test(numbers, k=5):
    """Realiza la prueba de series y devuelve el valor de Chi-cuadrado, las frecuencias y los pares."""
    if len(numbers) < 2:
        raise ValueError("Se necesitan al menos dos números para realizar la prueba de series.")
    
    # Tabla de frecuencias
    frequencies = np.zeros((k, k))
    pairs = [(numbers[i], numbers[i + 1]) for i in range(len(numbers) - 1)]

    # Rellenar la tabla de frecuencias
    for (x1, x2) in pairs:
        i = min(int(x1 * k), k - 1)
        j = min(int(x2 * k), k - 1)
        frequencies[i, j] += 1

    # Cálculo de Chi-cuadrado
    n_pairs = len(pairs)
    expected_frequency = n_pairs / (k * k)
    chi_square = np.sum((frequencies - expected_frequency) ** 2 / expected_frequency)

    return chi_square, frequencies, pairs, expected_frequency

def plot_series_scatter(pairs):
    """Genera una gráfica de dispersión de los pares consecutivos."""
    plt.figure(figsize=(6, 6))
    plt.scatter(*zip(*pairs), marker="o", color="blue", alpha=0.7)
    plt.title("Prueba de Series: Gráfico de Pares Consecutivos")
    plt.xlabel("x_i")
    plt.ylabel("x_{i+1}")
    plt.grid(True)
    plt.show()

def show_frequencies_table(frequencies):
    """Muestra una tabla con las frecuencias observadas en cada intervalo."""
    df = pd.DataFrame(frequencies)
    df.columns = [f"Intervalo {i+1}" for i in range(frequencies.shape[1])]
    df.index = [f"Intervalo {i+1}" for i in range(frequencies.shape[0])]
    print("Tabla de Frecuencias Observadas:")
    print(df)
    return df
