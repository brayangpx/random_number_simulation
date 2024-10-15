# src/tests/poker_test.py
from collections import Counter
from scipy.stats import chi2

def clasificar_numero(numero):
    """
    Clasifica un número Rs según sus dígitos en categorías:
    'Poker', 'Trio', 'Dos Pares', 'Un Par', 'Todos Diferentes'.
    """
    numero_str = f"{numero:.4f}".split(".")[1]  # Convertir el número a 4 decimales y tomar la parte decimal
    conteo_digitos = Counter(numero_str)  # Contar los dígitos de la parte decimal
    frecuencias = sorted(conteo_digitos.values(), reverse=True)  # Ordenar frecuencias de mayor a menor
    
    # Clasificar según las frecuencias de los dígitos
    if frecuencias == [4]:
        return 'Poker'
    elif frecuencias == [3, 1]:
        return 'Trio'
    elif frecuencias == [2, 2]:
        return 'Dos Pares'
    elif frecuencias == [2, 1, 1]:
        return 'Un Par'
    else:
        return 'Todos Diferentes'

def contar_frecuencias(rs_values):
    """
    Cuenta las frecuencias de cada categoría ('Poker', 'Trio', etc.)
    para los números Rs proporcionados.
    """
    categorias = {'Todos Diferentes': 0, 'Un Par': 0, 'Dos Pares': 0, 'Trio': 0, 'Poker': 0}
    for numero in rs_values:
        categoria = clasificar_numero(numero)  # Clasificar cada número
        categorias[categoria] += 1  # Contar cada categoría
    return categorias

def calcular_chi_cuadrado(frecuencias_observadas, total_numeros):
    """
    Calcula el estadístico de chi-cuadrado comparando las frecuencias
    observadas con las esperadas para las diferentes categorías.
    """
    probabilidades_esperadas = {
        'Todos Diferentes': 0.5040,
        'Un Par': 0.4320,
        'Dos Pares': 0.0270,
        'Trio': 0.0360,
        'Poker': 0.0010
    }

    chi_square_stat = 0
    for categoria in probabilidades_esperadas:
        frecuencia_esperada = probabilidades_esperadas[categoria] * total_numeros  # Frecuencia esperada
        frecuencia_observada = frecuencias_observadas[categoria]  # Frecuencia observada
        # Fórmula de chi-cuadrado
        chi_square_stat += ((frecuencia_observada - frecuencia_esperada) ** 2) / frecuencia_esperada

    return chi_square_stat

def poker_test(rs_values):
    """
    Ejecuta la prueba de Póker para los valores Rs proporcionados,
    clasificando los números y calculando el estadístico de chi-cuadrado.
    """
    total_numeros = len(rs_values)
    
    # Contar las frecuencias observadas de las categorías
    frecuencias_observadas = contar_frecuencias(rs_values)
    
    # Calcular el valor de chi-cuadrado
    chi_square_stat = calcular_chi_cuadrado(frecuencias_observadas, total_numeros)
    
    # Grados de libertad: 5 categorías - 1 = 4
    grados_de_libertad = 4
    alpha = 0.05  # Nivel de significancia
    
    # Valor crítico de chi-cuadrado para el nivel de significancia y grados de libertad
    chi_critical = chi2.ppf(1 - alpha, grados_de_libertad)
    
    # Evaluar si se cumple la hipótesis nula
    cumple = "Sí" if chi_square_stat <= chi_critical else "No"

    # Retornar el resultado detallado
    return (f"Frecuencias observadas: {frecuencias_observadas}\n"
            f"Valor de Chi-cuadrado: {chi_square_stat:.4f}\n"
            f"Valor crítico (alfa={alpha}): {chi_critical:.4f}\n"
            f"¿Cumple con la independencia esperada?: {cumple}")
