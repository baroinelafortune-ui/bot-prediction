from .elo_model import EloModel
from .poisson_model import PoissonModel
from typing import Dict

class HybridFootballModel:
    """
    Modèle hybride combinant Elo Rating et Poisson/Dixon-Coles.
    """
    def __init__(self, k_factor: int = 30):
        self.elo = EloModel(k_factor=k_factor)
        self.poisson = PoissonModel()

    def train(self, historical_matches: list):
        """Entraîne les deux modèles sur les données historiques."""
        self.elo.process_match_history(historical_matches)
        self.poisson.fit(historical_matches)

    def predict(self, home_id: int, away_id: int) -> Dict:
        """
        Génère une prédiction hybride.
        On utilise Elo pour ajuster les espérances de buts (lambda/mu) de Poisson.
        """
        # Prédiction Poisson de base
        p_probs = self.poisson.predict_probabilities(home_id, away_id)
        
        # Ajustement Elo
        rating_h = self.elo.get_rating(home_id)
        rating_a = self.elo.get_rating(away_id)
        elo_expected_h = self.elo.calculate_expected_score(rating_h, rating_a)
        
        # Pondération hybride (exemple simple: moyenne pondérée des probabilités 1X2)
        # On peut aussi ajuster les xG de Poisson en fonction de la différence Elo
        elo_prob_home = elo_expected_h * 0.9  # Ajustement arbitraire pour le nul
        elo_prob_draw = 0.25 # Simplification
        elo_prob_away = 1.0 - elo_prob_home - elo_prob_draw
        
        # Fusion des probabilités (50/50 pour l'exemple)
        hybrid_home = (p_probs['home'] + elo_prob_home) / 2
        hybrid_draw = (p_probs['draw'] + elo_prob_draw) / 2
        hybrid_away = (p_probs['away'] + elo_prob_away) / 2
        
        # Normalisation
        total = hybrid_home + hybrid_draw + hybrid_away
        
        return {
            'probabilities': {
                'home': hybrid_home / total,
                'draw': hybrid_draw / total,
                'away': hybrid_away / total,
                'over_25': p_probs['over_25'],
                'under_25': p_probs['under_25'],
                'btts': p_probs['btts']
            },
            'expected_goals': {
                'home': p_probs['expected_goals_home'],
                'away': p_probs['expected_goals_away']
            },
            'top_scores': p_probs['top_scores'],
            'elo_ratings': {
                'home': rating_h,
                'away': rating_a
            }
        }
