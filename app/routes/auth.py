# app/routes/auth.py

from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from app.services.auth_service import authenticate_user
from app.utils.auth import get_current_user

router = APIRouter()


# =====================================
#              AUTH
# =====================================

@router.get("/me")
def get_logged_in_user(user: str = Depends(get_current_user)):
    """
    🔐 Gibt den aktuell angemeldeten Benutzer zurück.

    **Returns:**  
    - `200 OK` mit `{"username": "<name>"}`  
    - `401 Unauthorized`, wenn kein gültiges Cookie vorhanden ist.
    """
    return {"username": user}


@router.post("/login")
async def login(request: Request, response: Response):
    """
    🔐 Authentifiziert den Benutzer und setzt ein HTTP-only Session-Cookie.

    **Request Body:**  
    ```json
    {
      "username": "admin",
      "password": "pass"
    }
    ```

    **Returns:**  
    - `200 OK` bei Erfolg  
    - `401 Unauthorized` bei falschen Zugangsdaten
    """
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if authenticate_user(username, password):
        response = JSONResponse(content={"message": "Login erfolgreich"})
        response.set_cookie(
            key="session",
            value=username,
            httponly=True,
            samesite="lax", # oder 'strict' falls gewünscht
            secure=False # auf True setzen bei HTTPS
        )
        return response

    return JSONResponse(
        status_code=401,
        content={"detail": "Falscher Benutzername oder Passwort"}
    )


@router.get("/logout")
def logout():
    """
    🔐 Löscht das Session-Cookie.

    **Returns:**  
    - `200 OK` + leere Antwort
    """
    response = JSONResponse(content={"message": "Abgemeldet"})
    response.delete_cookie("session")
    return response
