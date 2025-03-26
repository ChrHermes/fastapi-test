# app/routes/auth.py

from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse

from app.services.auth_service import authenticate_user
from app.config import settings
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/login")
async def login_page():
    """
    Liefert die Login-Seite aus dem static-Verzeichnis.
    """
    return FileResponse("static/login.html")

@router.post("/login")
async def login(request: Request, response: Response):
    """
    Authentifiziert den Benutzer anhand der übermittelten JSON-Daten.
    Bei erfolgreicher Authentifizierung wird der Benutzer auf die Startseite
    weitergeleitet und ein HTTP-Only-Cookie gesetzt.
    """
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    
    if authenticate_user(username, password):
        redirect_response = RedirectResponse(url="/static/index.html", status_code=303)
        redirect_response.set_cookie(key="session", value=username, httponly=True)
        return redirect_response
    else:
        return JSONResponse(content={"detail": "Falscher Benutzername oder Passwort"}, status_code=401)

@router.get("/logout")
async def logout():
    """
    Löscht das Session-Cookie und leitet den Benutzer zurück zur Login-Seite.
    """
    redirect_response = RedirectResponse(url="/login", status_code=303)
    redirect_response.delete_cookie("session")
    return redirect_response
