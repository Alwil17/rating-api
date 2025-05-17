# Utilise une image officielle Python
FROM python:3.10

# Crée un dossier pour l'application
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code source dans le conteneur
COPY . .

# Expose le port 8000 (par défaut pour Uvicorn)
EXPOSE 8000

# Commande pour lancer l'app
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
