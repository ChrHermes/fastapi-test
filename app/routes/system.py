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
