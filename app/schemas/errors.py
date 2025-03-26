# app/schemas/errors.py

# ------------------------------
#    DATABASE
# ------------------------------

class DatabaseResetError(Exception):
    """Basisfehler beim Zurücksetzen der Datenbank."""
    pass


class DatabaseInfoError(Exception):
    """Basisfehler beim Zurücksetzen der Datenbank."""
    pass


# ------------------------------
#    DOCKER
# ------------------------------

class DockerServiceError(Exception):
    """Basisklasse für alle Docker-bezogenen Fehler."""
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


class RegistryCheckError(DockerServiceError):
    """Allgemeiner Fehler bei der Überprüfung der Registry-Images."""
    pass


class ManifestError(DockerServiceError):
    """Fehler, wenn im Manifest kein gültiger Config-Digest gefunden wurde."""
    pass


class ConfigBlobError(DockerServiceError):
    """Fehler, wenn der Config-Blob nicht abgerufen werden konnte oder die erwarteten Informationen fehlen."""
    pass

