import requests
from datetime import datetime, timezone

OPENF1_API_URL = "https://api.openf1.org/v1/sessions"

def fetch_all_races():
    try:
        response = requests.get(OPENF1_API_URL, timeout=10)
        response.raise_for_status()
        sessions = response.json()
        races = []
        for s in sessions:
            if s.get("session_type") not in ["Race", "Sprint"]:
                continue
            # Parse dates, skip if missing
            date_start = s.get("date_start")
            date_end = s.get("date_end")
            if not date_start or not date_end:
                continue
            try:
                fecha_inicio = datetime.fromisoformat(date_start)
                fecha_fin = datetime.fromisoformat(date_end)
            except Exception:
                continue
            races.append({
                "nombre": s.get("session_name", "Carrera"),
                "lugar": s.get("location", "Lugar no disponible"),
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "descripcion": f"{s.get('country_name', '')} - {s.get('circuit_short_name', '')}",
            })
        return races
    except requests.RequestException as e:
        print(f"Error fetching OpenF1 API data: {e}")
        return []