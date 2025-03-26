# app/main.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app import app
from app.routes import auth, view, logging as log_routes, system

# Beispiel: Einbinden einer globalen Middleware
@app.middleware("http")
async def auth_middleware(request, call_next):
    allowed_paths = ["/login", "/logout"]
    if request.url.path.startswith("/static") or request.url.path in allowed_paths:
        return await call_next(request)
    
    session = request.cookies.get("session")
    if not session:
        if request.method == "GET":
            return RedirectResponse(url="/login")
    return await call_next(request)

# Routen einbinden
app.include_router(auth.router)
app.include_router(view.router)
app.include_router(log_routes.router)
app.include_router(system.router)
