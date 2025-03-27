#!/usr/bin/env python3
import time
import app.services.docker_service as docker_service
from app.config import settings

# Dummy-Implementierungen für get_manifest und get_config_blob,
# falls diese Funktionen in docker_service noch nicht implementiert sind.
def get_manifest(image):
    # Liefert ein Dummy-Manifest mit einem Platzhalter für den Digest.
    return {"config": {"digest": "dummy_digest"}}

def get_config_blob(image, digest):
    # Liefert ein Dummy Config-Blob mit einem Platzhalter für die Version.
    return {"config": {"Labels": {"Version": "dummy_version"}}}

# Monkey-Patching: Überschreibe ggf. die fehlenden Funktionen im Modul
docker_service.get_manifest = get_manifest
docker_service.get_config_blob = get_config_blob

def test_list_docker_containers():
    print("Teste list_docker_containers()...")
    try:
        containers = docker_service.list_docker_containers()
        print("Gefundene Container:", containers)
    except Exception as e:
        print("Fehler bei list_docker_containers:", e)

def test_check_registry_images():
    print("Teste check_registry_images()...")
    # Beispielhafte Image-Namen – passe diese bei Bedarf an deine Testumgebung an.
    test_images = ["myimage:latest", "anotherimage:1.0"]
    try:
        result = docker_service.check_registry_images(test_images)
        print("Ergebnis der Registry-Prüfung:", result)
    except Exception as e:
        print("Fehler bei check_registry_images:", e)

if __name__ == "__main__":
    test_list_docker_containers()
    # Eine kurze Pause, um die Ausgaben besser zu unterscheiden.
    time.sleep(1)
    test_check_registry_images()
