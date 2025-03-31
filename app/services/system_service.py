import subprocess

from app.config import settings
from app.services.log_service import write_log

# =====================================
#          SYSTEM
# ===================================== 

def delayed_shutdown(delay_seconds: int):
    if settings.MOCK_MODE:
        write_log("INFO", "Shutdown wird übersprungen, da MOCK_MODE aktiviert ist.")
        return 0  # Kein echter Shutdown, daher Rückgabewert 0
    try:
        # Übergabe des Delays direkt an den poweroff-Befehl mit dem -d Parameter
        result = subprocess.run(
            ["poweroff", "-d", str(delay_seconds)],
            capture_output=True,
            text=True
        )
        write_log("INFO", f"Poweroff-Kommando ausgeführt, Return Code: {result.returncode}")
        return result.returncode
    except Exception as e:
        write_log("ERROR", f"Fehler beim Herunterfahren: {str(e)}")
        return -1

def delayed_reboot(delay_seconds: int):
    if settings.MOCK_MODE:
        write_log("INFO", "Reboot wird übersprungen, da MOCK_MODE aktiviert ist.")
        return 0
    try:
        # Übergabe des Delays direkt an den reboot-Befehl mit dem -d Parameter
        result = subprocess.run(
            ["reboot", "-d", str(delay_seconds)],
            capture_output=True,
            text=True
        )
        write_log("INFO", f"Reboot-Kommando ausgeführt, Return Code: {result.returncode}")
        return result.returncode
    except Exception as e:
        write_log("ERROR", f"Fehler beim Neustart: {str(e)}")
        return -1
