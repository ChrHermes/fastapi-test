from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging

app = FastAPI()
security = HTTPBasic()

# Logger einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Einfache Benutzerauthentifizierung
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "admin" and credentials.password == "password":
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

# API-Endpunkte
@app.post("/log/button1")
def log_button1(user: str = Depends(get_current_user)):
    logger.info("Button 1 wurde geklickt")
    return {"message": "Button 1 ausgelöst"}

@app.post("/log/button2")
def log_button2(user: str = Depends(get_current_user)):
    logger.info("Button 2 wurde geklickt")
    return {"message": "Button 2 ausgelöst"}

# Statische Dateien für das UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_page(user: str = Depends(get_current_user)):
    return FileResponse("static/index.html")