# Système de Prédiction de Football Automatisé

## Table des Matières

1.  [Introduction](#1-introduction)
2.  [Fonctionnalités](#2-fonctionnalités)
3.  [Architecture du Projet](#3-architecture-du-projet)
4.  [Installation](#4-installation)
5.  [Configuration](#5-configuration)
6.  [Utilisation](#6-utilisation)
7.  [Livrables](#7-livrables)
8.  [Technologies Utilisées](#8-technologies-utilisées)

## 1. Introduction

Ce projet vise à construire un système automatisé et professionnel de prédiction de matchs de football. Il intègre des modèles de modélisation avancés, une détection de value bets, un module de backtesting, une gestion de base de données et la génération de rapports quotidiens. L'objectif est de fournir des probabilités fiables et d'identifier des opportunités de paris à valeur ajoutée.

## 2. Fonctionnalités

Le système offre les fonctionnalités suivantes :

*   **Collecte de Données Automatisée :** Récupération des données historiques et en temps réel via l'API Football (matchs, équipes, statistiques, cotes).
*   **Modélisation Hybride :** Utilisation combinée des modèles Elo Rating, Poisson et Dixon-Coles pour des prédictions robustes.
*   **Détection de Value Bets :** Identification des paris où la probabilité du modèle est significativement supérieure à la probabilité implicite des bookmakers (Edge ≥ 5%).
*   **Calculs de Probabilités :** Génération de probabilités pour 1X2, Over/Under 2.5, BTTS et les scores exacts les plus probables.
*   **Backtesting et Analyse de Performance :** Évaluation continue des performances du modèle avec des métriques clés (ROI, Yield, Accuracy, Brier Score, Log Loss).
*   **Base de Données Intégrée :** Stockage structuré des données brutes, des prédictions et des résultats dans une base de données SQLite.
*   **Rapports Quotidiens :** Génération automatique de rapports présentant les meilleurs value bets et un résumé des performances.
*   **Automatisation Complète :** Mise à jour quotidienne des données, recalcul des modèles et génération de rapports.

## 3. Architecture du Projet

La structure des répertoires est conçue pour la modularité et la maintenabilité :

```
football_prediction_system/
├── data/                 # Données brutes et traitées (matchs, équipes, joueurs, cotes)
├── models/               # Modèles de prédiction entraînés et scripts de modélisation
├── src/                  # Code source de l'application
│   ├── api/              # Modules pour l'interaction avec les APIs externes
│   ├── core/             # Logique métier principale (calculs, prédictions)
│   ├── db/               # Gestion de la base de données
│   ├── backtesting/      # Modules pour le backtesting et l'analyse de performance
│   └── reports/          # Génération des rapports quotidiens
├── reports/              # Rapports générés (quotidiens, performance)
├── tests/                # Tests unitaires et d'intégration
├── config/               # Fichiers de configuration (API keys, paramètres de modèle)
├── architecture.md       # Document d'architecture détaillé
├── README.md             # Ce document
└── requirements.txt      # Dépendances Python
```

## 4. Installation

Suivez ces étapes pour installer et configurer le système :

1.  **Cloner le dépôt :**
    ```bash
    git clone <URL_DU_DEPOT>
    cd football_prediction_system
    ```

2.  **Créer un environnement virtuel (recommandé) :**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur Windows: .\venv\Scripts\activate
    ```

3.  **Installer les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    ```

## 5. Configuration

Le système nécessite une clé API pour l'API Football. Vous pouvez l'obtenir sur [api-sports.io](https://api-sports.io/).

*   **Via variable d'environnement :**
    Définissez la variable d'environnement `FOOTBALL_API_KEY` avec votre clé API :
    ```bash
    export FOOTBALL_API_KEY="VOTRE_CLE_API_FOOTBALL"
    ```
    (Pour une persistance, ajoutez cette ligne à votre `~/.bashrc` ou `~/.zshrc`)

*   **Via argument de ligne de commande :**
    Vous pouvez passer la clé directement lors de l'exécution du script principal :
    ```bash
    python main.py --api_key "VOTRE_CLE_API_FOOTBALL"
    ```

## 6. Utilisation

Pour exécuter le système, utilisez le script `main.py` :

```bash
python main.py
```

Le script effectuera les opérations suivantes (les étapes de collecte et d'entraînement sont commentées par défaut pour éviter des appels API excessifs lors des premiers tests) :

1.  Initialisation des modules (Base de données, Collecteur, Modèle, Value Betting).
2.  Collecte des données historiques et à venir (décommenter et adapter `main.py` pour activer).
3.  Entraînement des modèles de prédiction.
4.  Génération des prédictions pour les matchs à venir.
5.  Détection des value bets.
6.  Génération d'un rapport quotidien dans le dossier `reports/`.

### Automatisation Quotidienne

Pour automatiser l'exécution quotidienne, vous pouvez utiliser `cron` (sur Linux/macOS) ou le Planificateur de Tâches (sur Windows).

Exemple `cron` (pour une exécution chaque jour à 03h00 du matin) :

```bash
0 3 * * * /usr/bin/python3 /path/to/your/football_prediction_system/main.py --api_key "VOTRE_CLE_API_FOOTBALL" >> /path/to/your/football_prediction_system/logs/daily_run.log 2>&1
```

Assurez-vous que le chemin vers `python3` et le répertoire du projet sont corrects.

## 7. Livrables

*   **Code complet :** L'ensemble du code source Python est fourni dans le répertoire `src/`.
*   **Architecture du projet :** Décrite dans `architecture.md` et reflétée par la structure des répertoires.
*   **Script d'exécution automatique :** `main.py` sert de point d'entrée pour l'exécution et l'automatisation.
*   **Connexion API fonctionnelle :** Le module `src/api/football_api.py` gère l'interaction avec l'API Football.
*   **Base de données opérationnelle :** Une base de données SQLite (`data/football.db`) est créée et gérée par `src/db/database.py`.
*   **Système de backtesting :** Le module `src/backtesting/backtester.py` permet d'évaluer les performances.
*   **Documentation claire d'installation :** Ce fichier `README.md`.

## 8. Technologies Utilisées

*   **Langage de Programmation :** Python 3.x
*   **Librairies Python :**
    *   `requests` : Pour les requêtes HTTP vers les APIs.
    *   `numpy` : Pour les opérations numériques.
    *   `scipy` : Pour les fonctions statistiques (e.g., `poisson.pmf`).
    *   `pandas` : Pour la manipulation et l'analyse de données (potentiellement pour les rapports).
    *   `sqlite3` : Module intégré pour la gestion de la base de données SQLite.
*   **Base de Données :** SQLite

---

**Auteur :** Manus AI
**Date :** 22 Juin 2026
