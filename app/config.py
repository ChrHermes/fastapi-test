# app/config.py

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Allgemeine Konfiguration
    ADMIN_USER: str = "SuperAdmin"
    ADMIN_PASS: str = "Asdfg_Poiuz65"
    
    # Weitere Konfigurationen können hier ergänzt werden:
    BACKEND_CONTAINER_NAME: str = "backend"
    DB_PATH: str = "/data/gcn.db"
    DELAY_SHUTDOWN: int = 10
    DELAY_REBOOT: int = 10

    # GitLab-Konfiguration
    GIT_USER: str = "username"
    GIT_PAT: str = "personal_access_token"
    GIT_REGISTRY: str = "https://gitlab.de"
    GIT_REPOSITORY: str = "project_name"

    # Compose-Pfad und Image/Container Listen
    COMPOSE_PATH: str = "/opt/gridcal"
    COMPOSE_NAME: str = "gridcal"

    MOCK_MODE: bool = False

    IMAGES: List[str] = [
        'gcgw',
        'gcfcs',
        'gcnia'
        'backend',
        'frontend',
        'gatewaycontrol',
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        env_prefix = ""
        extra = "allow"


# Erzeugung einer globalen Settings-Instanz, die überall importiert werden kann
settings = Settings()
