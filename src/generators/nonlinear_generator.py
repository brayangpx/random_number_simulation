# src/generators/nonlinear_generator.py
class NonLinearMethodGenerator:
    def __init__(self, a, b, c, m, X0):
        self.a = a
        self.b = b
        self.c = c
        self.m = m
        self.X0 = X0

    def generate(self, n):
        """
        Genera las iteraciones del método no lineal.
        :param n: Número de iteraciones.
        :return: Lista de resultados de las iteraciones con X_n y r_n.
        """
        iterations = []
        Xn = self.X0  # Inicializamos Xn con X0

        for i in range(n):
            Xn_function = (self.a * (Xn**2) + self.b * Xn + self.c)
            Xn_next = Xn_function % self.m
            rn = Xn_next / self.m  # Calculamos el residuo rn
            iterations.append([i + 1, rn, Xn_next,Xn_function])
            Xn = Xn_next  # Actualizamos Xn para la siguiente iteración

        return iterations
