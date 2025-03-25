import docker
import time

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
#          DATABASE
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