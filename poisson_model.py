import numpy as np
from scipy.stats import poisson
from scipy.optimize import minimize
from typing import Dict, Tuple

class PoissonModel:
    """
    Modèle de Poisson pour l'estimation des buts et des probabilités de match.
    Inclut la correction de Dixon-Coles pour les scores faibles.
    """
    def __init__(self):
        self.team_stats = {}
        self.avg_home_goals = 0
        self.avg_away_goals = 0

    def fit(self, matches: list):
        """
        Calcule les forces d'attaque et de défense pour chaque équipe.
        """
        if not matches:
            return

        all_home_goals = [m['goals']['home'] for m in matches if m['goals']['home'] is not None]
        all_away_goals = [m['goals']['away'] for m in matches if m['goals']['away'] is not None]
        
        self.avg_home_goals = np.mean(all_home_goals)
        self.avg_away_goals = np.mean(all_away_goals)

        teams = {}
        for m in matches:
            home_id = m['teams']['home']['id']
            away_id = m['teams']['away']['id']
            
            if home_id not in teams: teams[home_id] = {'home_goals': [], 'away_goals_conceded': [], 'away_goals': [], 'home_goals_conceded': []}
            if away_id not in teams: teams[away_id] = {'home_goals': [], 'away_goals_conceded': [], 'away_goals': [], 'home_goals_conceded': []}
            
            if m['goals']['home'] is not None and m['goals']['away'] is not None:
                teams[home_id]['home_goals'].append(m['goals']['home'])
                teams[home_id]['home_goals_conceded'].append(m['goals']['away'])
                teams[away_id]['away_goals'].append(m['goals']['away'])
                teams[away_id]['away_goals_conceded'].append(m['goals']['home'])

        for team_id, data in teams.items():
            attack_home = np.mean(data['home_goals']) / self.avg_home_goals if data['home_goals'] else 1.0
            defense_home = np.mean(data['home_goals_conceded']) / self.avg_away_goals if data['home_goals_conceded'] else 1.0
            attack_away = np.mean(data['away_goals']) / self.avg_away_goals if data['away_goals'] else 1.0
            defense_away = np.mean(data['away_goals_conceded']) / self.avg_home_goals if data['away_goals_conceded'] else 1.0
            
            self.team_stats[team_id] = {
                'att_h': attack_home,
                'def_h': defense_home,
                'att_a': attack_away,
                'def_a': defense_away
            }

    def _dixon_coles_rho(self, x, y, lambda_x, mu_y, rho):
        """Fonction de correction de Dixon-Coles."""
        if x == 0 and y == 0:
            return 1 - lambda_x * mu_y * rho
        elif x == 0 and y == 1:
            return 1 + lambda_x * rho
        elif x == 1 and y == 0:
            return 1 + mu_y * rho
        elif x == 1 and y == 1:
            return 1 - rho
        return 1.0

    def predict_probabilities(self, home_id: int, away_id: int, max_goals: int = 8, rho: float = 0.0) -> Dict:
        """
        Prédit les probabilités 1X2, O/U 2.5, BTTS et Score Exact.
        """
        stats_h = self.team_stats.get(home_id, {'att_h': 1.0, 'def_h': 1.0})
        stats_a = self.team_stats.get(away_id, {'att_a': 1.0, 'def_a': 1.0})

        lambda_x = stats_h['att_h'] * stats_a['def_a'] * self.avg_home_goals
        mu_y = stats_a['att_a'] * stats_h['def_h'] * self.avg_away_goals

        matrix = np.zeros((max_goals + 1, max_goals + 1))
        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                prob = poisson.pmf(i, lambda_x) * poisson.pmf(j, mu_y)
                if rho != 0:
                    prob *= self._dixon_coles_rho(i, j, lambda_x, mu_y, rho)
                matrix[i, j] = prob

        # Normalisation
        matrix /= matrix.sum()

        prob_home = np.sum(np.tril(matrix, -1))
        prob_draw = np.sum(np.diag(matrix))
        prob_away = np.sum(np.triu(matrix, 1))

        # Over/Under 2.5
        prob_under_25 = matrix[0,0] + matrix[0,1] + matrix[0,2] + matrix[1,0] + matrix[1,1] + matrix[2,0]
        prob_over_25 = 1.0 - prob_under_25

        # BTTS
        prob_no_btts = np.sum(matrix[0, :]) + np.sum(matrix[:, 0]) - matrix[0,0]
        prob_btts = 1.0 - prob_no_btts

        # Top 3 scores exacts
        scores = []
        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                scores.append(((i, j), matrix[i, j]))
        top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:3]

        return {
            'home': prob_home,
            'draw': prob_draw,
            'away': prob_away,
            'over_25': prob_over_25,
            'under_25': prob_under_25,
            'btts': prob_btts,
            'top_scores': top_scores,
            'expected_goals_home': lambda_x,
            'expected_goals_away': mu_y
        }
