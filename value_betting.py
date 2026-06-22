from typing import Dict, List, Optional

class ValueBettingModule:
    """
    Module pour détecter les value bets en comparant les probabilités du modèle aux cotes.
    """
    def __init__(self, min_edge: float = 0.05):
        self.min_edge = min_edge

    def calculate_edge(self, model_prob: float, bookmaker_odds: float) -> float:
        """
        Calcule l'edge (avantage) par rapport au bookmaker.
        Formule: Edge = P_modele - (1 / cote)
        """
        if bookmaker_odds <= 0:
            return 0.0
        implied_prob = 1.0 / bookmaker_odds
        return model_prob - implied_prob

    def detect_value_bets(self, predictions: Dict, odds: Dict) -> List[Dict]:
        """
        Identifie les paris de valeur pour un match donné.
        """
        value_bets = []
        
        # Marché 1X2
        if '1X2' in odds:
            markets = {
                'home': odds['1X2'].get('home'),
                'draw': odds['1X2'].get('draw'),
                'away': odds['1X2'].get('away')
            }
            for outcome, odd in markets.items():
                if odd:
                    prob = predictions['probabilities'][outcome]
                    edge = self.calculate_edge(prob, odd)
                    if edge >= self.min_edge:
                        value_bets.append({
                            'market': '1X2',
                            'outcome': outcome,
                            'odd': odd,
                            'model_prob': prob,
                            'implied_prob': 1.0 / odd,
                            'edge': edge,
                            'confidence': self.calculate_confidence(edge, prob)
                        })

        # Marché Over/Under 2.5
        if 'OU25' in odds:
            ou_markets = {
                'over_25': odds['OU25'].get('over'),
                'under_25': odds['OU25'].get('under')
            }
            for outcome, odd in ou_markets.items():
                if odd:
                    prob = predictions['probabilities'][outcome]
                    edge = self.calculate_edge(prob, odd)
                    if edge >= self.min_edge:
                        value_bets.append({
                            'market': 'Over/Under 2.5',
                            'outcome': outcome,
                            'odd': odd,
                            'model_prob': prob,
                            'implied_prob': 1.0 / odd,
                            'edge': edge,
                            'confidence': self.calculate_confidence(edge, prob)
                        })

        return value_bets

    def calculate_confidence(self, edge: float, prob: float) -> float:
        """
        Calcule un niveau de confiance de 0 à 10.
        Basé sur l'edge et la probabilité absolue.
        """
        # Formule simple pour l'exemple
        confidence = (edge * 100) * (prob * 2)
        return min(max(confidence, 0), 10)
