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
from app.services.docker_service import check_registry_images
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

# ----------------- supporting methods


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
#          REGISTRY
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
    Es wird angenommen, dass sich die docker-compose.yml im Arbeitsverzeichnis COMPOSE_PATH (/opt/gridcal) befindet.
    """
    write_log("INFO", "Starte Update der Docker-Images")
    try:
        pull_command = ["docker-compose", "pull"] + settings.IMAGES
        write_log("INFO", f"Führe Befehl aus: {' '.join(pull_command)} im Verzeichnis {settings.COMPOSE_PATH}")
        result = subprocess.run(
            pull_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=settings.COMPOSE_PATH
        )
        write_log("INFO", "Docker-Images wurden erfolgreich aktualisiert")
        return {"status": "Docker-Images wurden erfolgreich aktualisiert", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        write_log("ERROR", f"Fehler beim Update der Images: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Update der Images fehlgeschlagen: {e.stderr}")


@router.post("/docker/restart")
async def restart_compose(user: str = Depends(get_current_user)):
    """
    Startet die docker-compose Umgebung neu.
    Dazu wird zunächst die Umgebung gestoppt (docker-compose down) und anschließend im Detached-Modus neu gestartet (docker-compose up -d).
    Das Arbeitsverzeichnis (COMPOSE_PATH) wird hierbei verwendet.
    """
    write_log("INFO", "Starte Neustart der docker-compose Umgebung")
    try:
        # Umgebung stoppen
        down_command = ["docker-compose", "down"]
        write_log("INFO", f"Führe Befehl aus: {' '.join(down_command)} im Verzeichnis {settings.COMPOSE_PATH}")
        subprocess.run(
            down_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=settings.COMPOSE_PATH
        )
        
        # Umgebung im Detached-Modus starten
        up_command = ["docker-compose", "up", "-d"]
        write_log("INFO", f"Führe Befehl aus: {' '.join(up_command)} im Verzeichnis {settings.COMPOSE_PATH}")
        result = subprocess.run(
            up_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=settings.COMPOSE_PATH
        )
        write_log("INFO", "Docker-compose Umgebung wurde erfolgreich neu gestartet")
        return {"status": "Docker-compose Umgebung wurde erfolgreich neu gestartet", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        write_log("ERROR", f"Fehler beim Neustarten der docker-compose Umgebung: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Neustart der docker-compose Umgebung fehlgeschlagen: {e.stderr}")
