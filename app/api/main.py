from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

# Importer la dépendance de la base de données
from app.api.endpoints import item_endpoints, rating_endpoints, user_endpoints, category_endpoints, tag_endpoints
import app.api.auth as auth
from app.config import settings

# Initialise Sentry avec ton DSN (à stocker dans une variable d'environnement)
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    traces_sample_rate=1.0  # Ajuste en fonction de tes besoins
)

app = FastAPI(
    title="API de Rating",
    description="Une API REST pour gérer des ratings (notes) sur divers items.",
    version="1.0.0"
)

app.include_router(category_endpoints.router)
app.include_router(tag_endpoints.router)
app.include_router(rating_endpoints.router)
app.include_router(user_endpoints.router)
app.include_router(item_endpoints.router)
app.include_router(auth.router)

if(settings.PROMETHEUS_ENABLED):
    # Instrumentation pour Prometheus
    Instrumentator().instrument(app).expose(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SentryAsgiMiddleware)

# Lancer l'application si le fichier est exécuté directement
if __name__ == "__main__":
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)
