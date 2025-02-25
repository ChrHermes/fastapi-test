# app/routes/view.py
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/")
def serve_page(user: str = Depends(get_current_user)):
    return FileResponse("static/index.html")

@router.get("/protected")
async def protected_page(user: str = Depends(get_current_user)):
    return {"message": f"Willkommen, {user}!"}
