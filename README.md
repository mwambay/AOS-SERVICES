# Système d'Inscription et de Gestion des Cotes Étudiants

Ce projet est composé de deux microservices Flask distincts conçus pour fonctionner ensemble :

1.  **Service d'Inscription (`registration_service.py`)** : Gère l'enregistrement des étudiants, le statut de leur paiement et la notification d'autres services.
2.  **Service de Gestion des Cotes (`grades_service.py`)** : Reçoit des informations sur les étudiants initialisés et permet d'ajouter et de consulter leurs notes (cotes).

L'objectif est de séparer les responsabilités : l'un gère l'identité et le statut administratif de l'étudiant, l'autre gère ses résultats académiques.

## Architecture Générale

*   **Service d'Inscription** : Point d'entrée principal pour les nouveaux étudiants. Il utilise une base de données **SQLite** pour stocker les informations de manière persistante.
*   **Service de Gestion des Cotes** : Service secondaire qui est informé de l'existence d'un étudiant par le service d'inscription. Il utilise un **dictionnaire en mémoire** pour stocker les notes, ce qui signifie que **les notes sont perdues à chaque redémarrage du service**.
*   **Communication** : Le service d'inscription peut envoyer une requête HTTP POST au service de gestion des cotes pour l'informer qu'un nouvel étudiant est prêt à recevoir des notes.

---

## 1. Service d'Inscription (`registration_service.py`)

### Description

Ce service Flask gère l'enregistrement des étudiants, la confirmation de leur paiement et peut notifier le service de gestion des cotes.

### Fonctionnalités Clés

*   Enregistrement de nouveaux étudiants (nom, email).
*   Mise à jour du statut de paiement d'un étudiant.
*   Envoi d'une notification au service de cotes pour initialiser un étudiant.
*   Utilise une base de données SQLite (`students.db`) pour la persistance des données des étudiants.

### Ports
    * Service d'inscription : `5000`
    * Service de gestion des cotes : `5001`

### Endpoints API

*   `POST /register` : Enregistre un nouvel étudiant.
    *   Corps : `{"name": "...", "email": "..."}`
    *   Réponse : `{"message": "...", "id": ...}`
*   `POST /pay/<student_id>` : Marque le paiement d'un étudiant comme effectué.
    *   Réponse : `{"message": "Paiement confirmé"}`
*   `POST /notify_grades/<student_id>` : Notifie le service de cotes.
    *   Réponse : `{"status": "...", "grades_response": ...}`
*   `GET /students` : Récupère la liste de tous les étudiants enregistrés.
    *   Réponse : `[{"id": ..., "name": "...", "email": "...", "paid": ...}]`
---

## 2. Service de Gestion des Cotes (`grades_service.py`)

### Description

Ce service Flask simple stocke et récupère les notes des étudiants. Il est conçu pour être initialisé par le service d'inscription.

### Fonctionnalités Clés

*   Initialisation d'un espace pour les notes d'un étudiant (via `POST /init_student`).
*   Ajout de notes pour un étudiant spécifique.
*   Consultation du nom et de la liste des notes d'un étudiant.
*   Utilise un **dictionnaire en mémoire** (`students_grades`). **Les données ne sont pas persistantes.**

### Endpoints API

*   `POST /init_student` : Crée une entrée pour un étudiant (généralement appelé par le service d'inscription).
    *   Corps : `{"id": ..., "name": "..."}`
    *   Réponse : `{"message": "Espace notes créé pour ..."}`
*   `POST /add_grade/<student_id>` : Ajoute une note à un étudiant.
    *   Corps : `{"grade": ...}`
    *   Réponse : `{"message": "Note ajoutée"}`
*   `GET /get_grades/<student_id>` : Récupère les informations et notes d'un étudiant.
    *   Réponse : `{"name": "...", "grades": [...]}`

