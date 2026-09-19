import random
import math

# Generador Uniforme U(0,1) base
def generar_uniforme():
    """Genera un número aleatorio uniforme U(0,1)"""
    return random.random()

def generar_exponencial(tasa_lambda):
    """
    Genera un valor Exponencial usando el método de la Transformada Inversa.
    Fórmula: X = -(1/lambda) * ln(U)
    """
    u = generar_uniforme()
    # Para evitar log(0)
    while u == 0:
        u = generar_uniforme()
    return -(1.0 / tasa_lambda) * math.log(u)

def generar_bernoulli(probabilidad):
    """
    Genera un valor Bernoulli (1 = éxito, 0 = fracaso) por Transformada Inversa.
    """
    u = generar_uniforme()
    return 1 if u <= probabilidad else 0

def generar_beta(alpha, beta_param):
    """
    Genera un valor Beta(alpha, beta) usando el algoritmo de Johnk.
    Este algoritmo usa la transformada inversa y aceptación/rechazo en U(0,1).
    """
    while True:
        u1 = generar_uniforme()
        u2 = generar_uniforme()
        # Para evitar divisiones o bases en cero
        if u1 == 0 or u2 == 0:
            continue
        y1 = u1 ** (1.0 / alpha)
        y2 = u2 ** (1.0 / beta_param)
        if y1 + y2 <= 1.0:
            return y1 / (y1 + y2)

def generar_gamma_entera(k, theta):
    """
    Genera un valor Gamma(k, theta) donde k es un entero (distribución Erlang).
    Fórmula: X = -theta * ln(U1 * U2 * ... * Uk)
    """
    producto_u = 1.0
    for _ in range(int(k)):
        u = generar_uniforme()
        while u == 0:
            u = generar_uniforme()
        producto_u *= u
    return -theta * math.log(producto_u)

def calcular_probabilidad_like(deseabilidad_perfil, exigencia_usuario):
    """
    Calcula la probabilidad de que un usuario le dé like a un perfil
    usando una función logística dependiente de la diferencia.
    """
    diferencia = deseabilidad_perfil - exigencia_usuario
    return 1.0 / (1.0 + math.exp(-10 * diferencia))
