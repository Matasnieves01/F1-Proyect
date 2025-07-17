# f1_teams/management/commands/import_teams.py
import requests
import logging
from django.core.management.base import BaseCommand
from core.models import Escuderia
from f1_teams.utils import TEAMS_METADATA

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Formula 1 teams from OpenF1 API and store in database"

    def handle(self, *args, **kwargs):
        api_url = "https://api.openf1.org/v1/drivers?session_key=latest"
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            drivers = response.json()

            # Extract unique team names
            team_names = set(driver["team_name"] for driver in drivers)
            logger.info(f"Found {len(team_names)} teams: {', '.join(team_names)}")

            # Update or create teams in database
            for team_name in team_names:
                metadata = TEAMS_METADATA.get(team_name, {
                    "pais": "Unknown",
                    "año_fundación": 0,
                    "campeonatos": 0,
                    "logo": "https://via.placeholder.com/150x150?text=No+Logo"
                })
                Escuderia.objects.update_or_create(
                    nombre=team_name,
                    defaults={
                        "pais": metadata["pais"],
                        "año_fundación": metadata["año_fundación"],
                        "campeonatos": metadata["campeonatos"],
                        "logo": metadata["logo"]
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Successfully imported/updated {len(team_names)} teams"))

        except requests.RequestException as e:
            logger.error(f"Error fetching data from OpenF1 API: {e}")
            self.stdout.write(self.style.ERROR(f"Error fetching data from API: {e}"))
            # Fallback to static metadata
            logger.info("Falling back to static metadata")
            for team_name, metadata in TEAMS_METADATA.items():
                Escuderia.objects.update_or_create(
                    nombre=team_name,
                    defaults={
                        "pais": metadata["pais"],
                        "año_fundación": metadata["año_fundación"],
                        "campeonatos": metadata["campeonatos"],
                        "logo": metadata["logo"]
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Successfully imported/updated {len(TEAMS_METADATA)} teams from static metadata"))