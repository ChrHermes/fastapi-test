import subprocess
import docker
import os
import re
from datetime import datetime

from app.config import settings
from app.services.log_service import write_log
from app.utils.common import format_bytes

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
    print(info)  # Debug-Ausgabe
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
    Gibt die Systemlaufzeit als Klartext zurück, z.B. „3 Tage, 5 Stunden“.

    **Nutzt:** `uptime` Befehl im Host-System via Subprocess
    """
    try:
        output = subprocess.run(
            ["chroot", "/host", "/usr/bin/uptime"],
            # shell=True,
            capture_output=True,
            text=True,
            check=True,
        )
        # Beispielausgabe: " 12:01:49 up 3 days, 5:32,  3 users,  load average: 0.35, 0.31, 0.30"
        match = re.search(r"up\s+(\d+)\s+days?,\s+(\d+):(\d+)", output)
        if match:
            days = int(match.group(1))
            hours = int(match.group(2))
            minutes = int(match.group(3))
        else:
            # Fallback, falls keine Tage erwähnt sind (z.B. "up 3:45")
            match = re.search(r"up\s+(\d+):(\d+)", output)
            if match:
                days = 0
                hours = int(match.group(1))
                minutes = int(match.group(2))
            else:
                days, hours, minutes = 0, 0, 0  # Fehlerfall

        return {"days": days, "hours": hours, "minutes": minutes}
    except Exception as e:
        return {"uptime": "unbekannt", "error": str(e)}


def get_load_average():
    """
    Gibt die Load Average für 1m, 5m, 15m zurück.
    """
    try:
        with open("/proc/loadavg", "r") as f:
            load1, load5, load15 = map(float, f.readline().split()[:3])
    except Exception:
        load1, load5, load15 = (
            (2.97, 1.55, 0.96) if settings.MOCK_MODE else (0.0, 0.0, 0.0)
        )

    return {
        "1m": round(load1, 2),
        "5m": round(load5, 2),
        "15m": round(load15, 2),
    }


def get_disk_usage():
    """
    Gibt die Speicherplatznutzung aller konfigurierten Pfade als Liste zurück.
    Werte werden als Bytes gesammelt und zusätzlich menschenlesbar formatiert.
    """
    results = []

    for path_entry in settings.DISK_PATHS:
        path = path_entry.get("path")
        label = path_entry.get("label", path)
        try:
            stat = os.statvfs(path)
            total = stat.f_frsize * stat.f_blocks
            free = stat.f_frsize * stat.f_bfree
            used = total - free
            percent = round((used / total) * 100, 2) if total > 0 else 0

            results.append({
                "label": label,
                "mount": path,
                "used_bytes": used,
                "total_bytes": total,
                "percent": percent,
                "used": format_bytes(used),
                "total": format_bytes(total),
            })
        except Exception as e:
            results.append({
                "label": label,
                "mount": path,
                "error": str(e),
            })

    return results



# def get_health_status():
#     """
#     Gibt eine Ampel-Bewertung zurück, basierend auf Load oder Speicher.
#     """
#     load = get_load_average()["1m"]
#     sd = get_sd_usage()["percent"]

#     if load > 2.5 or sd > 90:
#         status = "error"
#     elif load > 1.5 or sd > 75:
#         status = "warn"
#     else:
#         status = "ok"

#     return {"status": status}


def get_netbird_status():
    """
    Parst den Output von `netbird status` und gibt relevante Werte als Dict zurück.
    """
    try:
        raw = subprocess.check_output(["netbird", "status"], text=True)
        lines = raw.strip().splitlines()
        data = {}

        for line in lines:
            if ": " in line:
                key, val = line.split(": ", 1)
                key = key.strip().lower().replace(" ", "_")
                data[key] = val.strip()

        # Beispielhafte Umbenennung für UI-Zwecke
        return {
            "version": data.get("cli_version"),
            "status": data.get("management", "Unbekannt"),
            "signal": data.get("signal"),
            "fqdn": data.get("fqdn"),
            "ip": data.get("netbird_ip", "").split("/")[0],
            "connected_peers": data.get("peers_count"),
            "interface": data.get("interface_type"),
        }
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}


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
            ["poweroff", "-d", str(delay_seconds)], capture_output=True, text=True
        )
        write_log(
            "INFO", f"Poweroff-Kommando ausgeführt, Return Code: {result.returncode}"
        )
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
            ["reboot", "-d", str(delay_seconds)], capture_output=True, text=True
        )
        write_log(
            "INFO", f"Reboot-Kommando ausgeführt, Return Code: {result.returncode}"
        )
        return result.returncode
    except Exception as e:
        write_log("ERROR", f"Fehler beim Neustart: {str(e)}")
        return -1
