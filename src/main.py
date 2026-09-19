import random

def inicializar_simulacion():
    print("Inicializando la simulación de Tinder...")
    # Configuración base y parámetros globales
    random.seed(42) # Para reproducibilidad de las partes de control (los generadores manuales usarán su propia lógica)
    
if __name__ == "__main__":
    inicializar_simulacion()
    print("Arquitectura base configurada.")
