from domain.models import Corredor
from infrastructure.repositories import corredor_repository

def registrar_corredor(nombre, pais, equipo, numero_auto, puntos, foto_url, edad=None, podios=None, victorias=None):
    nuevo_corredor = Corredor(
        nombre=nombre,
        pais=pais,
        equipo=equipo,
        numero_auto=numero_auto,
        puntos=puntos,
        foto_url=foto_url,
        edad=edad,
        podios=podios,
        victorias=victorias
    )
    corredor_repository.agregar_corredor(nuevo_corredor)
    return nuevo_corredor

def listar_corredores():
    return corredor_repository.obtener_corredores()

def mostrar_corredor(nombre):
    corredor = corredor_repository.buscar_corredor_por_nombre(nombre)
    if corredor:
        return str(corredor)
    return "Corredor no encontrado"
