# app/routes/system.py

import os
import docker
import subprocess
import time
import requests
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.services.log_service import write_log
from fastapi.responses import JSONResponse
from app.utils.auth import get_current_user

router = APIRouter()

BACKEND_CONTAINER = os.getenv("BACKEND_CONTAINER_NAME", "backend")
DB_PATH = os.getenv("DB_PATH", "/data/gcn.db")
DELAY_SHUTDOWN = os.getenv("DELAY_SHUTDOWN", 10)
DELAY_REBOOT = os.getenv("DELAY_REBOOT", 10)

# Konfiguration: GitLab-Projekt-ID und Personal Access Token
GITLAB_PAT = os.getenv("GITLAB_PAT", "your_access_token")
REGISTRY_URL = os.getenv("REGISTRY_URL", "https://gitlab.de")
COMPOSE_PATH = "/opt/gridcal"
IMAGES = ['gcn_backend',
          'gcn_frontend',
          'gateway',
          'gcnia']

CONTAINER = ['gridcal-frontend-1',
             'gridcal-gatewaycontrol-1',
             'gridcal-backend-1',
             'gridcal-gcfcs-1',
             'gridcal-gcgw-1',
             'gridcal-gcnia-1']

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None

# =====================================
#          SYSTEM
# ===================================== 

@router.post("/system/shutdown")
def shutdown_system(background_tasks: BackgroundTasks, user: str = Depends(get_current_user)):
    write_log("WARN", f"Herunterfahren wird in {DELAY_SHUTDOWN} Sekunden eingeleitet")
    background_tasks.add_task(delayed_shutdown)
    return {"message": f"Herunterfahren wird in {DELAY_SHUTDOWN} Sekunden eingeleitet"}

@router.post("/system/reboot")
def reboot_system(background_tasks: BackgroundTasks, user: str = Depends(get_current_user)):
    write_log("WARN", f"Neustart wird in {DELAY_REBOOT} Sekunden eingeleitet")
    background_tasks.add_task(delayed_reboot)
    return {"message": f"Neustart wird in {DELAY_REBOOT} Sekunden eingeleitet"}

# ----------------- supporting methods

def delayed_shutdown():
    time.sleep(DELAY_SHUTDOWN)
    try:
        subprocess.run(["poweroff"], check=True)
    except Exception as e:
        write_log("ERROR", f"Fehler beim Herunterfahren: {str(e)}")

def delayed_reboot():
    time.sleep(DELAY_REBOOT)
    try:
        subprocess.run(["reboot"], check=True)
    except Exception as e:
        write_log("ERROR", f"Fehler beim Neustart: {str(e)}")

# =====================================
#          DATABASE
# ===================================== 

@router.post("/database/reset")
def database_reset(user: str = Depends(get_current_user)):
    import time
    import datetime
    import shutil
    try:
        if docker_client is None:
            write_log("ERROR", "Docker client nicht verfügbar")
            return JSONResponse(content={"error": "Docker client nicht verfügbar"}, status_code=500)

        # 1. Container-Existenz prüfen
        try:
            container = docker_client.containers.get(BACKEND_CONTAINER)
            write_log("INFO", f"Container '{BACKEND_CONTAINER}' gefunden")
        except docker.errors.NotFound:
            write_log("ERROR", f"Container '{BACKEND_CONTAINER}' existiert nicht")
            return JSONResponse(content={"error": f"Container '{BACKEND_CONTAINER}' existiert nicht"}, status_code=404)

        # 2. Container stoppen und sicherstellen, dass er wirklich gestoppt ist
        container.stop()
        timeout = 60  # maximale Wartezeit in Sekunden
        while timeout > 0:
            container.reload()
            if container.status == "exited":
                break
            time.sleep(0.5)
            timeout -= 0.5
        if container.status != "exited":
            write_log("ERROR", f"Container '{BACKEND_CONTAINER}' konnte nicht gestoppt werden, aktueller Status: {container.status}")
            return JSONResponse(content={"error": f"Container '{BACKEND_CONTAINER}' konnte nicht gestoppt werden"}, status_code=500)
        write_log("INFO", f"Container '{BACKEND_CONTAINER}' erfolgreich gestoppt")

        # 3. Backup der Datenbank erstellen
        if os.path.exists(DB_PATH):
            backup_dir = "/data/backup"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                write_log("INFO", f"Backup-Ordner '{backup_dir}' wurde erstellt")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            backup_filename = os.path.join(backup_dir, f"gcn.db_{timestamp}")
            shutil.copy2(DB_PATH, backup_filename)
            write_log("INFO", f"Backup der Datenbank erstellt: {backup_filename}")
        else:
            write_log("WARN", f"Datenbank '{DB_PATH}' existiert nicht. Kein Backup erstellt")

        # 4. Löschen der Datenbankdateien (Datenbank, -wal und -journal)
        db_files = [DB_PATH, f"{DB_PATH}-wal", f"{DB_PATH}-journal", f"{DB_PATH}-shm"]
        for file in db_files:
            if os.path.exists(file):
                os.remove(file)
                write_log("INFO", f"Datei '{file}' wurde gelöscht")
            else:
                write_log("DEBUG", f"Datei '{file}' existiert nicht")

        # 5. Container sicher neu starten
        container.start()
        timeout = 60  # maximale Wartezeit in Sekunden
        while timeout > 0:
            container.reload()
            if container.status == "running":
                break
            time.sleep(0.5)
            timeout -= 0.5
        if container.status != "running":
            write_log("ERROR", f"Container '{BACKEND_CONTAINER}' konnte nicht gestartet werden, aktueller Status: {container.status}")
            return JSONResponse(content={"error": f"Container '{BACKEND_CONTAINER}' konnte nicht gestartet werden"}, status_code=500)
        write_log("INFO", f"Container '{BACKEND_CONTAINER}' erfolgreich gestartet")

        write_log("INFO", "Datenbank wurde erfolgreich zurückgesetzt")
        return {"message": "Datenbank wurde erfolgreich zurückgesetzt"}
    except Exception as e:
        write_log("ERROR", f"Fehler beim Zurücksetzen der DB: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/database/info")
def database_info():
    """
    Gibt die aktuelle Größe der Datenbank zurück.
    Dynamische Größenangaben werden in B, kB, MB, GB oder TB zurückgegeben.
    Falls die DB nicht existiert, wird '0 B' geliefert.
    """
    if os.path.exists(DB_PATH):
        size_in_bytes = os.path.getsize(DB_PATH)
        return {"size": format_size(size_in_bytes)}
    else:
        return {"size": "0 B"}

# ----------------- supporting methods

def format_size(size_bytes):
    """
    Formatiert eine Größe in Bytes in eine menschenlesbare Form (B, kB, MB, GB, TB).
    """
    if size_bytes == 0:
        return "0 B"
    units = ["B", "kB", "MB", "GB", "TB"]
    index = 0
    while size_bytes >= 1024 and index < len(units) - 1:
        size_bytes /= 1024.0
        index += 1
    return f"{size_bytes:.2f} {units[index]}"

# =====================================
#          REGISTRY
# ===================================== 

@router.get("/docker/check")
async def check_registry(user: str = Depends(get_current_user)):
    """
    Prüft die Docker-Images in der Registry und extrahiert den "Version"-Label.
    """
    write_log("INFO", "Starte Überprüfung der Registry-Images")
    results = {}
    for image in IMAGES:
        try:
            write_log("INFO", f"Überprüfe Image: {image}")
            manifest = get_manifest(image)
            config_digest = manifest.get("config", {}).get("digest")
            if not config_digest:
                raise Exception("Kein Config-Digest im Manifest gefunden")
            
            config_blob = get_config_blob(image, config_digest)
            version_label = config_blob.get("config", {}).get("Labels", {}).get("Version", "unbekannt")
            write_log("INFO", f"Image {image} hat Version: {version_label}")
            
            results[image] = {
                "version": version_label,
                "manifest_digest": config_digest
            }
        except Exception as e:
            write_log("ERROR", f"Fehler bei der Überprüfung von {image}: {str(e)}")
            results[image] = {"error": str(e)}
    
    write_log("INFO", "Überprüfung der Registry-Images abgeschlossen")
    return {"images": results}

@router.post("/docker/update")
async def update_images(user: str = Depends(get_current_user)):
    """
    Aktualisiert die Docker-Images mittels docker-compose pull.
    Es wird angenommen, dass sich die docker-compose.yml im Arbeitsverzeichnis COMPOSE_PATH (/opt/gridcal) befindet.
    """
    write_log("INFO", "Starte Update der Docker-Images")
    try:
        pull_command = ["docker-compose", "pull"] + IMAGES
        write_log("INFO", f"Führe Befehl aus: {' '.join(pull_command)} im Verzeichnis {COMPOSE_PATH}")
        result = subprocess.run(
            pull_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=COMPOSE_PATH
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
        write_log("INFO", f"Führe Befehl aus: {' '.join(down_command)} im Verzeichnis {COMPOSE_PATH}")
        subprocess.run(
            down_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=COMPOSE_PATH
        )
        
        # Umgebung im Detached-Modus starten
        up_command = ["docker-compose", "up", "-d"]
        write_log("INFO", f"Führe Befehl aus: {' '.join(up_command)} im Verzeichnis {COMPOSE_PATH}")
        result = subprocess.run(
            up_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=COMPOSE_PATH
        )
        write_log("INFO", "Docker-compose Umgebung wurde erfolgreich neu gestartet")
        return {"status": "Docker-compose Umgebung wurde erfolgreich neu gestartet", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        write_log("ERROR", f"Fehler beim Neustarten der docker-compose Umgebung: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Neustart der docker-compose Umgebung fehlgeschlagen: {e.stderr}")


# ----------------- supporting methods

def get_manifest(image: str, tag: str = "latest"):
    manifest_url = f"{REGISTRY_URL}/v2/{image}/manifests/{tag}"
    headers = {
        "Accept": "application/vnd.docker.distribution.manifest.v2+json",
        "Authorization": f"Bearer {GITLAB_PAT}"
    }
    write_log("INFO", f"Rufe Manifest für {image}:{tag} ab von {manifest_url}")
    response = requests.get(manifest_url, headers=headers)
    if response.status_code != 200:
        write_log("ERROR", f"Fehler beim Laden des Manifests für {image}:{tag}. Status Code: {response.status_code}")
        raise Exception(f"Manifest für {image}:{tag} konnte nicht geladen werden: {response.status_code}")
    write_log("INFO", f"Manifest für {image}:{tag} erfolgreich geladen")
    return response.json()

def get_config_blob(image: str, digest: str):
    blob_url = f"{REGISTRY_URL}/v2/{image}/blobs/{digest}"
    headers = {
        "Authorization": f"Bearer {GITLAB_PAT}"
    }
    write_log("INFO", f"Rufe Config-Blob für {image} mit Digest {digest} ab von {blob_url}")
    response = requests.get(blob_url, headers=headers)
    if response.status_code != 200:
        write_log("ERROR", f"Fehler beim Laden des Config-Blobs für {image} (Digest: {digest}). Status Code: {response.status_code}")
        raise Exception(f"Config-Blob für {image} (Digest: {digest}) konnte nicht geladen werden: {response.status_code}")
    write_log("INFO", f"Config-Blob für {image} erfolgreich geladen")
    return response.json()

