import math
from scipy import stats

def prueba_kolmogorov_smirnov(datos, distribucion_teorica, **params):
    """
    Prueba KS real para validar generadores de variables continuas.
    Compara la distribución acumulada empírica de 'datos' contra la teórica.

    Distribuciones soportadas:
      - 'exponencial': params = {'lam': float}
      - 'beta':        params = {'alpha': float, 'beta': float}
      - 'gamma':       params = {'alpha': float, 'beta': float}

    Retorna: (estadistico_D, p_value)
      - p_value > 0.05 → no rechazamos H0 (el generador produce la distribución correcta)
      - p_value ≤ 0.05 → rechazamos H0 (el generador tiene problemas)
    """
    if distribucion_teorica == 'exponencial':
        # Exponencial: media = 1/lam → scale = 1/lam
        lam = params.get('lam', 1.0)
        D, p = stats.kstest(datos, 'expon', args=(0, 1.0 / lam))

    elif distribucion_teorica == 'beta':
        alpha = params.get('alpha', 2.0)
        beta  = params.get('beta',  5.0)
        D, p = stats.kstest(datos, 'beta', args=(alpha, beta))

    elif distribucion_teorica == 'gamma':
        alpha = params.get('alpha', 2.0)
        beta  = params.get('beta',  1.0)
        # scipy Gamma: shape=alpha, scale=beta
        D, p = stats.kstest(datos, 'gamma', args=(alpha, 0, beta))

    else:
        raise ValueError(f"Distribución '{distribucion_teorica}' no reconocida.")

    return D, p


def prueba_chi_cuadrado(datos_poisson, lam):
    """
    Prueba Chi-cuadrado real para validar el generador de Poisson.
    Compara las frecuencias observadas de 'datos_poisson' contra las
    frecuencias esperadas de una Poisson(lam).

    Retorna: (estadistico_chi2, p_value)
      - p_value > 0.05 → no rechazamos H0 (el generador produce Poisson correcta)
      - p_value ≤ 0.05 → rechazamos H0
    """
    n = len(datos_poisson)
    k_max = int(max(datos_poisson)) + 1

    # Frecuencias observadas
    observadas = [0] * (k_max + 1)
    for val in datos_poisson:
        k = int(val)
        if k <= k_max:
            observadas[k] += 1

    # Frecuencias esperadas según Poisson(lam)
    probs = []
    for k in range(k_max + 1):
        prob_k = (math.exp(-lam) * (lam ** k)) / math.factorial(k) if k <= 170 else 0.0
        probs.append(prob_k)
    # Normalizar probs para que sumen exactamente 1 (evita errores de precisión flotante)
    total_prob = sum(probs)
    probs = [p / total_prob for p in probs]
    esperadas = [p * n for p in probs]

    # Agrupamos colas para que cada celda tenga freq esperada >= 5
    obs_agr, esp_agr = [], []
    acum_obs, acum_esp = 0, 0.0
    for o, e in zip(observadas, esperadas):
        acum_obs += o
        acum_esp += e
        if acum_esp >= 5:
            obs_agr.append(acum_obs)
            esp_agr.append(acum_esp)
            acum_obs, acum_esp = 0, 0.0
    if acum_obs > 0:  # resto al último bin
        if obs_agr:
            obs_agr[-1] += acum_obs
            esp_agr[-1] += acum_esp
        else:
            obs_agr.append(acum_obs)
            esp_agr.append(acum_esp)

    # Renormalizar esperadas al total observado exacto
    factor = sum(obs_agr) / sum(esp_agr)
    esp_agr = [e * factor for e in esp_agr]

    chi2, p = stats.chisquare(f_obs=obs_agr, f_exp=esp_agr)
    return chi2, p


def generar_reporte_visual(motor):
    """
    Imprime estadísticas finales y ejecuta las pruebas estadísticas reales
    sobre los datos generados por el motor de simulación.
    """
    import random
    from src.generadores_poisson import poisson_producto_uniformes
    from src.generadores_otros import generar_exponencial, generar_beta

    total_matches = sum(len(u.matches) for u in motor.usuarios.values())
    usuarios_sin_match = sum(1 for u in motor.usuarios.values() if len(u.matches) == 0)

    print("=== Análisis de Resultados ===")
    print(f"Total de usuarios simulados: {motor.num_usuarios}")
    print(f"Total de matches formados: {total_matches // 2}")
    print(f"Usuarios que no consiguieron match: {usuarios_sin_match} "
          f"({(usuarios_sin_match / motor.num_usuarios) * 100:.2f}%)")
    print(f"Matches promedio por usuario: {(total_matches / motor.num_usuarios):.4f}")

    # ── Generamos muestras frescas para validar cada generador ───────────────
    N_MUESTRAS = 5000
    LAM_EXP    = 10.0   # tasa del proceso exponencial
    LAM_POIS   = 15.0   # lambda de Poisson (igual que en la simulación)

    muestras_exp  = [generar_exponencial(LAM_EXP) for _ in range(N_MUESTRAS)]
    muestras_beta = [generar_beta(2, 5)            for _ in range(N_MUESTRAS)]
    muestras_pois = [poisson_producto_uniformes(LAM_POIS) for _ in range(N_MUESTRAS)]

    # ── Prueba KS para Exponencial ───────────────────────────────────────────
    D_exp, p_exp = prueba_kolmogorov_smirnov(muestras_exp, 'exponencial', lam=LAM_EXP)

    # ── Prueba KS para Beta(2,5) ─────────────────────────────────────────────
    D_beta, p_beta = prueba_kolmogorov_smirnov(muestras_beta, 'beta', alpha=2, beta=5)

    # ── Prueba Chi-cuadrado para Poisson(15) ─────────────────────────────────
    chi2_pois, p_pois = prueba_chi_cuadrado(muestras_pois, lam=LAM_POIS)

    print("\n=== Validación Estadística (α = 0.05) ===")
    print(f"KS  | Exponencial(λ={LAM_EXP})  → D={D_exp:.4f},  p-value={p_exp:.4f}  "
          f"→ {'✅ No rechazamos H0' if p_exp > 0.05 else '❌ Rechazamos H0'}")
    print(f"KS  | Beta(2, 5)               → D={D_beta:.4f},  p-value={p_beta:.4f}  "
          f"→ {'✅ No rechazamos H0' if p_beta > 0.05 else '❌ Rechazamos H0'}")
    print(f"χ²  | Poisson(λ={LAM_POIS})       → χ²={chi2_pois:.4f}, p-value={p_pois:.4f}  "
          f"→ {'✅ No rechazamos H0' if p_pois > 0.05 else '❌ Rechazamos H0'}")
