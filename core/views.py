import requests
from django.shortcuts import render
from datetime import datetime, timezone
from use_cases.race_service import categorize_races
from django.template.loader import get_template
from .models import Escuderia

def index(request):
    actuales, futuras, pasadas = categorize_races()
    return render(request, 'index.html', {
        'actuales': actuales,
        'futuras': futuras,
        'pasadas': pasadas
    })


# Create your views here.
def carreras_view(request):
    url = 'https://ergast.com/api/f1/current.json'
    response = requests.get(url)
    actuales = []
    futuras = []
    pasadas = []

    if response.status_code == 200:
        data = response.json()
        races = data['MRData']['RaceTable']['Races']
        for race in races:
            fecha_str = race['date']+"T"+race.get('time', '00:00:00Z')
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            ahora = datetime.now(timezone.utc)

            carrera = {
                'nombre': race['raceName'],
                'lugar': race['Circuit']['Location']['locality'] + ", " + race['Circuit']['Location']['country'],
                'fecha_inicio': fecha_obj,
                'estado': '',
                'descripcion': f"{race['Circuit']['circuitName']} - {race['Circuit']['Location']['country']}",
            }

            #Clasificacion por tiempo
            if abs((fecha_obj - ahora).total_seconds()) < 3600*3:
                carrera['estado'] = 'En curso'
                actuales.append(carrera)
            elif fecha_obj > ahora:
                carrera['estado'] = 'Próxima'
                futuras.append(carrera)
            else:
                carrera['estado'] = 'Finalizada'
                pasadas.append(carrera)

    context = {
        'actuales': actuales,
        'futuras': futuras,
        'pasadas': pasadas,
    }
    return render(request, 'carreras.html', {'carreras': context})

def test_template(request):
    context = {
        'actuales': [
            {
                'nombre': 'Gran Premio Test',
                'lugar': 'Ciudad Test, País Test',
                'fecha_inicio': datetime.now(),
                'estado': 'En curso',
                'descripcion': 'Circuito de prueba',
            }
        ],
        'futuras': [],
        'pasadas': [],
    }
    return render(request, 'index.html', context)

def pilotos(request):
    return render(request, 'pilots.html')

def lista_escuderias(request):
    escuderias = Escuderia.objects.all()
    return render(request, 'escuderias/lista.html', {'escuderias': escuderias})