import random
from src.simulacion import MotorSimulacion

def inicializar_simulacion():
    print("Inicializando la simulación de Tinder...")
    # Configuración base y parámetros globales
    random.seed(42)
    
    motor = MotorSimulacion(num_usuarios=1000)
    print("Ejecutando simulación...")
    motor.ejecutar()
    print("Simulación finalizada.")
    return motor
    
if __name__ == "__main__":
    motor = inicializar_simulacion()
