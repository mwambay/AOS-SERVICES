
# Service d'Inscription Étudiant (`registration_service.py`)

Ceci est une application Flask simple qui sert de service d'inscription pour des étudiants. Elle permet d'enregistrer de nouveaux étudiants, de marquer leur paiement comme effectué et de notifier un service externe (service de gestion des cotes).

## Fonctionnalités

*   **Enregistrement d'étudiants** : Ajoute de nouveaux étudiants à la base de données avec leur nom et email.
*   **Confirmation de Paiement** : Met à jour le statut d'un étudiant pour indiquer qu'il a payé.
*   **Notification Externe** : Envoie les informations d'un étudiant (ID, nom) à un service de gestion des cotes externe lorsque demandé.
*   **Base de Données** : Utilise une base de données SQLite (`students.db`) pour stocker les informations des étudiants.

## Prérequis

*   min Python 3.9
*   pip (gestionnaire de paquets Python)

## Installation

1.  Clonez le dépôt ou copiez le fichier `registration_service.py`.
2.  Installez les dépendances nécessaires :
    ```
    pip install -r requirements
    ```

## Lancement de l'application

1.  Placez-vous dans le répertoire contenant le fichier `registration_service.py`.
2.  Exécutez la commande suivante dans votre terminal :
    ```bash
    python registration_service.py
    ```
3.  Le service sera lancé et accessible à l'adresse `http://localhost:5000` (ou l'adresse IP de votre machine sur le port 5000). La base de données `students.db` sera créée automatiquement si elle n'existe pas.

## Endpoints de l'API

*   **`POST /register`**
    *   **Description** : Enregistre un nouvel étudiant.
    *   **Corps de la requête (JSON)** :
        ```json
        {
          "name": "Nom de l'étudiant",
          "email": "email@example.com"
        }
        ```
    *   **Réponse (Succès - 201)** :
        ```json
        {
          "message": "Etudiant enregistré avec succès",
          "id": <id_de_l_etudiant_cree>
        }
        ```

*   **`POST /pay/<student_id>`**
    *   **Description** : Marque le paiement d'un étudiant comme confirmé. Remplacez `<student_id>` par l'ID de l'étudiant concerné.
    *   **Réponse (Succès - 200)** :
        ```json
        {
          "message": "Paiement confirmé"
        }
        ```
    *   **Réponse (Erreur - 404)** : Si l'étudiant n'est pas trouvé.
        ```json
        {
          "error": "Etudiant non trouvé"
        }
        ```

*   **`POST /notify_grades/<student_id>`**
    *   **Description** : Notifie le service de gestion des cotes externe (`https://service-cotes-production.up.railway.app/init_student`) avec les informations de l'étudiant. Remplacez `<student_id>` par l'ID de l'étudiant.
    *   **Réponse (Succès - 200)** :
        ```json
        {
          "status": "notification envoyée",
          "grades_response": <reponse_du_service_cotes>
        }
        ```
    *   **Réponse (Erreur - 404)** : Si l'étudiant n'est pas trouvé.
        ```json
        {
          "error": "Etudiant non trouvé"
        }
        ```

    **`GET /students`**
        *   **Description** : recupere ous les etudiants *

## Base de Données

*   **Type** : SQLite
*   **Fichier** : `students.db` (créé automatiquement dans le même répertoire que le script).
*   **Table** : `student`
    *   `id` (Integer, Clé primaire)
    *   `name` (String, Non null)
    *   `email` (String, Unique, Non null)
    *   `has_paid` (Boolean, Défaut: False)
