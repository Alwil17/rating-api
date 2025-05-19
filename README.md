# 📌 FastAPI Rating System

Ce projet est une API REST développée avec **FastAPI** permettant la gestion des utilisateurs, des items et des évaluations (ratings). Il suit une architecture modulaire et repose sur SQLAlchemy pour la gestion des données.

---

## 📂 Structure du projet
```
app/
├── api/                 # Routeurs FastAPI et logique d'authentification
│   ├── endpoints/       # Endpoints REST (users, items, ratings, categories, tags)
│   ├── main.py          # Point d'entrée principal de l'API
│   ├── auth.py          # Authentification et sécurité
│   └── security.py      # Dépendances et outils de sécurité
│
├── application/
│   ├── schemas/         # DTOs et modèles de réponse Pydantic
│   ├── services/        # Logique métier (services)
│
├── domain/              # Modèles SQLAlchemy (User, Item, Rating, etc.)
│
├── infrastructure/
│   ├── database.py      # Configuration de la base de données et session
│   ├── repositories/    # Accès aux données (repositories)
│   └── seeders/         # Scripts de seed pour les catégories/items
│
📁 resources/           # Contient les diagrammes UML
│   ├── schema.puml         # Schéma de la base de données (PlantUML)
│   ├── schema.png          # Version image du schéma de la BD
│   ├── sequence.puml       # Diagramme de séquence (PlantUML)
│   ├── sequence.png        # Version image du diagramme de séquence
│
├── requirements.txt        # Dépendances du projet
├── README.md               # Documentation du projet
```

---

## 🛠️ Installation et Exécution

### 1️⃣ Prérequis

- Python 3.8+
- (Optionnel) PostgreSQL si vous ne souhaitez pas utiliser SQLite

### 2️⃣ Installation des dépendances

```bash
python -m venv venv
# Sur Mac/Linux
source venv/bin/activate
# Sur Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3️⃣ Configuration

Créez un fichier `.env` à la racine du projet (en vous basant sur le fichier `.env.example`) pour surcharger les variables de configuration si besoin (voir `app/config.py` pour les variables disponibles).

Exemple :
```
APP_DEBUG=True
DB_ENGINE=sqlite
DB_NAME=ratings
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
SENTRY_DSN=
```

### 4️⃣ Initialisation de la base de données

Au premier lancement, la base de données sera automatiquement créée et seedée avec des catégories et items de base si `APP_DEBUG=True`.

### 5️⃣ Lancer l'application

```bash
uvicorn app.api.main:app --reload --host 0.0.0.0
```

L'API sera accessible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📖 Documentation interactive

- Swagger UI : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Les endpoints sont organisés en groupes :
- **Users** → `/users/...`
- **Items** → `/items/...`
- **Ratings** → `/ratings/...`
- **Categories** → `/categories/...`
- **Tags** → `/tags/...`
- **Auth** → `/auth/...`

---

## 🔐 Authentification

L'API utilise OAuth2 avec Bearer token.  
Pour tester les endpoints protégés :
1. Créez un utilisateur via `/auth/register`
2. Récupérez un token via `/auth/token`
3. Ajoutez le header `Authorization: Bearer <token>` à vos requêtes

---

## 🧪 Tests

Pour lancer les tests unitaires et d'intégration :

```bash
pytest
```

---

## 🐳 Docker

Pour builder et lancer l'application avec Docker :

```bash
docker build -t rating_api .
docker run -p 8000:8000 rating_api
```

Un workflow GitHub Actions est fourni pour CI/CD et le push automatique sur Docker Hub.

---

## 📊 Diagrammes UML

- **Schéma de la base de données** :  
  ![DB Schema](resources/schema.png)
- **Diagramme de séquence** :  
  ![Diagramme de séquence](resources/sequence.png)

---

## 🛠 Technologies utilisées

- **FastAPI** : Framework web rapide pour Python
- **SQLAlchemy** : ORM pour la gestion des bases de données
- **PostgreSQL** ou **SQLite** : Base de données relationnelle
- **Uvicorn** : Serveur ASGI performant
- **PlantUML** : Génération de diagrammes UML
- **Pytest** : Tests unitaires
- **Docker** : Conteneurisation
- **Sentry** : Monitoring des erreurs (optionnel)
- **Prometheus** : Monitoring des métriques (optionnel)

---

## 🚀 Améliorations futures

- 🔹 Authentification OAuth2 avancée
- 🔹 WebSockets pour les mises à jour en temps réel
- 🔹 Permissions et rôles avancés
- 🔹 Recommandations personnalisées

---

## 📩 Contact

Pour toute question ou contribution, ouvrez une issue ou une pull request sur le dépôt GitHub.  
Merci d'utiliser et d'améliorer ce projet ! 😃