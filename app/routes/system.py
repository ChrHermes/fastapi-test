# app/routes/system.py

from fastapi import APIRouter, Depends, BackgroundTasks

from app.config import settings
from app.services.log_service import write_log
from app.services import system_service
from app.utils.auth import get_current_user

router = APIRouter()


# =====================================
#          SYSTEM
# ===================================== 

# -------------------------------------------
# Informationen einholen
# -------------------------------------------
@router.get("/system/info")
def get_system_info(user: str = Depends(get_current_user)):
    """
    🖥️ **Allgemeine Systeminformationen**

    Liefert grundlegende Informationen wie Hostname und aktuelle Systemzeit.

    **Returns:** dict mit `hostname`, `time`
    """
    return system_service.get_system_info()


@router.get("/system/uptime")
def get_system_uptime(user: str = Depends(get_current_user)):
    """
    ⏱️ **Laufzeit des Systems**

    Gibt zurück, wie lange das System bereits läuft.

    **Returns:** dict mit `uptime` (z.B. "3 Tage, 4 Stunden")
    """
    return system_service.get_uptime()


@router.get("/system/loadavg")
def get_load_average(user: str = Depends(get_current_user)):
    """
    📊 **Systemlast (Load Average)**

    Liefert die durchschnittliche Systemlast über 1, 5 und 15 Minuten.

    **Returns:** dict mit `1m`, `5m`, `15m`
    """
    return system_service.get_load_average()


@router.get("/system/sd")
def get_sd_usage(user: str = Depends(get_current_user)):
    """
    💾 **Nutzung der SD-Karte**

    Gibt Informationen zur Speicherbelegung der SD-Karte zurück.

    **Returns:** dict mit `used`, `total`, `percent`
    """
    return system_service.get_sd_usage()


@router.get("/system/health")
def get_system_health(user: str = Depends(get_current_user)):
    """
    🟢 **Systemgesundheit**

    Bewertet den Gesamtzustand des Systems (z.B. Last, Speicher, Services).

    **Returns:** dict mit `status` (z.B. `"ok"`, `"warn"`, `"error"`)
    """
    return system_service.get_health_status()


@router.get("/system/summary")
def get_system_summary(user: str = Depends(get_current_user)):
    """
    🧩 **Komplette Systemübersicht**

    Liefert eine zusammengefasste Antwort mit allen verfügbaren Systemdaten:
    - Hostname, Zeit
    - Uptime, Loadavg
    - Speicher, Status

    **Returns:** dict mit allen Teildaten als Sub-Objekte.
    """
    return {
        "info": system_service.get_system_info(),
        "uptime": system_service.get_uptime(),
        "load": system_service.get_load_average(),
        "sd": system_service.get_sd_usage(),
        "health": system_service.get_health_status()
    }


# -------------------------------------------
# Aktive Eingriffe ins System
# -------------------------------------------
@router.post("/system/shutdown")
def shutdown_system(background_tasks: BackgroundTasks, user: str = Depends(get_current_user)):
    """
    🚫 **Fährt das System herunter**

    Startet eine verzögerte Herunterfahrsequenz im Hintergrund.

    - 🔧 Die Verzögerungszeit ist über die Konstante `settings.DELAY_SHUTDOWN` konfigurierbar.
    - 🪵 Der Vorgang wird mit dem Log-Level `WARN` dokumentiert.
    - 🧵 Die Ausführung erfolgt über einen Hintergrund-Task (`delayed_shutdown`).

    **Args:**
    - `background_tasks` (BackgroundTasks): Mechanismus für parallele Aufgaben in FastAPI.
    - `user` (str): Authentifizierter Benutzer (über `Depends(get_current_user)`).

    **Returns:**
    - `dict`: Nachricht über die geplante Herunterfahraktion.
    """
    write_log("WARN", f"Herunterfahren wird in {settings.DELAY_SHUTDOWN} Sekunden eingeleitet")
    background_tasks.add_task(system_service.delayed_shutdown, settings.DELAY_SHUTDOWN)
    return {"message": f"Herunterfahren wird in {settings.DELAY_SHUTDOWN} Sekunden eingeleitet"}


@router.post("/system/reboot")
def reboot_system(background_tasks: BackgroundTasks, user: str = Depends(get_current_user)):
    """
    🔁 **Startet einen Systemneustart**

    Startet eine verzögerte Neustartsequenz im Hintergrund.

    - 🔧 Die Verzögerungszeit ist über die Konstante `settings.DELAY_REBOOT` konfigurierbar.
    - 🪵 Der Vorgang wird mit dem Log-Level `WARN` dokumentiert.
    - 🧵 Die Ausführung erfolgt über einen Hintergrund-Task (`delayed_reboot`).

    **Args:**
    - `background_tasks` (BackgroundTasks): Mechanismus für parallele Aufgaben in FastAPI.
    - `user` (str): Authentifizierter Benutzer (über `Depends(get_current_user)`).

    **Returns:**
    - `dict`: Nachricht über die geplante Neustartaktion.
    """
    write_log("WARN", f"Neustart wird in {settings.DELAY_REBOOT} Sekunden eingeleitet")
    background_tasks.add_task(system_service.delayed_reboot, settings.DELAY_REBOOT)
    return {"message": f"Neustart wird in {settings.DELAY_REBOOT} Sekunden eingeleitet"}
