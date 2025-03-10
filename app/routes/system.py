# app/routes/system.py

import os
import docker
import subprocess
import time
from fastapi import APIRouter, Depends, BackgroundTasks
from app.services.log_service import write_log
from fastapi.responses import JSONResponse
from app.utils.auth import get_current_user

router = APIRouter()

BACKEND_CONTAINER = os.getenv("BACKEND_CONTAINER_NAME", "backend")
DB_PATH = os.getenv("DB_PATH", "/data/gcn.db")
DELAY_SHUTDOWN = os.getenv("DELAY_SHUTDOWN", 10)
DELAY_REBOOT = os.getenv("DELAY_REBOOT", 10)

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None

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
    Gibt die aktuelle Größe der Datenbank (in MB) zurück.
    Falls die DB nicht existiert, wird '0 MB' geliefert.
    """
    if os.path.exists(DB_PATH):
        size_in_bytes = os.path.getsize(DB_PATH)
        size_in_mb = size_in_bytes / (1024 * 1024)
        return {"size": f"{size_in_mb:.2f} MB"}
    else:
        return {"size": "0 MB"}

# =====================================
#          REGISTRY
# ===================================== 

@router.get("/registry/check")
def registry_check(user: str = Depends(get_current_user)):
    """
    Prüft beispielhaft für die Container 'backend', 'frontend', 'gateway' und 'gcnia'
    ob ein Softwareupdate vorliegt. Hier wird simuliert, dass für den 'backend'-Container
    ein Update verfügbar ist (z.B. Version "v2.0"), während für die anderen Container
    kein Update vorliegt.
    """
    updates = {}
    containers = ['backend', 'frontend', 'gateway', 'gcnia']
    for container in containers:
        # Beispielhafte Logik: Nur beim 'backend'-Container wird ein Update angenommen.
        if container == "backend":
            updates[container] = {"available": True, "newVersion": "v2.0"}
        else:
            updates[container] = {"available": False}
    write_log("INFO", "Registry-Check durchgeführt")
    return {"updates": updates}

@router.post("/registry/update")
def registry_update(user: str = Depends(get_current_user)):
    """
    Führt beispielhaft die Softwareaktualisierung für die Container durch, für die
    ein Update verfügbar ist. Hier wird die Aktualisierung simuliert, indem die
    Container (sofern vorhanden) neu gestartet werden.
    """
    updated = {}
    containers = ['backend', 'frontend', 'gateway', 'gcnia']
    for container in containers:
        try:
            cont = docker_client.containers.get(container)
            # Beispielhafte Aktualisierung: Container neu starten
            cont.restart()
            updated[container] = "updated"
        except Exception as e:
            updated[container] = f"Fehler: {str(e)}"
    write_log("INFO", "Registry Update durchgeführt")
    return {"message": "Registry Update durchgeführt", "details": updated}
