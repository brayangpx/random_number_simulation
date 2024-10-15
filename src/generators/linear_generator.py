# src/generators/linear_generator.py

class LinearGenerator:
    def __init__(self, a, c, m, seed):
        self.a = a  # Constante multiplicativa
        self.c = c  # Constante aditiva
        self.m = m  # Módulo
        self.seed = seed

    def generate(self, n):
        """
        Genera `n` números aleatorios utilizando el método de congruencia lineal.
        :param n: Número de valores a generar.
        :return: Lista de `n` números generados.
        """
        numbers = []
        x = self.seed
        for _ in range(n):
            x = (self.a * x + self.c) % self.m
            numbers.append(x / self.m)  # Normalizar a [0, 1]
        return numbers
