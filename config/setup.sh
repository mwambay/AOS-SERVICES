#!/bin/bash
# Ce script installe les dépendances nécessaires et démarre le service principal.
# Assurez-vous que ce script est exécuté dans le bon répertoire
# et que vous avez les permissions nécessaires.
# Usage : ./setup.sh
echo "Installation des dépendances..."
pip install -r requirements.txt

echo "Création de la base de données..."
python -c "from src.app import db; db.create_all()"

echo "Démarrage du service principal..."
python src/app.py
echo "Demarrage du service de cotes"
python src/service_cotes.py