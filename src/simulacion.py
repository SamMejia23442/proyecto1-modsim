from .models import Usuario
from .generadores_otros import generar_beta, generar_gamma, funcion_logistica, ensayo_bernoulli
from .generadores_poisson import poisson_producto_uniformes

class MotorSimulacion:
    """
    Motor central que orquesta la simulación de Tinder.
    Maneja el estado global de los usuarios, iteraciones temporales
    y la cola de perfiles.
    """
    def __init__(self, num_usuarios: int = 1000):
        self.num_usuarios = num_usuarios
        self.usuarios = {}
        self.tiempo_actual = 0.0
        
    def inicializar_usuarios(self):
        for i in range(self.num_usuarios):
            # Deseabilidad típica Beta(2, 5) donde pocos son muy deseables
            des = generar_beta(2, 5)
            # Exigencia Beta(3, 3) más centrada
            exig = generar_beta(3, 3)
            self.usuarios[i] = Usuario(id_usuario=i, deseabilidad=des, exigencia=exig)
            
    def simular_sesiones(self):
        # Para cada usuario simulamos una sesión
        for i, usuario in self.usuarios.items():
            # Cuántos perfiles verá en esta sesión (Poisson)
            num_perfiles = poisson_producto_uniformes(lam=15)
            
            for _ in range(num_perfiles):
                perfil_id = self._seleccionar_perfil_aleatorio(excluir=i)
                perfil = self.usuarios[perfil_id]
                
                # Calcular probabilidad de like
                prob_like = funcion_logistica(perfil.deseabilidad, usuario.exigencia)
                dio_like = ensayo_bernoulli(prob_like)
                
                if dio_like == 1:
                    usuario.dar_like(perfil_id)
                    # Revisar si hay match (si el otro ya le había dado like a este)
                    if i in perfil.likes_dados:
                        usuario.registrar_match(perfil_id)
                        perfil.registrar_match(i)

    def _seleccionar_perfil_aleatorio(self, excluir):
        # Simplificación: escoge un ID al azar que no sea el mismo
        import random
        candidato = excluir
        while candidato == excluir:
            candidato = random.randint(0, self.num_usuarios - 1)
        return candidato
        
    def ejecutar(self):
        self.inicializar_usuarios()
        self.simular_sesiones()
