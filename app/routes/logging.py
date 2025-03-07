# app/routes/logging.py
import os
import json
from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.services.log_service import write_log
from app.utils.auth import get_current_user

router = APIRouter()

class CustomLogEntry(BaseModel):
    message: str

LOG_FILE = os.path.join("logs", "logs.json")

@router.post("/log")
async def log_message(request: Request):
    data = await request.json()
    level = data.get("level", "INFO").upper()
    message = data.get("message", "")
    write_log(level, message)
    return {"status": "ok"}

@router.post("/log/reboot")
def log_button3(user: str = Depends(get_current_user)):
    write_log("INFO", "System wird neugestartet")
    return {"message": "System wird neugestartet"}

@router.post("/log/shutdown")
def log_button3(user: str = Depends(get_current_user)):
    write_log("INFO", "System wird heruntergefahren")
    return {"message": "System wird heruntergefahren"}

@router.post("/log/custom")
def log_custom(entry: CustomLogEntry, user: str = Depends(get_current_user)):
    """
    Nimmt einen benutzerdefinierten Logeintrag entgegen und schreibt ihn mit dem Log-Level "USER" ins Log.
    """
    if not entry.message.strip():
        return JSONResponse(content={"error": "Nachricht darf nicht leer sein."}, status_code=400)
    write_log("USER", entry.message)
    return {"message": f"Benutzereintrag wurde gespeichert: {entry.message}"}

@router.get("/logs")
def get_logs():
    if not os.path.exists(LOG_FILE):
        return JSONResponse(content={"logs": []})
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)
    return JSONResponse(content={"logs": logs})