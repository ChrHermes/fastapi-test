# app/routes/system.py

import os
import docker
import subprocess
import requests

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException

from app.config import settings
from app.services.log_service import write_log
from app.services.database_service import database_reset, database_info
from app.services.system_service import delayed_reboot, delayed_shutdown
from app.services.docker_service import check_registry_images, restart_compose_environment, update_docker_images
from app.schemas.errors import *
from app.utils.auth import get_current_user

router = APIRouter()

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None

# =====================================
#          SYSTEM
# ===================================== 

@router.post("/system/shutdown")
def shutdown_system(background_tasks: BackgroundTasks, user: str = Depends(get_current_user)):
    write_log("WARN", f"Herunterfahren wird in {settings.DELAY_SHUTDOWN} Sekunden eingeleitet")
    background_tasks.add_task(delayed_shutdown(settings.DELAY_SHUTDOWN))
    return {"message": f"Herunterfahren wird in {settings.DELAY_SHUTDOWN} Sekunden eingeleitet"}

@router.post("/system/reboot")
def reboot_system(background_tasks: BackgroundTasks, user: str = Depends(get_current_user)):
    write_log("WARN", f"Neustart wird in {settings.DELAY_REBOOT} Sekunden eingeleitet")
    background_tasks.add_task(delayed_reboot(settings.DELAY_REBOOT))
    return {"message": f"Neustart wird in {settings.DELAY_REBOOT} Sekunden eingeleitet"}


# =====================================
#          DATABASE
# ===================================== 

@router.post("/database/reset")
async def post_database_reset(user: str = Depends(get_current_user)):
    try:
        result = await database_reset(
            backend_container=settings.BACKEND_CONTAINER,
            database_path=settings.DB_PATH
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
    try:
        result = await database_info(
            database_path=settings.DB_PATH
        )
        return result
    except DatabaseInfoError as e:
        raise HTTPException(status_code=500, detail=str(e)) 


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
