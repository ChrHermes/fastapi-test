# app/services/mock_data.py

from datetime import datetime


def mock_uptime():
    return {"days": 2, "hours": 4, "minutes": 35}


def mock_disk_usage():
    mock_disks = [
        {
            "label": "Medien",
            "path": "/Volumes/Medien",
            "used": "512.31 GB",
            "total": "1000.00 GB",
            "percent": 51.23,
        },
        {
            "label": "SD-Karte",
            "path": "/media/sd",
            "used": "7.81 GB",
            "total": "32.00 GB",
            "percent": 24.40,
        },
    ]

    return mock_disks


def mock_netbird_status():
    return {
        "daemon_version": "0.36.5",
        "cli_version": "0.36.5",
        "management": "Connected",
        "signal": "Connected",
        "relays": "3/3 Available",
        "nameservers": "1/1 Available",
        "fqdn": "ds.netbird.cloud",
        "netbird_ip": "100.72.234.206",
        "interface_type": "Userspace",
        "quantum_resistance": "false",
        "peers": "0/2 Connected",
    }


def mock_system_info():
    return {
        "hostname": "mocked-host",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
