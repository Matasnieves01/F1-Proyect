import requests
from datetime import datetime, timezone

ERGAST_API_URL = "https://ergast.com/api/f1/current.json"

def fetch_ergast_races():
    try:
        response = requests.get(ERGAST_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        races = data['MRData']['RaceTable']['Races']
        formatted_races = []

        for race in races:
            fecha_str = race['date'] + "T" + race.get('time', '00:00:00Z')
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

            formatted_races.append({
                'nombre': race['raceName'],
                'lugar': f"{race['Circuit']['Location']['locality']}, {race['Circuit']['Location']['country']}",
                'fecha_inicio': fecha_obj,
                'descripcion': f"{race['Circuit']['circuitName']} - {race['Circuit']['Location']['country']}",
            })

        return formatted_races
    except requests.RequestException as e:
        print(f"Error fetching Ergast API data: {e}")
        return []