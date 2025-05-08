import subprocess
import docker
import os
import re

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
#          DOCKER
# =====================================


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


# =====================================
#         SYSTEM /proc-basierend
# =====================================


def get_uptime() -> dict:
    """
    Liefert die Systemlaufzeit basierend auf /proc/uptime des Docker-Hosts.

    Returns:
        dict: `{ "success": bool, "days": int, "hours": int, "minutes": int }` oder Fehlerdetails.
    """
    try:
        with open(os.path.join(settings.HOST_PROC_PATH, "uptime"), "r") as f:
            uptime_seconds = float(f.readline().split()[0])
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return {"success": True, "days": days, "hours": hours, "minutes": minutes}
    except Exception as e:
        return {"success": False, "days": 0, "hours": 0, "minutes": 0, "error": str(e)}


def get_load_average() -> dict:
    """
    Liefert die Load Average des Systems über 1, 5 und 15 Minuten.

    Returns:
        dict: `{ "success": bool, "1m": float, "5m": float, "15m": float }` oder Fehlerdetails.
    """
    try:
        with open(os.path.join(settings.HOST_PROC_PATH, "loadavg"), "r") as f:
            load1, load5, load15 = map(float, f.readline().split()[:3])
        return {
            "success": True,
            "1m": round(load1, 2),
            "5m": round(load5, 2),
            "15m": round(load15, 2),
        }
    except Exception as e:
        return {"success": False, "1m": 0.0, "5m": 0.0, "15m": 0.0, "error": str(e)}


def get_hostname() -> dict:
    """
    Gibt den Hostnamen des Docker-Hosts zurück.

    Returns:
        dict: `{ "success": bool, "hostname": str }` oder Fehlerdetails.
    """
    try:
        with open(
            os.path.join(settings.HOST_PROC_PATH, "sys/kernel/hostname"), "r"
        ) as f:
            hostname = f.read().strip()
        return {"success": True, "hostname": hostname}
    except Exception as e:
        return {"success": False, "hostname": "", "error": str(e)}


def get_memory_info() -> dict:
    """
    Liefert RAM-Informationen über den Docker-Host in Kilobyte (kB).

    Returns:
        dict:
            {
                "success": True,
                "total_kb": int,
                "used_kb": int,
                "buffers_kb": int,
                "cached_kb": int,
                "free_kb": int,
                "percent_used": float
            }
            oder bei Fehler:
            {
                "success": False,
                "error": str
            }
    """
    try:
        meminfo = {}
        with open(os.path.join(settings.HOST_PROC_PATH, "meminfo"), "r") as f:
            for line in f:
                key, value = line.split(":")
                meminfo[key.strip()] = int(value.strip().split()[0])  # in kB

        total_kb = meminfo.get("MemTotal", 0)
        free_kb = meminfo.get("MemFree", 0)
        buffers_kb = meminfo.get("Buffers", 0)
        cached_kb = meminfo.get("Cached", 0)

        used_kb = total_kb - (buffers_kb + cached_kb + free_kb)

        return {
            "success": True,
            "total_kb": total_kb,
            "used_kb": used_kb,
            "buffers_kb": buffers_kb,
            "cached_kb": cached_kb,
            "free_kb": free_kb,
            "percent_used": round((used_kb / total_kb) * 100, 2) if total_kb else 0.0
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_network_status(interface: str = "eth0") -> dict:
    """
    Liefert den Netzwerkstatus des Hosts für ein bestimmtes Interface.

    Liest Informationen aus:
      - /host/sys/class/net/<interface>/
      - /host/proc/net/fib_trie

    Args:
        interface (str): Netzwerkinterface (z. B. "eth0")

    Returns:
        dict mit Interface-Daten wie MAC, Status, empfangene/gesendete Bytes und IP-Adresse.
    """
    try:
        base_path = os.path.join(settings.HOST_SYS_CLASS_NET_PATH, interface)

        def read_file(filename: str) -> str:
            with open(os.path.join(base_path, filename), "r") as f:
                return f.read().strip()

        operstate = read_file("operstate")
        mac = read_file("address")
        rx_bytes = int(read_file("statistics/rx_bytes"))
        tx_bytes = int(read_file("statistics/tx_bytes"))

        # IP-Adresse aus fib_trie ermitteln
        ip_address = ""
        with open(os.path.join(settings.HOST_PROC_PATH, "net/fib_trie"), "r") as f:
            block = ""
            for line in f:
                if line.startswith(" " * 6):  # neue Zeile mit IP-Block
                    block = line.strip()
                if interface in line and re.match(r"^\d+\.\d+\.\d+\.\d+$", block):
                    ip_address = block
                    break

        return {
            "success": True,
            "interface": interface,
            "operstate": operstate,
            "mac": mac,
            "ip": ip_address,
            "rx_bytes": rx_bytes,
            "tx_bytes": tx_bytes,
        }

    except Exception as e:
        return {
            "success": False,
            "interface": interface,
            "operstate": "unknown",
            "mac": "",
            "ip": "",
            "rx_bytes": 0,
            "tx_bytes": 0,
            "error": str(e),
        }


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


# =====================================
#         SYSTEM binary-basierend
# =====================================


def get_disk_usage():
    """
    Gibt die Speicherplatznutzung aller konfigurierten Pfade als Liste zurück.
    Werte werden sowohl in Bytes als auch menschenlesbar (fmt_*) zurückgegeben.
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

            results.append(
                {
                    "label": label,
                    "mount": path,
                    "byte_used": used,
                    "byte_free": free,
                    "byte_total": total,
                    "fmt_used": format_bytes(used),
                    "fmt_free": format_bytes(free),
                    "fmt_total": format_bytes(total),
                    "percent": percent,
                }
            )
        except Exception as e:
            results.append(
                {
                    "label": label,
                    "mount": path,
                    "error": str(e),
                }
            )

    return results


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
