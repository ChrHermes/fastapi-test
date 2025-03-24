import docker
import os

from fastapi.responses import JSONResponse

from app.services.log_service import write_log

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None

# =====================================
#          DATABASE
# ===================================== 

async def database_reset(backend_container: str,
                         database_path: str):
    import time
    import datetime
    import shutil
    
    try:
        if docker_client is None:
            write_log("ERROR", "Docker client nicht verfügbar")
            return JSONResponse(content={"error": "Docker client nicht verfügbar"}, status_code=500)

        # ----- 1. Container-Existenz prüfen
        try:
            container = docker_client.containers.get(backend_container)
            write_log("INFO", f"Container '{backend_container}' gefunden")
        except docker.errors.NotFound:
            write_log("ERROR", f"Container '{backend_container}' existiert nicht")
            return JSONResponse(content={"error": f"Container '{backend_container}' existiert nicht"}, status_code=404)

        # ----- 2. Container stoppen und sicherstellen, dass er wirklich gestoppt ist
        container.stop()
        timeout = 60  # maximale Wartezeit in Sekunden
        while timeout > 0:
            container.reload()
            if container.status == "exited":
                break
            time.sleep(0.5)
            timeout -= 0.5
        if container.status != "exited":
            write_log("ERROR", f"Container '{backend_container}' konnte nicht gestoppt werden, aktueller Status: {container.status}")
            return JSONResponse(content={"error": f"Container '{backend_container}' konnte nicht gestoppt werden"}, status_code=500)
        write_log("INFO", f"Container '{backend_container}' erfolgreich gestoppt")

        # ----- 3. Backup der Datenbank erstellen
        if os.path.exists(database_path):
            backup_dir = "/data/backup"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                write_log("INFO", f"Backup-Ordner '{backup_dir}' wurde erstellt")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            backup_filename = os.path.join(backup_dir, f"gcn.db_{timestamp}")
            shutil.copy2(database_path, backup_filename)
            write_log("INFO", f"Backup der Datenbank erstellt: {backup_filename}")
        else:
            write_log("WARN", f"Datenbank '{database_path}' existiert nicht. Kein Backup erstellt")

        # ----- 4. Löschen der Datenbankdateien (Datenbank, -wal und -journal)
        db_files = [database_path, f"{database_path}-wal", f"{database_path}-journal", f"{database_path}-shm"]
        for file in db_files:
            if os.path.exists(file):
                os.remove(file)
                write_log("INFO", f"Datei '{file}' wurde gelöscht")
            else:
                write_log("DEBUG", f"Datei '{file}' existiert nicht")

        # ----- 5. Container sicher neu starten
        container.start()
        timeout = 60  # maximale Wartezeit in Sekunden
        while timeout > 0:
            container.reload()
            if container.status == "running":
                break
            time.sleep(0.5)
            timeout -= 0.5
        if container.status != "running":
            write_log("ERROR", f"Container '{backend_container}' konnte nicht gestartet werden, aktueller Status: {container.status}")
            return JSONResponse(content={"error": f"Container '{backend_container}' konnte nicht gestartet werden"}, status_code=500)
        write_log("INFO", f"Container '{backend_container}' erfolgreich gestartet")

        write_log("INFO", "Datenbank wurde erfolgreich zurückgesetzt")
        return {"message": "Datenbank wurde erfolgreich zurückgesetzt"}
    
    except Exception as e:
        write_log("ERROR", f"Fehler beim Zurücksetzen der DB: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)