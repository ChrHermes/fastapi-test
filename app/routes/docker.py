# app/routes/system.py

import docker

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.services.log_service import write_log
from app.services.docker_service import (
    check_registry_images,
    restart_compose_environment,
    update_docker_images,
    list_docker_containers,
    get_registry_images,
    compare_image_versions
)
from app.schemas.errors import *
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
    Liefert alle Docker-Container, die dem definierten Compose-Projekt zugeordnet sind.
        Die Funktion sucht nach Containern, die das Label "com.docker.compose.project" enthalten,
        wobei der im Settings definierte Name (z. B. "gridcal") als Filter genutzt wird.
    Returns:
        dict: Ein Dictionary mit einer Liste der gefundenen Container unter dem Schlüssel "containers".
    Raises:
        HTTPException: Falls ein Fehler beim Abrufen der Container auftritt.
    """
    try:
        containers = list_docker_containers(settings.COMPOSE_NAME)
        return {"containers": containers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Container: {str(e)}")


# -------------------------------------------
# Abfrage der Registry
# -------------------------------------------
@router.get("/docker/registry/images")
async def get_registry_info(user: str = Depends(get_current_user)):
    """
    Ruft Informationen zu Docker-Images aus der privaten Registry ab.
        Diese Route stellt eine Verbindung zur Registry her, um die verfügbaren Docker-Images
        (und deren Versionen) abzurufen, die für das Projekt relevant sind.
    Args:
        user (str): Der aktuell authentifizierte Benutzer, bereitgestellt über die Dependency Injection.
    Returns:
        dict: Ein Dictionary mit den Registry-Images unter dem Schlüssel "registry_images".
    Raises:
        HTTPException: Falls ein Fehler bei der Abfrage der Registry auftritt.
    """
    try:
        registry_images = get_registry_images(settings.IMAGES)
        return {"registry_images": registry_images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler bei der Abfrage der Registry: {str(e)}")


# -------------------------------------------
# Vergleich: Welche Updates sind verfügbar?
# -------------------------------------------
@router.get("/docker/updates")
async def check_for_updates(user: str = Depends(get_current_user)):
    """
    Vergleicht die aktuell laufenden Container-Images mit den in der Registry verfügbaren Images.
        Diese Route ermittelt zunächst die laufenden Container des definierten Compose-Projekts,
        ruft anschließend die in der Registry verfügbaren Images ab und vergleicht beide Versionen.
        So wird eine Übersicht geliefert, welche Container-Images ein Update benötigen.
    Args:
        user (str): Der aktuell authentifizierte Benutzer.
    Returns:
        dict: Ein Dictionary mit den verfügbaren Updates unter dem Schlüssel "updates".
    Raises:
        HTTPException: Falls ein Fehler beim Vergleich der Versionen auftritt.
    """
    try:
        containers = list_docker_containers(settings.COMPOSE_NAME)
        registry_images = get_registry_images(settings.IMAGES)
        updates = compare_image_versions(containers, registry_images)
        return {"updates": updates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Vergleichen der Versionen: {str(e)}")


# -------------------------------------------
# Update und Neustart (Zukunftsplanung)
# -------------------------------------------
@router.post("/docker/update")
async def update_images(user: str = Depends(get_current_user)):
    """
    Aktualisiert die Docker-Images mittels docker-compose pull.
        Diese Route löst den Update-Prozess aus, der die Docker-Images aktualisiert.
        Sie verwendet die Funktion update_docker_images, um den Aktualisierungsvorgang durchzuführen.
    Args:
        user (str): Der aktuell authentifizierte Benutzer.
    Returns:
        dict: Ein Dictionary mit dem Ergebnis des Update-Prozesses.
    Raises:
        HTTPException: Falls während des Update-Prozesses ein Fehler auftritt.
    """
    try:
        return update_docker_images()
    except DockerImagesUpdateError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/docker/restart")
async def restart_compose(user: str = Depends(get_current_user)):
    """
    Startet die docker-compose Umgebung neu.
        Diese Route ruft die Funktion restart_compose_environment auf, um den Neustart
        der docker-compose Umgebung durchzuführen.
    Args:
        user (str): Der aktuell authentifizierte Benutzer.
    Returns:
        dict: Ein Dictionary mit dem Ergebnis des Neustarts.
    Raises:
        HTTPException: Falls ein Fehler beim Neustarten der Umgebung auftritt.
    """
    try:
        result = restart_compose_environment()
        return result
    except DockerComposeRestartError as e:
        raise HTTPException(status_code=500, detail=str(e))
