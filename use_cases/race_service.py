from infrastructure.fastf1_api import fetch_fastf1_races
from datetime import datetime, timezone
from infrastructure.ergast_api import fetch_ergast_races
from infrastructure.openf1_api import fetch_all_races

def categorize_races():
    now = datetime.now(timezone.utc)
    actuales, futuras, pasadas = [], [], []

    fastf1_races = fetch_fastf1_races()
    ergast_races = fetch_ergast_races()
    openf1_races = fetch_all_races()

    all_races = fastf1_races + ergast_races + openf1_races

    for r in all_races:
        try:
            fecha_inicio = r['fecha_inicio']
            carrera = {
                "nombre": r.get("nombre", "Carrera"),
                "lugar": r.get("lugar", "Lugar no disponible"),
                "fecha_inicio": fecha_inicio,
                "estado": "",
                "descripcion": r.get("descripcion", ""),
            }

            if fecha_inicio <= now:
                carrera["estado"] = "en curso" if (now - fecha_inicio).total_seconds() < 10800 else "finalizada"
                if carrera["estado"] == "en curso":
                    actuales.append(carrera)
                else:
                    pasadas.append(carrera)
            else:
                carrera["estado"] = "próxima"
                futuras.append(carrera)

        except Exception as e:
            print(f"Error processing race: {e}")
            continue

    print(f"Actuales: {len(actuales)}, Futuras: {len(futuras)}, Pasadas: {len(pasadas)}")
    return actuales, futuras, pasadas