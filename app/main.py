# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, system, docker, logging, database

app = FastAPI()

# CORS für das externe Frontend (z. B. auf Port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ggf. anpassen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-Routen registrieren
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(docker.router, prefix="/api/docker", tags=["docker"])
app.include_router(logging.router, prefix="/api/logs", tags=["logs"])
app.include_router(database.router, prefix="/api/database", tags=["database"])

