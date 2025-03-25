# ------------------------------
#    Eigene Ausnahmeklassen
# ------------------------------
class DatabaseResetError(Exception):
    """Basisfehler beim Zurücksetzen der Datenbank."""
    pass

class DockerClientNotAvailableError(DatabaseResetError):
    """Fehler: Docker-Client ist nicht verfügbar."""
    pass

class ContainerNotFoundError(DatabaseResetError):
    def __init__(self, message: str, container_id: str, additional_info: dict = None):
        super().__init__(message)
        self.container_id = container_id
        self.additional_info = additional_info

class ContainerStopError(DatabaseResetError):
    """Fehler: Der Container konnte nicht gestoppt werden."""
    pass

class ContainerStartError(DatabaseResetError):
    """Fehler: Der Container konnte nicht gestartet werden."""
    pass