# app/services/auth_service.py

from app.config import settings

def authenticate_user(username: str, password: str) -> bool:
    """
    Überprüft, ob der übergebene Benutzername und das Passwort den
    im Config-Modul definierten Zugangsdaten entsprechen.
    """
    return username == settings.ADMIN_USER and password == settings.ADMIN_PASS
