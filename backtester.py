import numpy as np
from typing import List, Dict

class Backtester:
    """
    Module pour évaluer les performances passées du système.
    """
    def __init__(self):
        self.results = []

    def add_prediction_result(self, prediction: Dict, actual_outcome: str, won: bool, profit: float):
        """
        Enregistre le résultat d'une prédiction.
        """
        self.results.append({
            'prediction': prediction,
            'actual_outcome': actual_outcome,
            'won': won,
            'profit': profit,
            'brier_score': self.calculate_brier_score(prediction['model_prob'], won),
            'log_loss': self.calculate_log_loss(prediction['model_prob'], won)
        })

    def calculate_brier_score(self, prob: float, won: bool) -> float:
        """Calcule le Brier Score pour une prédiction binaire."""
        y = 1.0 if won else 0.0
        return (prob - y) ** 2

    def calculate_log_loss(self, prob: float, won: bool) -> float:
        """Calcule la Log Loss pour une prédiction binaire."""
        y = 1.0 if won else 0.0
        eps = 1e-15
        p = np.clip(prob, eps, 1 - eps)
        return -(y * np.log(p) + (1 - y) * np.log(1 - p))

    def get_metrics(self) -> Dict:
        """
        Calcule les métriques globales de performance.
        """
        if not self.results:
            return {}

        total_bets = len(self.results)
        wins = sum(1 for r in self.results if r['won'])
        total_profit = sum(r['profit'] for r in self.results)
        total_staked = total_bets # On assume une mise de 1 unité par pari
        
        roi = (total_profit / total_staked) * 100 if total_staked > 0 else 0
        accuracy = (wins / total_bets) * 100 if total_bets > 0 else 0
        avg_brier = np.mean([r['brier_score'] for r in self.results])
        avg_log_loss = np.mean([r['log_loss'] for r in self.results])

        return {
            'total_bets': total_bets,
            'wins': wins,
            'accuracy': accuracy,
            'total_profit': total_profit,
            'roi': roi,
            'yield': roi, # Dans ce cas simple ROI = Yield
            'avg_brier_score': avg_brier,
            'avg_log_loss': avg_log_loss
        }

    def analyze_performance(self) -> str:
        """Analyse les performances et propose des améliorations."""
        metrics = self.get_metrics()
        if not metrics:
            return "Pas assez de données pour l'analyse."

        report = f"--- Rapport de Performance ---\n"
        report += f"Total Paris: {metrics['total_bets']}\n"
        report += f"Précision: {metrics['accuracy']:.2f}%\n"
        report += f"ROI: {metrics['roi']:.2f}%\n"
        report += f"Brier Score: {metrics['avg_brier_score']:.4f}\n"

        if metrics['roi'] < 0:
            report += "\nAnalyse: Le modèle sous-performe. Suggestions:\n"
            report += "- Augmenter le seuil d'Edge (actuellement 5%).\n"
            report += "- Vérifier la pondération temporelle (Time Decay).\n"
            report += "- Intégrer des données plus récentes ou des variables supplémentaires (xG, blessures).\n"
        else:
            report += "\nAnalyse: Le modèle génère un profit. Continuez à surveiller la variance.\n"

        return report
