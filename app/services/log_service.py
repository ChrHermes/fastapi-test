# app/services/log_service.py
import os
import json
import logging
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "logs.json")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def write_log(level, message):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    log_entry = {"timestamp": timestamp, "level": level, "message": message}
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(log_entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    logger.log(getattr(logging, level, logging.INFO), message)

def reset_database_placeholder():
    logger.info("Datenbank-Reset gestartet (noch nicht implementiert).")
