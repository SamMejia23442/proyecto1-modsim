import time
import math
from generadores_base import generar_uniforme, generar_exponencial

def poisson_metodo_1(tasa_lambda):
    """
    Método 1: Producto de números uniformes.
    Sigue multiplicando U(0,1) hasta que el producto caiga por debajo de e^(-lambda).
    Ideal para valores pequeños o moderados de lambda.
    """
    # Si lambda es muy grande, e^(-lambda) da underflow (0.0). Se maneja como caso límite.
    if tasa_lambda > 700: 
        L = 0.0
    else:
        L = math.exp(-tasa_lambda)
        
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= generar_uniforme()
    return k - 1

def poisson_metodo_2(tasa_lambda):
    """
    Método 2: Suma de tiempos exponenciales.
    Acumula tiempos exponenciales entre llegadas hasta que la suma supera 1 unidad de tiempo.
    """
    k = 0
    suma_tiempos = 0.0
    while suma_tiempos <= 1.0:
        # Generar exponencial asume un lambda dado.
        # El tiempo entre eventos de Poisson(lambda) es Exp(lambda).
        tiempo = generar_exponencial(tasa_lambda)
        suma_tiempos += tiempo
        if suma_tiempos <= 1.0:
            k += 1
    return k

def poisson_metodo_3_rechazo(tasa_lambda):
    """
    Método 3: Aceptación y rechazo.
    Implementación sencilla para valores más altos de lambda usando una aproximación.
    En este caso, si lambda > 30, se aproxima a una Normal y se usa AR o similar,
    pero para cumplir con la simulación usaremos una envoltura básica o un método alternativo.
    Aquí implementamos Atkinson's Poisson method (un tipo de aceptación-rechazo) para completitud.
    Retorna también el número de rechazos para métricas.
    """
    c = 0.767 - 3.36 / tasa_lambda
    beta = math.pi / math.sqrt(3.0 * tasa_lambda)
    alpha = beta * tasa_lambda
    k = math.log(c) - tasa_lambda - math.log(beta)
    
    rechazos = 0
    while True:
        u = generar_uniforme()
        x = (alpha - math.log((1.0 - u) / u)) / beta
        n = math.floor(x + 0.5)
        
        if n < 0:
            rechazos += 1
            continue
            
        v = generar_uniforme()
        y = alpha - beta * x
        
        # Factorial usando Gamma function math.gamma(n+1)
        lhs = y + math.log(v / ((1.0 + math.exp(y)) ** 2))
        try:
            rhs = k + n * math.log(tasa_lambda) - math.log(math.gamma(n + 1))
        except OverflowError:
            rhs = float('-inf') # Manejo de desbordamiento de Gamma
            
        if lhs <= rhs:
            return int(n), rechazos
        rechazos += 1

def comparar_metodos_poisson(lambda_test, muestras):
    """
    Compara los 3 métodos generando 'muestras' cantidad de variables
    y mide el tiempo de CPU y la tasa de rechazo del método 3.
    """
    print(f"\\n--- Comparando para lambda={lambda_test}, muestras={muestras} ---")
    
    # Método 1
    inicio = time.time()
    for _ in range(muestras):
        poisson_metodo_1(lambda_test)
    tiempo_m1 = time.time() - inicio
    print(f"Método 1 (Producto U): {tiempo_m1:.4f} segundos")
    
    # Método 2
    inicio = time.time()
    for _ in range(muestras):
        poisson_metodo_2(lambda_test)
    tiempo_m2 = time.time() - inicio
    print(f"Método 2 (Suma Exp): {tiempo_m2:.4f} segundos")
    
    # Método 3
    inicio = time.time()
    rechazos_totales = 0
    # Solo ejecutar Método 3 si lambda es razonablemente grande (ej. > 10) 
    # ya que Atkinson asume lambdas más grandes, para lambdas pequeñas falla.
    if lambda_test > 10:
        for _ in range(muestras):
            _, rechazos = poisson_metodo_3_rechazo(lambda_test)
            rechazos_totales += rechazos
        tiempo_m3 = time.time() - inicio
        tasa_rechazo = rechazos_totales / muestras
        print(f"Método 3 (Rechazo): {tiempo_m3:.4f} segundos, Tasa de rechazo: {tasa_rechazo:.2f} por muestra")
    else:
        print("Método 3 (Rechazo): Ignorado para lambda pequeño (requiere lambda > 10).")

if __name__ == '__main__':
    # Prueba rápida de comparación de métodos
    comparar_metodos_poisson(lambda_test=5, muestras=10000)
    comparar_metodos_poisson(lambda_test=50, muestras=10000)
