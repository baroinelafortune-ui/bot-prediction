import requests
import json
import os
from typing import Dict, List, Optional

class FootballAPI:
    """
    Client pour l'API Football (api-football.com / api-sports.io).
    """
    BASE_URL = "https://v3.football.api-sports.io/"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'x-apisports-key': self.api_key
        }

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Effectue une requête GET vers l'API.
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('errors'):
                print(f"Erreurs API: {data['errors']}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête API: {e}")
            return {}

    def get_status(self) -> Dict:
        """Vérifie le statut de l'abonnement et les limites de requêtes."""
        return self._get("status")

    def get_leagues(self, id: Optional[int] = None, name: Optional[str] = None, country: Optional[str] = None) -> List[Dict]:
        """Récupère les informations sur les ligues."""
        params = {}
        if id: params['id'] = id
        if name: params['name'] = name
        if country: params['country'] = country
        
        data = self._get("leagues", params=params)
        return data.get('response', [])

    def get_fixtures(self, league: int, season: int, date: Optional[str] = None, last: Optional[int] = None, next: Optional[int] = None) -> List[Dict]:
        """Récupère les matchs (passés ou à venir)."""
        params = {'league': league, 'season': season}
        if date: params['date'] = date
        if last: params['last'] = last
        if next: params['next'] = next
        
        data = self._get("fixtures", params=params)
        return data.get('response', [])

    def get_fixture_statistics(self, fixture_id: int) -> List[Dict]:
        """Récupère les statistiques d'un match spécifique."""
        params = {'fixture': fixture_id}
        data = self._get("fixtures/statistics", params=params)
        return data.get('response', [])

    def get_odds(self, fixture: Optional[int] = None, league: Optional[int] = None, season: Optional[int] = None, date: Optional[str] = None) -> List[Dict]:
        """Récupère les cotes des bookmakers."""
        params = {}
        if fixture: params['fixture'] = fixture
        if league: params['league'] = league
        if season: params['season'] = season
        if date: params['date'] = date
        
        data = self._get("odds", params=params)
        return data.get('response', [])

    def get_predictions(self, fixture_id: int) -> List[Dict]:
        """Récupère les prédictions de l'API (pour comparaison ou xG)."""
        params = {'fixture': fixture_id}
        data = self._get("predictions", params=params)
        return data.get('response', [])

    def get_injuries(self, fixture: Optional[int] = None, league: Optional[int] = None, season: Optional[int] = None, date: Optional[str] = None) -> List[Dict]:
        """Récupère les blessures et suspensions."""
        params = {}
        if fixture: params['fixture'] = fixture
        if league: params['league'] = league
        if season: params['season'] = season
        if date: params['date'] = date
        
        data = self._get("injuries", params=params)
        return data.get('response', [])
