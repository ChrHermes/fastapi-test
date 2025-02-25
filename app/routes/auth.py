# app/routes/auth.py
import os
from fastapi import APIRouter, Request, Depends, Response, HTTPException
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from app.utils.auth import get_current_user

router = APIRouter()

USERS = {os.getenv("ADMIN_USER"): os.getenv("ADMIN_PASS")}

@router.get("/login")
async def login_page():
    return FileResponse("static/login.html")

@router.post("/login")
async def login(request: Request, response: Response):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    
    if USERS.get(username) == password:
        response = RedirectResponse(url="/static/index.html", status_code=303)
        response.set_cookie(key="session", value=username, httponly=True)
        return response
    else:
        return JSONResponse(content={"detail": "Falscher Benutzername oder Passwort"}, status_code=401)

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session")
    return response
