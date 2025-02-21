import os
from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import logging

# Initialisierung
app = FastAPI()
load_dotenv()

# Statische Dateien bereitstellen
app.mount("/static", StaticFiles(directory="static"), name="static")

# Nutzerverwaltung
USERS = {os.getenv("ADMIN_USER"): os.getenv("ADMIN_PASS")}

# Log-Datei Pfad
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "actions.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Stelle sicher, dass das Log-Verzeichnis existiert
os.makedirs(LOG_DIR, exist_ok=True)

# Logger einrichten (Datei- und Konsolen-Logging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
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
@app.get("/logs")
def get_logs(user: str = Depends(get_current_user)):
    """Lädt alle bisherigen Log-Meldungen aus der Datei."""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.readlines()
        return JSONResponse(content={"logs": logs})
    except FileNotFoundError:
        return JSONResponse(content={"logs": []})

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
