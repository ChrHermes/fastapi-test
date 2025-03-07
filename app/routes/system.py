# app/routes/system.py

import os
import docker
from fastapi import APIRouter, Depends
from app.services.log_service import write_log
from fastapi.responses import JSONResponse
from app.utils.auth import get_current_user

router = APIRouter()

BACKEND_CONTAINER = os.getenv("BACKEND_CONTAINER_NAME", "backend")
DB_PATH = os.getenv("DB_PATH", "/data/gcn.db")

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None

# =====================================
#          SYSTEM
# ===================================== 

@router.post("/system/shutdown")
def shutdown_system():
    write_log("WARN", "System wird heruntergefahren")
    return {"message": "System wird heruntergefahren..."}

# =====================================
#          DATABASE
# ===================================== 

@router.post("/database/reset")
def database_reset(user: str = Depends(get_current_user)):
    try:
        container = docker_client.containers.get(BACKEND_CONTAINER)
        container.stop()
        for file in [DB_PATH, f"{DB_PATH}-wal", f"{DB_PATH}-journal"]:
            if os.path.exists(file):
                os.remove(file)
        write_log("WARN", "Datenbank wurde erfolgreich zurückgesetzt")
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
