from django.db import models

# Create your models here.

class Escuderia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    logo = models.URLField(blank=True)
    año_fundación = models.IntegerField()
    campeonatos = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre
    
class ChatMessage(models.Model):
    user = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.user}: {self.content}"