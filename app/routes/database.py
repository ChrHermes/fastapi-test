# app/routes/system.py

import docker

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.services.database_service import database_reset, database_info
from app.schemas.errors import (
    DockerClientNotAvailableError,
    ContainerNotFoundError,
    DatabaseNotFoundError,
    DatabaseResetError,
    DatabaseInfoError,
)
from app.utils.auth import get_current_user

router = APIRouter()

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None


# =====================================
#          DATABASE
# =====================================


@router.post("/database/reset")
async def post_database_reset(user: str = Depends(get_current_user)):
    """
    🗑 **Setzt die Datenbank zurück**

    Diese Route stoppt den Container, entfernt die Datenbankdatei und startet den Container neu.

    - 🐳 Verwendet den Container `settings.BACKEND_CONTAINER_NAME`
    - 📂 Zielpfad der Datenbank: `settings.DB_PATH`
    - ⚙️ Führt das Zurücksetzen über die Funktion `database_reset()` aus

    **Args:**
    - `user` (str): Authentifizierter Benutzer, bereitgestellt über `Depends(get_current_user)`

    **Returns:**
    - `dict`: Rückgabe der `database_reset()`-Funktion mit Statusinformationen.

    **Raises:**
    - `500 Internal Server Error`: Bei Problemen mit dem Docker-Client oder während Stop/Start des Containers.
    - `404 Not Found`: Wenn der Container nicht gefunden wurde.
    """
    try:
        result = await database_reset(
            backend_container=settings.BACKEND_CONTAINER_NAME,
            database_path=settings.DB_PATH,
        )
        return result
    except DockerClientNotAvailableError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ContainerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (ContainerStopError, ContainerStartError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseResetError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/database/info")
async def get_database_info(user: str = Depends(get_current_user)):
    """
    ℹ️ **Liefert Informationen zur aktuellen Datenbank**

    Ruft Basisinformationen zur bestehenden SQLite-Datenbank ab.

    - 📂 Erwartet die Datenbank unter dem Pfad `settings.DB_PATH`
    - 🧠 Liest Struktur und ggf. Metadaten mit `database_info()`

    **Args:**
    - `user` (str): Authentifizierter Benutzer, bereitgestellt über `Depends(get_current_user)`

    **Returns:**
    - `dict`: Informationen zur Datenbank (z. B. Tabellen, Größe, Pfad).

    **Raises:**
    - `404 Not Found`: Wenn die Datenbankdatei nicht gefunden wurde.
    - `500 Internal Server Error`: Bei sonstigen Fehlern beim Auslesen der Datenbank.
    """
    try:
        result = await database_info(database_path=settings.DB_PATH)
        return result
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DatabaseInfoError as e:
        raise HTTPException(status_code=500, detail=str(e))
