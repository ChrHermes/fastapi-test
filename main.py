import os
import json
import docker
import logging
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

# Initialisierung
app = FastAPI()
load_dotenv()

# Statische Dateien bereitstellen
app.mount("/static", StaticFiles(directory="static"), name="static")

# Umgebungsvariablen
USERS = {os.getenv("ADMIN_USER"): os.getenv("ADMIN_PASS")}
BACKEND_CONTAINER = os.getenv("BACKEND_CONTAINER_NAME", "backend")
DB_PATH = os.getenv("DB_PATH", "/data/gcn.db")

# Docker-Client initialisieren
docker_available = False
try:
    docker_client = docker.from_env()
    docker_available = True
except Exception as e:
    print(f"Docker client konnte nicht initialisiert werden: {e}")
    docker_client = No

# Log-Datei Pfad
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "logs.json")
os.makedirs(LOG_DIR, exist_ok=True)

# Stelle sicher, dass das Log-Verzeichnis existiert
os.makedirs(LOG_DIR, exist_ok=True)

# Setup Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# =========================================================================
# ----- METHODEN ----------------------------------------------------------
# =========================================================================

# Authentifizierungsprüfung
def get_current_user(request: Request): 
    session = request.cookies.get("session")
    if session and session in USERS:
        return session
    return RedirectResponse(url="/login")

def reset_database():
    """Platzhalter-Funktion für den späteren Datenbank-Reset."""
    logger.info("Datenbank-Reset gestartet (noch nicht implementiert).")

def write_log(level, message):
    """Speichert Log-Meldung in einer JSON-Datei mit Zeitstempel."""
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

    logger.log(getattr(logging, level), message)

# =========================================================================
# ----- MIDDLEWARE --------------------------------------------------------
# =========================================================================

# Middleware: Blockiere nicht eingeloggte Nutzer
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    allowed_paths = ["/login", "/logout"]
    
    # Statische Dateien immer erlauben
    if request.url.path.startswith("/static") or request.url.path in allowed_paths:
        return await call_next(request)

    # Prüfe Session-Cookie
    session = request.cookies.get("session")
    if not session or session not in USERS:
        if request.method == "GET":
            return RedirectResponse(url="/login")  # Nur GET-Anfragen umleiten
        return JSONResponse(content={"detail": "Nicht autorisiert"}, status_code=401)

    return await call_next(request)

# =========================================================================
# ----- ROUTEN ------------------------------------------------------------
# =========================================================================

# ----- MAIN --------------------------------------------------------------
@app.get("/")
def serve_page(user: str = Depends(get_current_user)):
    return FileResponse("static/index.html")

# ----- LOGIN -------------------------------------------------------------
@app.get("/login")
async def login_page():
    return FileResponse("static/login.html")

@app.post("/login")
async def login(request: Request, response: Response):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if USERS.get(username) == password:
        response = RedirectResponse(url="/static/index.html", status_code=303)
        response.set_cookie(key="session", value=username, httponly=True)
        logger.info(f"Erfolgreicher Login: {username}")
        return response
    else:
        logger.warning(f"Fehlgeschlagener Login-Versuch: {username}")
        return JSONResponse(content={"detail": "Falscher Benutzername oder Passwort"}, status_code=401)

# ----- LOGOUT ------------------------------------------------------------
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session")
    return response

# Geschützte Seite
@app.get("/protected")
async def protected_page(user: str = Depends(get_current_user)):
    return {"message": f"Willkommen, {user}!"}

# ----- LOGGING -----------------------------------------------------------
@app.post("/log")
async def log_message(request: Request):
    """Fügt eine Log-Nachricht mit Level hinzu."""
    data = await request.json()
    level = data.get("level", "INFO").upper()
    message = data.get("message", "")

    if level not in ["INFO", "WARN", "ERROR"]:
        level = "INFO"

    write_log(level, message)
    return {"status": "ok"}

@app.get("/logs")
def get_logs():
    """Lädt Logs aus der JSON-Datei."""
    if not os.path.exists(LOG_FILE):
        return JSONResponse(content={"logs": []})

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)

    return JSONResponse(content={"logs": logs})

@app.post("/log/btnGC")
def log_button_gc(user: str = Depends(get_current_user)):
    """Platzhalter für eine zukünftige Datenbank-Reset-Funktion."""
    reset_database()
    log_message = "Datenbank wurde zurückgesetzt"
    logger.info(log_message)
    return {"message": log_message}

@app.post("/log/button2")
def log_button2(user: str = Depends(get_current_user)):
    log_message = "Button 2 wurde geklickt"
    logger.info(log_message)
    return {"message": log_message}

@app.post("/log/db-reset")
def log_db_reset():
    """Loggt einen Datenbank-Reset."""
    write_log("INFO", "Datenbankrücksetzung angefordert")
    write_log("WARN", "Datenbank zurückgesetzt")
    return {"message": "Reset-Log geschrieben"}

# ----- SYSTEM ------------------------------------------------------------

@app.post("/shutdown")
def shutdown_system():
    write_log("WARN", "System wird heruntergefahren")
    # subprocess.Popen(["shutdown", "-h", "now"])
    return "System wird heruntergefahren..."

@app.post("/reset-db")
def reset_database():
    try:
        # Backend-Container stoppen
        container = docker_client.containers.get(BACKEND_CONTAINER)
        container.stop()

        # DB & Cache löschen
        for file in [DB_PATH, f"{DB_PATH}-wal", f"{DB_PATH}-journal"]:
            if os.path.exists(file):
                os.remove(file)

        write_log("WARN", "Datenbank wurde erfolgreich zurückgesetzt")
        return "Datenbank wurde erfolgreich zurückgesetzt"
    
    except Exception as e:
        write_log("ERROR", f"Fehler beim Zurücksetzen der DB: {str(e)}")
        return f"Fehler: {str(e)}"