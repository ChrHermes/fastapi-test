# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import auth, system, docker, logging, database

def create_app() -> FastAPI:
    app = FastAPI(
        title="DemoBox Admin",
        version="0.1.0",
        docs_url="/api-documentation" if settings.DEBUG else None,
        redoc_url=None,
        # openapi_url=None
    )

    # CORS für das externe Frontend (z. B. auf Port 3000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routers(app)

    # rendedered static frontend einbinden
    if settings.SERVE_FRONTEND:
        app.mount("/", StaticFiles(directory="public", html=True), name="frontend")
   
    return app


def register_routers(app: FastAPI):
    # API-Routen registrieren
    api_prefix: str = "/api"
    app.include_router(auth.router, prefix=api_prefix, tags=["auth"])
    app.include_router(system.router, prefix=api_prefix, tags=["system"])
    app.include_router(docker.router, prefix=api_prefix, tags=["docker"])
    app.include_router(logging.router, prefix=api_prefix, tags=["logs"])
    app.include_router(database.router, prefix=api_prefix, tags=["database"])

app = create_app()
