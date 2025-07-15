import requests
import os
from django.shortcuts import render
from datetime import datetime, timezone
from use_cases.race_service import categorize_races
from django.template.loader import get_template
import fastf1
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
from use_cases.race_service import categorize_races
from collections import defaultdict
def index(request):
    actuales, futuras, pasadas = categorize_races()
    return render(request, 'index.html', {
        'actuales': actuales,
        'futuras': futuras,
        'pasadas': pasadas
    })




def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def season_list(request):
    current_year = datetime.now().year
    seasons = list(range(2003, current_year + 1))
    return render(request, 'season_list.html', {'seasons': seasons})


def race_list(request, year):
    year = int(year)

    cache_dir = '.f1cache'
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)

    try:
        schedule = fastf1.get_event_schedule(year)
    except Exception as e:
        return render(request, 'race_list.html', {
            'year': year,
            'error': f"Failed to load schedule: {e}",
            'races': []
        })

    races = []

    for _, row in schedule.iterrows():
        round_num = int(row['RoundNumber'])
        event_name = row['EventName']
        winner = "N/A"
        pole = "N/A"

        # Try to get race winner
        try:
            race = fastf1.get_session(year, round_num, 'R')
            race.load(telemetry=False, laps=False, weather=False)
            if race.results is not None and not race.results.empty:
                winner = race.results.sort_values('Position').iloc[0]['FullName']
        except Exception as e:
            print(f"[Race {round_num}] Failed to get race winner: {e}")

        # Try to get pole sitter
        try:
            quali = fastf1.get_session(year, round_num, 'Q')
            quali.load(telemetry=False, laps=False, weather=False)
            if quali.results is not None and not quali.results.empty:
                pole = quali.results.sort_values('Position').iloc[0]['FullName']
        except Exception as e:
            print(f"[Race {round_num}] Failed to get pole position: {e}")

        races.append({
            'round': round_num,
            'event': event_name,
            'winner': winner,
            'pole': pole
        })

    return render(request, 'race_list.html', {
        'year': year,
        'races': races,
        'error': None
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