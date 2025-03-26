# app/routes/system.py

import docker

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.services.log_service import write_log
from app.services.docker_service import check_registry_images, restart_compose_environment, update_docker_images
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

@router.get("/docker/containers/")
async def list_containers():
    """
    Liefert alle Container, bei denen das Label "com.docker.compose.project"
    den String "gridcal" enthält.
    """
    try:
        client = docker.from_env()
        all_containers = client.containers.list(all=True)
        # Filter: Nur Container mit dem Label 'com.docker.compose.project' == 'gridcal'
        filtered_containers = [
            container.name
            for container in all_containers
            if "gridcal" in container.labels.get("com.docker.compose.project", "")
        ]
        write_log("INFO", filtered_containers)
        return {"containers": filtered_containers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Container: {str(e)}")


@router.get("/docker/check")
async def check_registry(user: str = Depends(get_current_user)):
    """
    Prüft die Docker-Images in der Registry und extrahiert den "Version"-Label.
    """
    # Übergibt die Liste der Images aus dem zentralen Config-Modul
    return check_registry_images(settings.IMAGES)


@router.post("/docker/update")
async def update_images(user: str = Depends(get_current_user)):
    """
    Aktualisiert die Docker-Images mittels docker-compose pull.
    Es wird angenommen, dass sich die docker-compose.yml im Arbeitsverzeichnis COMPOSE_PATH befindet.
    """
    try:
        return update_docker_images()
    except DockerImagesUpdateError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/docker/restart")
async def restart_compose(user: str = Depends(get_current_user)):
    """
    Route zum Neustarten der docker-compose Umgebung.
    Ruft die Service-Funktion restart_compose_environment() auf.
    """
    try:
        result = restart_compose_environment()
        return result
    except DockerComposeRestartError as e:
        raise HTTPException(status_code=500, detail=str(e))
