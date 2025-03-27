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
    GITLAB_PAT: str = "your_access_token"
    REGISTRY_URL: str = "https://gitlab.de"
    
    # Compose-Pfad und Image/Container Listen
    COMPOSE_PATH: str = "/opt/gridcal"
    COMPOSE_NAME: str = "gridcal"

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


# Erzeugung einer globalen Settings-Instanz, die überall importiert werden kann
settings = Settings()
