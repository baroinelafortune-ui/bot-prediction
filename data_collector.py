import os
import json
import pandas as pd
from datetime import datetime
from .football_api import FootballAPI

class DataCollector:
    """
    Orchestrateur pour la collecte et le stockage des données.
    """
    # IDs des ligues prioritaires (API Football v3)
    PRIORITY_LEAGUES = {
        'Premier League': 39,
        'La Liga': 140,
        'Serie A': 135,
        'Bundesliga': 78,
        'Ligue 1': 61
    }

    def __init__(self, api_key: str, data_dir: str = "data"):
        self.api = FootballAPI(api_key)
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def collect_historical_data(self, seasons: list):
        """
        Collecte les données historiques pour les ligues prioritaires.
        """
        for league_name, league_id in self.PRIORITY_LEAGUES.items():
            for season in seasons:
                print(f"Collecte des données pour {league_name} (Saison {season})...")
                fixtures = self.api.get_fixtures(league=league_id, season=season)
                
                if fixtures:
                    file_path = os.path.join(self.data_dir, f"fixtures_{league_id}_{season}.json")
                    with open(file_path, 'w') as f:
                        json.dump(fixtures, f)
                    print(f"Sauvegardé: {file_path}")
                else:
                    print(f"Aucune donnée pour {league_name} {season}")

    def collect_upcoming_fixtures(self):
        """
        Collecte les matchs à venir pour les prochains jours.
        """
        current_year = datetime.now().year
        for league_name, league_id in self.PRIORITY_LEAGUES.items():
            print(f"Collecte des matchs à venir pour {league_name}...")
            # On cherche les matchs à venir (next 10 par exemple)
            fixtures = self.api.get_fixtures(league=league_id, season=current_year, next=10)
            
            if fixtures:
                file_path = os.path.join(self.data_dir, f"upcoming_{league_id}.json")
                with open(file_path, 'w') as f:
                    json.dump(fixtures, f)
                print(f"Sauvegardé: {file_path}")

    def collect_odds(self, league_id: int, season: int):
        """
        Collecte les cotes pour une ligue et saison donnée.
        """
        print(f"Collecte des cotes pour la ligue {league_id}...")
        odds = self.api.get_odds(league=league_id, season=season)
        if odds:
            file_path = os.path.join(self.data_dir, f"odds_{league_id}_{season}.json")
            with open(file_path, 'w') as f:
                json.dump(odds, f)
            print(f"Sauvegardé: {file_path}")
