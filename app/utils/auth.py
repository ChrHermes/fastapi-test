# app/utils/auth.py

from fastapi import Request
from fastapi.responses import RedirectResponse
import os

USERS = {os.getenv("ADMIN_USER"): os.getenv("ADMIN_PASS")}

def get_current_user(request: Request):
    session = request.cookies.get("session")
    if session and session in USERS:
        return session
    return RedirectResponse(url="/login")


# TODO: TokenAuth testen

# from fastapi import Depends, HTTPException, Request
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jwt, JWTError
# import os

# SECRET_KEY = os.getenv("JWT_SECRET", "super-secret")
# ALGORITHM = "HS256"

# security = HTTPBearer()

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload  # z.B. {"sub": "user", "role": "admin"}
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Ungültiger oder abgelaufener Token")
