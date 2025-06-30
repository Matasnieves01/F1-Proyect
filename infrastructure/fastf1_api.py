import fastf1
from datetime import datetime, timezone

def fetch_fastf1_races(year=None):
    if year is None:
        year = datetime.now().year
    schedule = fastf1.get_event_schedule(year)
    races = []
    for _, row in schedule.iterrows():
        fecha_obj = row['Session1DateUtc'].replace(tzinfo=timezone.utc)
        races.append({
            'nombre': row['EventName'],
            'lugar': f"{row['Location']}, {row['Country']}",
            'fecha_inicio': fecha_obj,
            'descripcion': row['OfficialEventName'],
        })
    return races