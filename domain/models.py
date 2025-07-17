from dataclasses import dataclass

@dataclass
class Piloto:
    name: str
    championships_won: int
    current_season_points: float
    team: str