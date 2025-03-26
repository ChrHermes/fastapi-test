# app/services/docker_service.py

import docker
import time
import subprocess

from app.config import settings
from app.services.log_service import write_log
from app.schemas.errors import *

# ------------------------------
#    Docker Client Initialisierung
# ------------------------------

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None

# =====================================
#          START/STOP CONTAINER
# ===================================== 

def container_stop(container, container_name: str, timeout: float = 60):
    """
    Stoppt den angegebenen Container und stellt sicher,
    dass er innerhalb der Timeout-Zeit den Status 'exited' erreicht.
    """
    container.stop()
    while timeout > 0:
        container.reload()
        if container.status == "exited":
            break
        time.sleep(0.5)
        timeout -= 0.5
    if container.status != "exited":
        write_log("ERROR", f"Container '{container_name}' konnte nicht gestoppt werden, aktueller Status: {container.status}")
        raise ContainerStopError(f"Container '{container_name}' konnte nicht gestoppt werden")
    write_log("INFO", f"Container '{container_name}' erfolgreich gestoppt")


def container_start(container, container_name: str, timeout: float = 60):
    """
    Startet den angegebenen Container und stellt sicher,
    dass er innerhalb der Timeout-Zeit den Status 'running' erreicht.
    """
    container.start()
    while timeout > 0:
        container.reload()
        if container.status == "running":
            break
        time.sleep(0.5)
        timeout -= 0.5
    if container.status != "running":
        write_log("ERROR", f"Container '{container_name}' konnte nicht gestartet werden, aktueller Status: {container.status}")
        raise ContainerStartError(f"Container '{container_name}' konnte nicht gestartet werden")
    write_log("INFO", f"Container '{container_name}' erfolgreich gestartet")


# =====================================
#          REGISTRY CHECK
# ===================================== 

def check_registry_images(images: List[str]) -> dict:
    """
    Prüft die Docker-Images in der Registry und extrahiert den "Version"-Label.
    """
    results = {}
    write_log("INFO", "Starte Überprüfung der Registry-Images")
    for image in images:
        try:
            write_log("INFO", f"Überprüfe Image: {image}")
            manifest = get_manifest(image)
            config_digest = manifest.get("config", {}).get("digest")
            if not config_digest:
                raise ManifestError("Kein Config-Digest im Manifest gefunden")
            
            config_blob = get_config_blob(image, config_digest)
            version_label = config_blob.get("config", {}).get("Labels", {}).get("Version")
            if version_label is None:
                raise ConfigBlobError("Kein Version-Label im Config-Blob gefunden")
            
            write_log("INFO", f"Image {image} hat Version: {version_label}")
            
            results[image] = {
                "version": version_label,
                "manifest_digest": config_digest
            }
        except (ManifestError, ConfigBlobError) as e:
            write_log("ERROR", f"Fehler bei der Überprüfung von {image}: {str(e)}")
            results[image] = {"error": str(e)}
        except Exception as e:
            # Für alle anderen Fehler
            write_log("ERROR", f"Unbekannter Fehler bei der Überprüfung von {image}: {str(e)}")
            results[image] = {"error": str(e)}
    
    write_log("INFO", "Überprüfung der Registry-Images abgeschlossen")
    return {"images": results}


# =====================================
#           COMPOSE OPERATIONS
# ===================================== 

def restart_compose_environment() -> dict:
    """
    Startet die docker-compose Umgebung neu, indem zuerst 'docker-compose down'
    und anschließend 'docker-compose up -d' ausgeführt wird. Das Arbeitsverzeichnis
    (settings.COMPOSE_PATH) wird hierfür verwendet.
    
    Gibt ein Dictionary mit Status und Output zurück.
    Wirft eine DockerComposeRestartError, falls ein Fehler auftritt.
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
        raise DockerComposeRestartError(f"Neustart der docker-compose Umgebung fehlgeschlagen: {e.stderr}")


# =====================================
#          UPDATE DOCKER IMAGES
# ===================================== 

def update_docker_images() -> dict:
    """
    Aktualisiert die Docker-Images mittels 'docker-compose pull'.
    Führt den Befehl im Verzeichnis settings.COMPOSE_PATH aus.
    
    Gibt ein Dictionary mit Status und Output zurück.
    Wirft DockerImagesUpdateError bei einem Fehler.
    """
    write_log("INFO", "Starte Update der Docker-Images")
    try:
        # Erstelle den Pull-Befehl, der alle in settings.IMAGES definierten Images zieht
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
        raise DockerImagesUpdateError(f"Update der Images fehlgeschlagen: {e.stderr}")


# =====================================
#          SUPPORT FUNCTIONS
# ===================================== 

def get_manifest(image: str, tag: str = "latest"):
    manifest_url = f"{settings.REGISTRY_URL}/v2/{image}/manifests/{tag}"
    headers = {
        "Accept": "application/vnd.docker.distribution.manifest.v2+json",
        "Authorization": f"Bearer {settings.GITLAB_PAT}"
    }
    write_log("INFO", f"Rufe Manifest für {image}:{tag} ab von {manifest_url}")
    response = requests.get(manifest_url, headers=headers)
    if response.status_code != 200:
        write_log("ERROR", f"Fehler beim Laden des Manifests für {image}:{tag}. Status Code: {response.status_code}")
        raise Exception(f"Manifest für {image}:{tag} konnte nicht geladen werden: {response.status_code}")
    write_log("INFO", f"Manifest für {image}:{tag} erfolgreich geladen")
    return response.json()


def get_config_blob(image: str, digest: str):
    blob_url = f"{settings.REGISTRY_URL}/v2/{image}/blobs/{digest}"
    headers = {
        "Authorization": f"Bearer {settings.GITLAB_PAT}"
    }
    write_log("INFO", f"Rufe Config-Blob für {image} mit Digest {digest} ab von {blob_url}")
    response = requests.get(blob_url, headers=headers)
    if response.status_code != 200:
        write_log("ERROR", f"Fehler beim Laden des Config-Blobs für {image} (Digest: {digest}). Status Code: {response.status_code}")
        raise Exception(f"Config-Blob für {image} (Digest: {digest}) konnte nicht geladen werden: {response.status_code}")
    write_log("INFO", f"Config-Blob für {image} erfolgreich geladen")
    return response.json()

