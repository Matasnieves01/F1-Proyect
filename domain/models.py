class Corredor:
    def __init__(self, nombre, pais, equipo, numero_auto, puntos, foto_url, edad=None, podios=None, victorias=None):
        self.nombre = nombre
        self.pais = pais
        self.equipo = equipo
        self.numero_auto = numero_auto
        self.puntos = puntos
        self.foto_url = foto_url
        self.edad = edad
        self.podios = podios if podios is not None else 0
        self.victorias = victorias if victorias is not None else 0

    def __str__(self):
        return f"{self.nombre} ({self.pais}) - Equipo: {self.equipo}, Puntos: {self.puntos}"
