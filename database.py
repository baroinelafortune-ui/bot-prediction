import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

class DatabaseManager:
    """
    Gère la persistance des données dans SQLite.
    """
    def __init__(self, db_path: str = "data/football.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialise les tables de la base de données."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Table des équipes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    country TEXT
                )
            ''')
            
            # Table des matchs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY,
                    league_id INTEGER,
                    season INTEGER,
                    date TEXT,
                    home_team_id INTEGER,
                    away_team_id INTEGER,
                    home_goals INTEGER,
                    away_goals INTEGER,
                    status TEXT,
                    FOREIGN KEY (home_team_id) REFERENCES teams(id),
                    FOREIGN KEY (away_team_id) REFERENCES teams(id)
                )
            ''')
            
            # Table des cotes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS odds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    match_id INTEGER,
                    bookmaker TEXT,
                    market TEXT,
                    outcome TEXT,
                    odd REAL,
                    timestamp TEXT,
                    FOREIGN KEY (match_id) REFERENCES matches(id)
                )
            ''')
            
            # Table des prédictions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    match_id INTEGER,
                    model_version TEXT,
                    prob_home REAL,
                    prob_draw REAL,
                    prob_away REAL,
                    prob_over25 REAL,
                    prob_under25 REAL,
                    prob_btts REAL,
                    timestamp TEXT,
                    FOREIGN KEY (match_id) REFERENCES matches(id)
                )
            ''')

            # Table des métriques de performance
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    roi REAL,
                    yield REAL,
                    accuracy REAL,
                    brier_score REAL,
                    log_loss REAL
                )
            ''')
            
            conn.commit()

    def save_teams(self, teams: List[Dict]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for team in teams:
                cursor.execute('INSERT OR REPLACE INTO teams (id, name, country) VALUES (?, ?, ?)',
                             (team['id'], team['name'], team.get('country')))
            conn.commit()

    def save_matches(self, matches: List[Dict]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for m in matches:
                cursor.execute('''
                    INSERT OR REPLACE INTO matches 
                    (id, league_id, season, date, home_team_id, away_team_id, home_goals, away_goals, status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    m['fixture']['id'],
                    m['league']['id'],
                    m['league']['season'],
                    m['fixture']['date'],
                    m['teams']['home']['id'],
                    m['teams']['away']['id'],
                    m['goals'].get('home'),
                    m['goals'].get('away'),
                    m['fixture']['status']['short']
                ))
            conn.commit()

    def save_prediction(self, match_id: int, probs: Dict):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO predictions 
                (match_id, model_version, prob_home, prob_draw, prob_away, prob_over25, prob_under25, prob_btts, timestamp) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                match_id,
                "v1.0-hybrid",
                probs['home'],
                probs['draw'],
                probs['away'],
                probs['over_25'],
                probs['under_25'],
                probs['btts'],
                datetime.now().isoformat()
            ))
            conn.commit()
