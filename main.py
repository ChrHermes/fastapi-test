import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel
import logging

# Initialisierung
app = FastAPI()
security = HTTPBasic()
load_dotenv()

# Nutzerverwaltung
USERS = {os.getenv("ADMIN_USER"): os.getenv("ADMIN_PASS")}

class LoginData(BaseModel):
    username: str
    password: str

# Log-Datei Pfad
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "actions.log")

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

# Authentifizierung
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "admin" and credentials.password == "password":
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

# Statische Dateien bereitstellen
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_page(user: str = Depends(get_current_user)):
    return FileResponse("static/index.html")

@app.get("/login")
async def login_page():
    return FileResponse("static/login.html")

# API-Endpunkte
@app.post("/login")
async def login(data: LoginData):
    if USERS.get(data.username) == data.password:
        logger.info(f"Erfolgreicher Login: {data.username}")
        return JSONResponse(content={"message": "Login erfolgreich"}, status_code=200)
    else:
        logger.warning(f"Fehlgeschlagener Login-Versuch: {data.username}")
        raise HTTPException(status_code=401, detail="Falscher Benutzername oder Passwort")

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

@app.post("/log/button3")
def log_button2(user: str = Depends(get_current_user)):
    log_message = "Button 3 wurde geklickt"
    logger.info(log_message)
    return {"message": log_message}

@app.post("/log/button4")
def log_button2(user: str = Depends(get_current_user)):
    log_message = "Button 4 wurde geklickt"
    logger.info(log_message)
    return {"message": log_message}

@app.get("/logs")
def get_logs(user: str = Depends(get_current_user)):
    """Lädt alle bisherigen Log-Meldungen aus der Datei."""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.readlines()
        return JSONResponse(content={"logs": logs})
    except FileNotFoundError:
        return JSONResponse(content={"logs": []})

def reset_database():
    """Platzhalter-Funktion für den späteren Datenbank-Reset."""
    logger.info("Datenbank-Reset gestartet (noch nicht implementiert).")