from django.db import models

class CorredorModel(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=50)
    equipo = models.CharField(max_length=100)
    numero_auto = models.IntegerField()
    puntos = models.IntegerField()
    foto_url = models.URLField()
    edad = models.IntegerField(null=True, blank=True)
    podios = models.IntegerField(default=0)
    victorias = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - {self.equipo} ({self.puntos} pts)"
