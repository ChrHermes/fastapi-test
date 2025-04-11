# app/utils/auth.py

from fastapi import Request,HTTPException, status
import os

USERS = {os.getenv("ADMIN_USER"): os.getenv("ADMIN_PASS")}

def get_current_user(request: Request):
    session = request.cookies.get("session")
    if session and session in USERS:
        return session
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
