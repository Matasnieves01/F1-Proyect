from f1_drivers.models import CorredorModel

def agregar_corredor(nombre, pais, equipo, numero_auto, puntos, foto_url, edad=None, podios=0, victorias=0):
    corredor = CorredorModel.objects.create(
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
    return corredor

def obtener_corredores():
    return CorredorModel.objects.all()

def buscar_corredor_por_nombre(nombre):
    try:
        return CorredorModel.objects.get(nombre__iexact=nombre)
    except CorredorModel.DoesNotExist:
        return None
