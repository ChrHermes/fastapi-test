# app/routes/system.py

import docker

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.services.docker_service import (
    restart_compose_environment,
    update_docker_images,
    list_docker_containers,
    get_registry_images,
    compare_image_versions,
)
from app.schemas.errors import (
    DockerComposeRestartError,
    DockerImagesUpdateError,
)
from app.utils.auth import get_current_user

router = APIRouter()

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None


# =====================================
#          DOCKER
# =====================================


# -------------------------------------------
# Aktuelle Container/Images
# -------------------------------------------
@router.get("/docker/containers/")
async def list_containers():
    """
    🐳 **Docker-Containerübersicht für Compose-Projekt**

    Diese Route gibt eine strukturierte Liste aller Docker-Container zurück, 
    die dem Compose-Projekt gemäß `settings.COMPOSE_NAME` zugeordnet sind.

    Jeder Container enthält Informationen wie Name, Status, Laufzeit, Image und Version.
    Die Uptime wird dabei sowohl lesbar (`"2 Tage, 3 Stunden"`) als auch in Sekunden (`uptime_seconds`) geliefert.

    **Rückgabeformat:**
    ```json
    {
        "containers": [
            {
                "id": "ab123456",
                "name": "backend",
                "image": "application-backend:latest",
                "version": "1.1.0",
                "uptime": "2 Tage, 1 Stunde",
                "uptime_seconds": 183600,
                "status": "Läuft"
            },
            ...
        ]
    }
    ```

    **Fehler:**
    - `500 Internal Server Error`: Wenn Container nicht abgerufen werden können.

    Returns:
        dict: Ein Dictionary mit dem Schlüssel `"containers"` und einer Liste der Container-Infos.
    """
    try:
        containers = list_docker_containers(settings.COMPOSE_NAME)
        return {"containers": containers}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fehler beim Abrufen der Container: {str(e)}"
        )


# -------------------------------------------
# Abfrage der Registry
# -------------------------------------------
@router.get("/docker/registry/images")
async def get_registry_info(user: str = Depends(get_current_user)):
    """
    🛒 **Ruft verfügbare Docker-Images aus der Registry ab**

    Diese Route fragt eine private Registry nach den verfügbaren Images und deren Versionen ab,
    die im Projekt verwendet werden könnten.

    **Args:**
    - `user` (str): Authentifizierter Benutzer über `Depends(get_current_user)`.

    **Returns:**
    - `dict`: Enthält die Registry-Informationen unter `"registry_images"`.

    **Raises:**
    - `500 Internal Server Error`: Bei Verbindungsfehlern zur Registry.
    """
    try:
        registry_images = get_registry_images(settings.IMAGES)
        return {"registry_images": registry_images}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Fehler bei der Abfrage der Registry: {str(e)}"
        )


# -------------------------------------------
# Vergleich: Welche Updates sind verfügbar?
# -------------------------------------------
@router.get("/docker/updates")
async def check_for_updates(user: str = Depends(get_current_user)):
    """
    🔄 **Prüft auf verfügbare Updates für Container-Images**

    Diese Route vergleicht laufende Container-Images mit den in der Registry verfügbaren Versionen
    und liefert eine Übersicht über mögliche Updates.

    **Args:**
    - `user` (str): Authentifizierter Benutzer über `Depends(get_current_user)`.

    **Returns:**
    - `dict`: Enthält Update-Informationen unter `"updates"`.

    **Raises:**
    - `500 Internal Server Error`: Bei Fehlern beim Vergleich.
    """
    try:
        containers = list_docker_containers(settings.COMPOSE_NAME)
        registry_images = get_registry_images(settings.IMAGES)
        updates = compare_image_versions(containers, registry_images)
        return {"updates": updates}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Fehler beim Vergleichen der Versionen: {str(e)}"
        )


# -------------------------------------------
# Update und Neustart (Zukunftsplanung)
# -------------------------------------------
@router.post("/docker/update")
async def update_images(user: str = Depends(get_current_user)):
    """
    ⬇️ **Aktualisiert die Docker-Images über `docker-compose pull`**

    Diese Route startet den Update-Prozess für alle Services, basierend auf dem aktuellen Compose-Setup.
    Es wird die Funktion `update_docker_images()` verwendet.

    **Args:**
    - `user` (str): Authentifizierter Benutzer über `Depends(get_current_user)`.

    **Returns:**
    - `dict`: Ergebnis des Update-Vorgangs.

    **Raises:**
    - `500 Internal Server Error`: Falls beim Update ein Fehler auftritt.
    """
    try:
        return update_docker_images()
    except DockerImagesUpdateError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/docker/restart")
async def restart_compose(user: str = Depends(get_current_user)):
    """
    🔁 **Startet die docker-compose Umgebung neu**

    Diese Route ruft `restart_compose_environment()` auf, um alle Services des aktuellen Projekts
    kontrolliert neu zu starten.

    **Args:**
    - `user` (str): Authentifizierter Benutzer über `Depends(get_current_user)`.

    **Returns:**
    - `dict`: Ergebnis des Neustart-Vorgangs.

    **Raises:**
    - `500 Internal Server Error`: Falls der Neustart fehlschlägt.
    """
    try:
        result = restart_compose_environment()
        return result
    except DockerComposeRestartError as e:
        raise HTTPException(status_code=500, detail=str(e))
