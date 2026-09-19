class Usuario:
    """
    Representa un usuario activo en la simulación de Tinder.
    """
    def __init__(self, id_usuario, deseabilidad, exigencia):
        self.id_usuario = id_usuario
        self.deseabilidad = deseabilidad
        self.exigencia = exigencia
        self.likes_dados = set() # IDs de usuarios a los que les ha dado like
        self.matches = set() # IDs de usuarios con los que hizo match
        self.tiempo_inicio_sesion = 0.0

    def dar_like(self, otro_usuario_id):
        self.likes_dados.add(otro_usuario_id)
        
    def registrar_match(self, otro_usuario_id):
        self.matches.add(otro_usuario_id)

    def __repr__(self):
        return f"Usuario(ID={self.id_usuario}, Des={self.deseabilidad:.2f}, Exig={self.exigencia:.2f})"
