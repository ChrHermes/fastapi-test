# app/routes/logging.py
import os
import json
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.services.log_service import write_log
from app.utils.auth import get_current_user

router = APIRouter()

LOG_FILE = os.path.join("logs", "logs.json")

@router.post("/log")
async def log_message(request: Request):
    data = await request.json()
    level = data.get("level", "INFO").upper()
    message = data.get("message", "")
    write_log(level, message)
    return {"status": "ok"}

@router.get("/logs")
def get_logs():
    if not os.path.exists(LOG_FILE):
        return JSONResponse(content={"logs": []})
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)
    return JSONResponse(content={"logs": logs})

@router.post("/log/button2")
def log_button2(user: str = Depends(get_current_user)):
    write_log("INFO", "Button 2 wurde geklickt")
    return {"message": "Button 2 wurde geklickt"}

@router.post("/log/button3")
def log_button3(user: str = Depends(get_current_user)):
    write_log("INFO", "Button 3 wurde geklickt")
    return {"message": "Button 3 wurde geklickt"}

@router.post("/log/button4")
def log_button3(user: str = Depends(get_current_user)):
    write_log("INFO", "Button 4 wurde geklickt")
    return {"message": "Button 4 wurde geklickt"}