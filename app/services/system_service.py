# app/services/system_service.py

import time
import subprocess

from app.services.log_service import write_log

# =====================================
#          SYSTEM
# ===================================== 

def delayed_shutdown(delay_seconds: int):
    time.sleep(delay_seconds)
    try:
        subprocess.run(["poweroff"], check=True)
    except Exception as e:
        write_log("ERROR", f"Fehler beim Herunterfahren: {str(e)}")

def delayed_reboot(delay_seconds: int):
    time.sleep(delay_seconds)
    try:
        subprocess.run(["reboot"], check=True)
    except Exception as e:
        write_log("ERROR", f"Fehler beim Neustart: {str(e)}")
