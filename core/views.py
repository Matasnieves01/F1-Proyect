import requests
import os
import logging
from .models import Escuderia
from django.templatetags.static import static
from datetime import datetime, timezone
import fastf1
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
from use_cases.race_service import categorize_races
from dotenv import load_dotenv
load_dotenv()

# Mapa de imágenes locales para pilotos (fallback)
DRIVER_IMAGES = {
    'Max Verstappen': 'drivers/max_verstappen.jpg',
    'Lando Norris': 'drivers/lando_norris.jpg',
    'Charles Leclerc': 'drivers/charles_leclerc.jpg',
    'Lewis Hamilton': 'drivers/lewis_hamilton.jpg',
    'Oscar Piastri': 'drivers/oscar_piastri.jpg',
    'Carlos Sainz': 'drivers/carlos_sainz.jpg',
    'George Russell': 'drivers/george_russell.jpg',
    'Yuki Tsunoda': 'drivers/yuki_tsunoda.jpg',
    'Alexander Albon': 'drivers/alexander_albon.jpg',
    'Nico Hulkenberg': 'drivers/nico_hulkenberg.jpg',
    'Gabriel Bortoleto': 'drivers/gabriel_bortoleto.jpg',
    'Liam Lawson': 'drivers/liam_lawson.jpg',
    'Isack Hadjar': 'drivers/isack_hadjar.jpg',
    'Lance Stroll': 'drivers/lance_stroll.jpg',
    'Fernando Alonso': 'drivers/fernando_alonso.jpg',
    'Esteban Ocon': 'drivers/esteban_ocon.jpg',
    'Oliver Bearman': 'drivers/oliver_bearman.jpg',
    'Pierre Gasly': 'drivers/pierre_gasly.jpg',
    'Franco Colapinto': 'drivers/franco_colapinto.jpg',
    'Kimi Antonelli': 'drivers/kimi_antonelli.jpg',
}
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
    seasons = list(range(2018, current_year + 1))
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

# Configurar logging para depuración
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carreras_view(request):
    season = request.GET.get('season', '2025')
    url = f'https://api.jolpi.ca/ergast/f1/{season}'
    response = requests.get(url)
    actuales = []
    futuras = []
    pasadas = []
    error = None

    # Clave API de Unsplash para circuitos
    UNSPLASH_API_KEY = os.environ.get('UNSPLASH_API_KEY')
    headers = None
    use_unsplash = True

    if not UNSPLASH_API_KEY:
        logger.error("No se encontró la clave API de Unsplash en las variables de entorno")
        error = "No se encontró la clave API de Unsplash. Usando imágenes de respaldo para circuitos."
        use_unsplash = False
    else:
        headers = {'Authorization': f'Client-ID {UNSPLASH_API_KEY}'}
        test_unsplash_url = "https://api.unsplash.com/search/photos?query=test&per_page=1"
        test_response = requests.get(test_unsplash_url, headers=headers)
        if test_response.status_code != 200:
            logger.error(f"Clave API de Unsplash inválida o error en la solicitud: {test_response.status_code} - {test_response.text}")
            error = f"Clave API de Unsplash inválida (Código: {test_response.status_code}). Usando imágenes de respaldo para circuitos."
            use_unsplash = False

    if response.status_code == 200:
        try:
            data = response.json()
            races = data['MRData']['RaceTable']['Races']
            for race in races:
                fecha_str = race['date'] + "T" + race.get('time', '00:00:00Z')
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                ahora = datetime.now(timezone.utc)

                circuit_name = race['Circuit']['circuitName']
                circuit_image = 'https://via.placeholder.com/800x600?text=No+Image+Available'

                # Buscar imagen del circuito en Unsplash si la clave es válida
                if use_unsplash:
                    unsplash_url = f"https://api.unsplash.com/search/photos?query={circuit_name}+Formula+1&per_page=1&orientation=landscape"
                    unsplash_response = requests.get(unsplash_url, headers=headers)
                    if unsplash_response.status_code == 200:
                        unsplash_data = unsplash_response.json()
                        if unsplash_data.get('results'):
                            circuit_image = unsplash_data['results'][0]['urls']['regular']
                            logger.info(f"Imagen encontrada para {circuit_name}: {circuit_image}")
                        else:
                            logger.warning(f"No se encontraron imágenes en Unsplash para {circuit_name}. Response: {unsplash_data}")
                            circuit_image = 'https://via.placeholder.com/800x600?text=No+Image+Available'
                    else:
                        logger.error(f"Error en la solicitud a Unsplash para {circuit_name}: {unsplash_response.status_code} - {unsplash_response.text}")
                        circuit_image = 'https://via.placeholder.com/800x600?text=API+Error'

                carrera = {
                    'nombre': race['raceName'],
                    'lugar': race['Circuit']['Location']['locality'] + ", " + race['Circuit']['Location']['country'],
                    'fecha_inicio': fecha_obj,
                    'estado': '',
                    'descripcion': f"{circuit_name} - {race['Circuit']['Location']['country']}",
                    'circuit_image': circuit_image,
                    'winner': None,
                    'winner_image': None,
                }

                # Fetch winner for past races
                if fecha_obj < ahora or season != '2025':
                    result_url = f"https://api.jolpi.ca/ergast/f1/{season}/{race['round']}/results"
                    result_response = requests.get(result_url)
                    if result_response.status_code == 200:
                        result_data = result_response.json()
                        results = result_data['MRData']['RaceTable']['Races']
                        if results and results[0]['Results']:
                            winner = results[0]['Results'][0]['Driver']
                            winner_name = f"{winner['givenName']} {winner['familyName']}"
                            carrera['winner'] = winner_name

                            # Intentar obtener imagen del piloto desde OpenF1 API
                            winner_image = 'https://via.placeholder.com/150x150?text=No+Winner+Image'
                            openf1_url = f"https://api.openf1.org/v1/drivers?driver_number={winner.get('driverId', '')}&session_key=latest"
                            openf1_response = requests.get(openf1_url)
                            if openf1_response.status_code == 200:
                                openf1_data = openf1_response.json()
                                if openf1_data and 'headshot_url' in openf1_data[0]:
                                    winner_image = openf1_data[0]['headshot_url']
                                    logger.info(f"Imagen encontrada para {winner_name} en OpenF1: {winner_image}")
                                else:
                                    logger.warning(f"No se encontró imagen en OpenF1 para {winner_name}. Respuesta: {openf1_data}")
                            else:
                                logger.error(f"Error en la solicitud a OpenF1 para {winner_name}: {openf1_response.status_code} - {openf1_response.text}")

                            # Fallback a imagen local si OpenF1 no proporciona imagen
                            if winner_image == 'https://via.placeholder.com/150x150?text=No+Winner+Image' and winner_name in DRIVER_IMAGES:
                                winner_image = static(DRIVER_IMAGES[winner_name])
                                logger.info(f"Usando imagen local para {winner_name}: {winner_image}")

                            carrera['winner_image'] = winner_image
                    else:
                        carrera['winner'] = 'N/A'
                        carrera['winner_image'] = 'https://via.placeholder.com/150x150?text=No+Winner+Image'

                # Classify race
                if season == '2025' and abs((fecha_obj - ahora).total_seconds()) < 3600 * 3:
                    carrera['estado'] = 'En curso'
                    actuales.append(carrera)
                elif season == '2025' and fecha_obj > ahora:
                    carrera['estado'] = 'Próxima'
                    futuras.append(carrera)
                else:
                    carrera['estado'] = 'Finalizada'
                    pasadas.append(carrera)

            # Sort past races in descending order
            pasadas.sort(key=lambda x: x['fecha_inicio'], reverse=True)

        except (KeyError, IndexError) as e:
            logger.error(f"Error procesando datos de la API: {str(e)}")
            error = f"Error procesando datos de la API: {str(e)}"
    else:
        logger.error(f"Error al obtener datos de la API: Código {response.status_code}")
        error = f"Error al obtener datos de la API: Código {response.status_code}"

    context = {
        'actuales': actuales,
        'futuras': futuras,
        'pasadas': pasadas,
        'error': error,
        'season': int(season)
    }
    return render(request, 'carreras.html', {'carreras': context})

def pilotos(request):
    return render(request, 'pilots.html')

def lista_escuderias(request):
    escuderias = Escuderia.objects.all()
    return render(request, 'escuderias/lista.html', {'escuderias': escuderias})