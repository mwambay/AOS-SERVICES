@echo off
REM Script de configuration pour Windows
REM Assurez-vous que Python et pip sont installés et ajoutés au PATH
REM Vérification de l'installation de Python

echo Installation des dépendances...
pip install -r requirements.txt

echo Creation de la base de donnees...
python -c "from src.app import db; db.create_all()"

echo Demarrage du service principal...
python src\app.py
echo Demarrage du service de cotes...
REM Le service de cotes doit être lancé après le service principal
python src\service_cotes.py