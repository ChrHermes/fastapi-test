# app/services/docker_service.py

import docker
import time
import subprocess
import requests

from typing import List

from app.config import settings
from app.services.log_service import write_log
from app.schemas.errors import (
    ContainerStopError,
    ContainerStartError,
    ManifestError,
    ConfigBlobError,
    DockerComposeRestartError,
    DockerImagesUpdateError,
)

# ------------------------------
#    Docker Client Initialisierung
# ------------------------------

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None


# =====================================
#           COMPOSE OPERATIONS
# =====================================


def list_docker_containers(project_label: str = "gridcal") -> list:
    """
    Liefert alle Docker-Container, die dem definierten Compose-Projekt zugeordnet sind.
        Die Funktion sucht nach Containern, die das Label "com.docker.compose.project" enthalten,
        wobei der im Settings definierte Name (z. B. "gridcal") als Filter genutzt wird.
    Returns:
        list: Eine Liste der Container-Namen, die gefunden wurden.
    Raises:
        Exception: Falls ein Fehler beim Abruf der Container auftritt.
    """
    client = docker.from_env()
    all_containers = client.containers.list(all=True)
    filtered_containers = [
        container.name
        for container in all_containers
        if project_label in container.labels.get("com.docker.compose.project", "")
    ]
    write_log("INFO", f"Gefundene Container: {filtered_containers}")
    return filtered_containers


# =====================================
#          START/STOP CONTAINER
# =====================================


def container_stop(container, container_name: str, timeout: float = 60):
    """
    Stoppt den angegebenen Docker-Container und stellt sicher, dass er innerhalb der Timeout-Zeit den Status 'exited' erreicht.
        Die Funktion überprüft wiederholt den Status des Containers, bis 'exited' erreicht ist oder der Timeout überschritten wird.
    Returns:
        None
    Raises:
        ContainerStopError: Falls der Container nicht erfolgreich gestoppt werden kann.
    """
    container.stop()
    while timeout > 0:
        container.reload()
        if container.status == "exited":
            break
        time.sleep(0.5)
        timeout -= 0.5
    if container.status != "exited":
        write_log(
            "ERROR",
            f"Container '{container_name}' konnte nicht gestoppt werden, aktueller Status: {container.status}",
        )
        raise ContainerStopError(
            f"Container '{container_name}' konnte nicht gestoppt werden"
        )
    write_log("INFO", f"Container '{container_name}' erfolgreich gestoppt")


def container_start(container, container_name: str, timeout: float = 60):
    """
    Startet den angegebenen Docker-Container und stellt sicher, dass er innerhalb der Timeout-Zeit den Status 'running' erreicht.
        Die Funktion überprüft wiederholt den Status des Containers, bis 'running' erreicht ist oder der Timeout überschritten wird.
    Returns:
        None
    Raises:
        ContainerStartError: Falls der Container nicht erfolgreich gestartet werden kann.
    """
    container.start()
    while timeout > 0:
        container.reload()
        if container.status == "running":
            break
        time.sleep(0.5)
        timeout -= 0.5
    if container.status != "running":
        write_log(
            "ERROR",
            f"Container '{container_name}' konnte nicht gestartet werden, aktueller Status: {container.status}",
        )
        raise ContainerStartError(
            f"Container '{container_name}' konnte nicht gestartet werden"
        )
    write_log("INFO", f"Container '{container_name}' erfolgreich gestartet")


# =====================================
#          REGISTRY CHECK
# =====================================


def check_registry_images(images: List[str]) -> dict:
    """
    Prüft die Docker-Images in der Registry und extrahiert den "Version"-Label.
        Die Funktion ruft für jedes angegebene Image das Manifest und den zugehörigen Config-Blob ab,
        um den Version-Label zu ermitteln.
    Returns:
        dict: Ein Dictionary mit den Image-Namen als Schlüsseln und den zugehörigen Versionsinformationen sowie dem Manifest-Digest.
    Raises:
        ManifestError: Falls der Manifest-Aufruf fehlschlägt oder der Config-Digest nicht gefunden wird.
        ConfigBlobError: Falls der Version-Label im Config-Blob nicht gefunden wird.
        Exception: Bei anderen Fehlern.
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
            version_label = (
                config_blob.get("config", {}).get("Labels", {}).get("Version")
            )
            if version_label is None:
                raise ConfigBlobError("Kein Version-Label im Config-Blob gefunden")

            write_log("INFO", f"Image {image} hat Version: {version_label}")
            results[image] = {
                "version": version_label,
                "manifest_digest": config_digest,
            }
        except (ManifestError, ConfigBlobError) as e:
            write_log("ERROR", f"Fehler bei der Überprüfung von {image}: {str(e)}")
            results[image] = {"error": str(e)}
        except Exception as e:
            write_log(
                "ERROR", f"Unbekannter Fehler bei der Überprüfung von {image}: {str(e)}"
            )
            results[image] = {"error": str(e)}

    write_log("INFO", "Überprüfung der Registry-Images abgeschlossen")
    return {"images": results}


# =====================================
#           COMPOSE OPERATIONS
# =====================================


def restart_compose_environment() -> dict:
    """
    Startet die docker-compose Umgebung neu, indem zuerst 'docker-compose down' und anschließend 'docker-compose up -d' ausgeführt wird.
        Das Arbeitsverzeichnis (settings.COMPOSE_PATH) wird hierbei verwendet.
    Returns:
        dict: Ein Dictionary mit dem Status und dem Output des Neustarts.
    Raises:
        DockerComposeRestartError: Falls der Neustart der Umgebung fehlschlägt.
    """
    write_log("INFO", "Starte Neustart der docker-compose Umgebung")
    try:
        down_command = ["docker-compose", "down"]
        write_log(
            "INFO",
            f"Führe Befehl aus: {' '.join(down_command)} im Verzeichnis {settings.COMPOSE_PATH}",
        )
        subprocess.run(
            down_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=settings.COMPOSE_PATH,
        )

        up_command = ["docker-compose", "up", "-d"]
        write_log(
            "INFO",
            f"Führe Befehl aus: {' '.join(up_command)} im Verzeichnis {settings.COMPOSE_PATH}",
        )
        result = subprocess.run(
            up_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=settings.COMPOSE_PATH,
        )
        write_log("INFO", "Docker-compose Umgebung wurde erfolgreich neu gestartet")
        return {
            "status": "Docker-compose Umgebung wurde erfolgreich neu gestartet",
            "output": result.stdout,
        }
    except subprocess.CalledProcessError as e:
        write_log(
            "ERROR", f"Fehler beim Neustarten der docker-compose Umgebung: {e.stderr}"
        )
        raise DockerComposeRestartError(
            f"Neustart der docker-compose Umgebung fehlgeschlagen: {e.stderr}"
        )


# =====================================
#          UPDATE DOCKER IMAGES
# =====================================


def update_docker_images() -> dict:
    """
    Aktualisiert die Docker-Images mittels 'docker-compose pull' im definierten Arbeitsverzeichnis.
        Die Funktion zieht alle in settings.IMAGES angegebenen Images.
    Returns:
        dict: Ein Dictionary mit dem Status und dem Output des Update-Vorgangs.
    Raises:
        DockerImagesUpdateError: Falls der Update-Vorgang fehlschlägt.
    """
    write_log("INFO", "Starte Update der Docker-Images")
    try:
        pull_command = ["docker-compose", "pull"] + settings.IMAGES
        write_log(
            "INFO",
            f"Führe Befehl aus: {' '.join(pull_command)} im Verzeichnis {settings.COMPOSE_PATH}",
        )
        result = subprocess.run(
            pull_command,
            capture_output=True,
            text=True,
            check=True,
            cwd=settings.COMPOSE_PATH,
        )
        write_log("INFO", "Docker-Images wurden erfolgreich aktualisiert")
        return {
            "status": "Docker-Images wurden erfolgreich aktualisiert",
            "output": result.stdout,
        }
    except subprocess.CalledProcessError as e:
        write_log("ERROR", f"Fehler beim Update der Images: {e.stderr}")
        raise DockerImagesUpdateError(f"Update der Images fehlgeschlagen: {e.stderr}")


# =====================================
#         NEUE SUPPORT FUNCTIONS
# =====================================


def get_registry_images(images: List[str]) -> dict:
    """
    Ruft für jedes in der Liste angegebene Docker-Image die Versionsinformationen aus der Registry ab.
        Nutzt intern die Funktion check_registry_images, um Manifest- und Config-Blob-Daten abzurufen.
    Returns:
        dict: Ein Dictionary, in dem jedes Image einem Dictionary mit 'version' und 'manifest_digest' zugeordnet ist.
    """
    result = check_registry_images(images)
    return result.get("images", {})


def compare_image_versions(containers: list, registry_images: dict) -> dict:
    """
    Vergleicht die Versionsinformationen der aktuell laufenden Container-Images mit den in der Registry verfügbaren.
        Die Funktion ermittelt für jeden Container die aktuell verwendete Version (entweder über ein Label oder den Image-Tag)
        und vergleicht diese mit der in der Registry abgefragten Version.
    Returns:
        dict: Ein Dictionary, das für jeden Container den aktuellen Versionsstand und den in der Registry verfügbaren Versionsstand
              oder einen Fehler enthält.
    """
    updates = {}
    for container_name in containers:
        try:
            container = docker_client.containers.get(container_name)
            current_version = container.labels.get("Version")
            if not current_version and container.image.tags:
                tag = container.image.tags[0]
                if ":" in tag:
                    current_version = tag.split(":")[1]
            if container.image.tags:
                image_name = container.image.tags[0].split(":")[0]
            else:
                image_name = None

            if image_name and image_name in registry_images:
                registry_version = registry_images[image_name].get("version")
                if current_version != registry_version:
                    updates[container_name] = {
                        "current_version": current_version,
                        "available_version": registry_version,
                    }
        except Exception as e:
            updates[container_name] = {"error": str(e)}

    return updates


# =====================================
#          SUPPORT FUNCTIONS
# =====================================


def get_manifest(image: str, tag: str = "latest"):
    """
    Ruft das Manifest für das angegebene Docker-Image und Tag aus der Registry ab.
        Verwendet die GitLab Registry URL und die im Settings hinterlegten Zugangsdaten.
    Returns:
        dict: Das Manifest als JSON-Dictionary.
    Raises:
        Exception: Falls das Manifest nicht erfolgreich geladen werden kann.
    """
    manifest_url = f"{settings.GIT_REGISTRY}/v2/{image}/manifests/{tag}"
    headers = {
        "Accept": "application/vnd.docker.distribution.manifest.v2+json",
        "Authorization": f"Bearer {settings.GIT_PAT}",
    }
    write_log("INFO", f"Rufe Manifest für {image}:{tag} ab von {manifest_url}")
    response = requests.get(manifest_url, headers=headers)
    if response.status_code != 200:
        write_log(
            "ERROR",
            f"Fehler beim Laden des Manifests für {image}:{tag}. Status Code: {response.status_code}",
        )
        raise Exception(
            f"Manifest für {image}:{tag} konnte nicht geladen werden: {response.status_code}"
        )
    write_log("INFO", f"Manifest für {image}:{tag} erfolgreich geladen")
    return response.json()


def get_config_blob(image: str, digest: str):
    """
    Ruft den Config-Blob für das angegebene Docker-Image anhand des Digest aus der Registry ab.
        Nutzt die GitLab Registry URL und die im Settings hinterlegten Zugangsdaten.
    Returns:
        dict: Den Config-Blob als JSON-Dictionary.
    Raises:
        Exception: Falls der Config-Blob nicht erfolgreich geladen werden kann.
    """
    blob_url = f"{settings.GIT_REGISTRY}/v2/{image}/blobs/{digest}"
    headers = {"Authorization": f"Bearer {settings.GIT_PAT}"}
    write_log(
        "INFO", f"Rufe Config-Blob für {image} mit Digest {digest} ab von {blob_url}"
    )
    response = requests.get(blob_url, headers=headers)
    if response.status_code != 200:
        write_log(
            "ERROR",
            f"Fehler beim Laden des Config-Blobs für {image} (Digest: {digest}). Status Code: {response.status_code}",
        )
        raise Exception(
            f"Config-Blob für {image} (Digest: {digest}) konnte nicht geladen werden: {response.status_code}"
        )
    write_log("INFO", f"Config-Blob für {image} erfolgreich geladen")
    return response.json()
