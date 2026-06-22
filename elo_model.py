import math

class EloModel:
    """
    Modèle de classement Elo pour évaluer la force relative des équipes.
    """
    def __init__(self, k_factor: int = 30, initial_rating: float = 1500.0):
        self.k_factor = k_factor
        self.initial_rating = initial_rating
        self.ratings = {}

    def get_rating(self, team_id: int) -> float:
        return self.ratings.get(team_id, self.initial_rating)

    def calculate_expected_score(self, rating_a: float, rating_b: float) -> float:
        """Calcule le score attendu (probabilité de victoire/nul)."""
        return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400.0))

    def update_ratings(self, team_a_id: int, team_b_id: int, score_a: int, score_b: int):
        """Met à jour les classements après un match."""
        rating_a = self.get_rating(team_a_id)
        rating_b = self.get_rating(team_b_id)

        expected_a = self.calculate_expected_score(rating_a, rating_b)
        expected_b = 1.0 - expected_a

        # Résultat réel (1 pour victoire, 0.5 pour nul, 0 pour défaite)
        if score_a > score_b:
            actual_a, actual_b = 1.0, 0.0
        elif score_a < score_b:
            actual_a, actual_b = 0.0, 1.0
        else:
            actual_a, actual_b = 0.5, 0.5

        # Mise à jour avec le facteur K
        # On peut ajuster K en fonction de la différence de buts (optionnel)
        margin_multiplier = 1.0
        diff = abs(score_a - score_b)
        if diff > 1:
            margin_multiplier = 1.0 + math.log(diff)

        self.ratings[team_a_id] = rating_a + self.k_factor * margin_multiplier * (actual_a - expected_a)
        self.ratings[team_b_id] = rating_b + self.k_factor * margin_multiplier * (actual_b - expected_b)

    def process_match_history(self, matches: list):
        """Traite une liste de matchs pour initialiser/mettre à jour les classements."""
        # Trier les matchs par date pour respecter l'ordre chronologique
        sorted_matches = sorted(matches, key=lambda x: x['fixture']['timestamp'])
        
        for match in sorted_matches:
            if match['fixture']['status']['short'] == 'FT':
                team_a_id = match['teams']['home']['id']
                team_b_id = match['teams']['away']['id']
                score_a = match['goals']['home']
                score_b = match['goals']['away']
                self.update_ratings(team_a_id, team_b_id, score_a, score_b)
