# app/routes/system.py

import os
import docker
from fastapi import APIRouter
from app.services.log_service import write_log
from fastapi.responses import JSONResponse

router = APIRouter()

BACKEND_CONTAINER = os.getenv("BACKEND_CONTAINER_NAME", "backend")
DB_PATH = os.getenv("DB_PATH", "/data/gcn.db")

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None

@router.post("/shutdown")
def shutdown_system():
    write_log("WARN", "System wird heruntergefahren")
    return {"message": "System wird heruntergefahren..."}

@router.post("/reset-db")
def reset_database():
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

# NEUE ROUTE FÜR DB-GRÖSSE
@router.get("/db-info")
def get_db_info():
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
