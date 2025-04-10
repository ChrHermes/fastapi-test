import subprocess
import docker
import os
from datetime import datetime

from app.config import settings
from app.services.log_service import write_log

# ------------------------------
#    Docker Client Initialisierung
# ------------------------------

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None


# =====================================
#          SYSTEM
# ===================================== 

# -------------------------------------------
# Informationen einholen
# -------------------------------------------

def get_host_info():
    client = docker.from_env()
    info = client.info()
    return {
        info
        # "hostname": info.get("Name"),
        # "kernel": info.get("KernelVersion"),
        # "mem_total_gb": round(info.get("MemTotal") / (1024**3), 2),
        # "cpu_count": info.get("NCPU"),
        # "uptime": info.get("SystemTime"),  # begrenzt aussagekräftig
    }


def get_system_info():
    """
    Liefert Hostname und aktuelle Zeit als Dictionary.
    """
    hostname = os.uname().nodename if not settings.MOCK_MODE else "mocked-host"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"hostname": hostname, "time": now}


def get_uptime():
    """
    Gibt die Systemlaufzeit zurück.
    """
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
    except Exception:
        uptime_seconds = 123456 if settings.MOCK_MODE else 0

    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    return {"uptime": f"{days} Tage, {hours} Stunden"}


def get_load_average():
    """
    Gibt die Load Average für 1m, 5m, 15m zurück.
    """
    try:
        with open("/proc/loadavg", "r") as f:
            load1, load5, load15 = map(float, f.readline().split()[:3])
    except Exception:
        load1, load5, load15 = (2.97, 1.55, 0.96) if settings.MOCK_MODE else (0.0, 0.0, 0.0)

    return {
        "1m": round(load1, 2),
        "5m": round(load5, 2),
        "15m": round(load15, 2),
    }


def get_sd_usage():
    """
    Gibt den belegten Speicherplatz auf der root-Partition zurück.
    """
    try:
        stat = os.statvfs("/")
        total = stat.f_frsize * stat.f_blocks
        free = stat.f_frsize * stat.f_bfree
        used = total - free
    except Exception:
        total = 32 * 1024**3
        used = 7.8 * 1024**3 if settings.MOCK_MODE else 0

    percent = round((used / total) * 100, 2) if total > 0 else 0

    return {
        "used": f"{used / (1024**3):.1f} GB",
        "total": f"{total / (1024**3):.0f} GB",
        "percent": percent,
    }


def get_health_status():
    """
    Gibt eine Ampel-Bewertung zurück, basierend auf Load oder Speicher.
    """
    load = get_load_average()["1m"]
    sd = get_sd_usage()["percent"]

    if load > 2.5 or sd > 90:
        status = "error"
    elif load > 1.5 or sd > 75:
        status = "warn"
    else:
        status = "ok"

    return {"status": status}


# -------------------------------------------
# Aktive Eingriffe ins System
# -------------------------------------------
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
