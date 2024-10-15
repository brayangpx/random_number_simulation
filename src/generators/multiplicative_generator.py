# src/generators/multiplicative_generator.py

class MultiplicativeGenerator:
    def __init__(self, a, m, seed):
        if seed == 0:
            raise ValueError("La semilla no puede ser cero en un generador multiplicativo.")
        self.a = a  # Constante multiplicativa
        self.m = m  # Módulo
        self.seed = seed  # Semilla inicial

    def generate(self, n):
        """
        Genera n números aleatorios utilizando el método de congruencia multiplicativa.
        :param n: Número de valores a generar.
        :return: Lista de n números generados.
        """
        numbers = []
        x = self.seed
        for _ in range(n):
            x = (self.a * x) % self.m
            numbers.append(x / self.m)  # Normalizar a [0, 1]
        return numbers