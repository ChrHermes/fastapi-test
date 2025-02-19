# FastAPI Test

## PyCharm

1. Öffne “Run Configurations”
   1. Gehe zu Run → Edit Configurations.
   1. Falls keine Konfiguration existiert, klicke auf + (Add new configuration) und wähle Python. 
1. Ändere die Einstellungen
   1. Module: `uvicorn`
   2. Parameters: `main:app --reload`
   3. Python interpreter: Wähle den Interpreter deiner virtuellen Umgebung (venv).
1. Speichern und ausführen
