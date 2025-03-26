# app/services/database_service.py

import docker
import os

from app.services.log_service import write_log
from app.services.docker_service import container_start, container_stop
from app.schemas.errors import *

# ------------------------------
#    Docker Client Initialisierung
# ------------------------------

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None

# =====================================
#          DATABASE
# ===================================== 

async def database_reset(backend_container: str,
                         database_path: str):
    import datetime
    import shutil
    
    try:
        if docker_client is None:
            write_log("ERROR", "Docker Client nicht verfügbar")
            raise DockerClientNotAvailableError("Docker Client nicht verfügbar")

        # ----- 1. Container-Existenz prüfen
        try:
            container = docker_client.containers.get(backend_container)
            write_log("INFO", f"Container '{backend_container}' gefunden")
        except docker.errors.NotFound:
            write_log("ERROR", f"Container '{backend_container}' existiert nicht")
            raise ContainerNotFoundError(f"Container '{backend_container}' existiert nicht")

        # ----- 2. Container stoppen und sicherstellen, dass er wirklich gestoppt ist
        container_stop(container, backend_container)

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
        db_files = [
            database_path, 
            f"{database_path}-wal", 
            f"{database_path}-journal", 
            f"{database_path}-shm"
        ]
        for file in db_files:
            if os.path.exists(file):
                os.remove(file)
                write_log("INFO", f"Datei '{file}' wurde gelöscht")
            else:
                write_log("DEBUG", f"Datei '{file}' existiert nicht")

        # ----- 5. Container sicher neu starten
        container_start(container, backend_container)

        write_log("INFO", "Datenbank wurde erfolgreich zurückgesetzt")
        return {"message": "Datenbank wurde erfolgreich zurückgesetzt"}
        
    except Exception as e:
        # Falls es sich nicht um einen bereits definierten Fehler handelt, diesen als generischen DatabaseResetError weiterreichen.
        if not isinstance(e, DatabaseResetError):
            write_log("ERROR", f"Fehler beim Zurücksetzen der DB: {str(e)}")
            raise DatabaseResetError(str(e))
        raise


async def database_info(database_path: str):
    """
    Gibt die aktuelle Größe der Datenbank zurück.
    Dynamische Größenangaben werden in B, kB, MB, GB oder TB zurückgegeben.
    Falls die DB nicht existiert, wird '0 B' geliefert.
    """
    try:
        if os.path.exists(database_path):
            size_in_bytes = os.path.getsize(database_path)
            return {"size": format_size(size_in_bytes)}
        else:
            raise DatabaseInfoError(f"{database_path} existiert nicht.")
    except Exception as e:
        # Falls es sich nicht um einen bereits definierten Fehler handelt, diesen als generischen DatabaseResetError weiterreichen.
        if not isinstance(e, DatabaseInfoError):
            write_log("ERROR", f"Fehler beim Auslesen der DB: {str(e)}")
            raise DatabaseInfoError(str(e))
        raise


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