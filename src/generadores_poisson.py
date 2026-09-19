import math
import random

def poisson_producto_uniformes(lam):
    """
    Genera un valor Poisson usando el método del producto de números uniformes.
    Ideal para valores pequeños/moderados de lambda.
    """
    L = math.exp(-lam)
    k = 0
    p = 1.0
    
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            return k - 1

def poisson_suma_exponenciales(lam):
    """
    Genera un valor Poisson sumando tiempos exponenciales.
    Basado en el proceso de Poisson.
    """
    k = 0
    t = 0.0
    
    while True:
        # Generar tiempo exponencial E ~ Exp(lam) usando inversa de Uniforme
        # t += -ln(U) / lam -> Pero para simular en el intervalo [0,1] con tasa lam:
        u = random.random()
        t -= math.log(u) # tiempo exponencial estandarizado
        if t > lam:
            return k
        k += 1

def poisson_aceptacion_rechazo(lam):
    """
    Generador de Poisson usando un método aproximado (Aceptación-Rechazo / Normal) 
    útil para lambdas altos donde exp(-lam) es muy pequeño y causa underflow.
    Aquí se implementa una versión básica de AR si lam es alto.
    """
    # Si lam es bajo, caemos a producto de uniformes
    if lam < 10:
        return poisson_producto_uniformes(lam)
        
    c = 0.767 - 3.36 / lam
    beta = math.pi / math.sqrt(3.0 * lam)
    alpha = beta * lam
    k = math.log(c) - lam - math.log(beta)
    
    while True:
        u = random.random()
        x = (alpha - math.log((1.0 - u) / u)) / beta
        n = int(math.floor(x + 0.5))
        
        if n < 0:
            continue
            
        v = random.random()
        y = alpha - beta * x
        
        # log-factorial aproximado de n
        log_n_fact = math.lgamma(n + 1)
        
        # Criterio de rechazo
        if k + n * math.log(lam) - log_n_fact >= math.log(v * (1.0 + math.exp(y))**2):
            return n
