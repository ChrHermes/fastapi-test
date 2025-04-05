# app/routes/system.py

from fastapi import APIRouter, Depends, BackgroundTasks

from app.config import settings
from app.services.log_service import write_log
from app.services.system_service import delayed_reboot, delayed_shutdown
from app.utils.auth import get_current_user

router = APIRouter()


# =====================================
#          SYSTEM
# ===================================== 

@router.post("/system/shutdown")
def shutdown_system(background_tasks: BackgroundTasks, user: str = Depends(get_current_user)):
    write_log("WARN", f"Herunterfahren wird in {settings.DELAY_SHUTDOWN} Sekunden eingeleitet")
    background_tasks.add_task(delayed_shutdown, settings.DELAY_SHUTDOWN)
    return {"message": f"Herunterfahren wird in {settings.DELAY_SHUTDOWN} Sekunden eingeleitet"}

@router.post("/system/reboot")
def reboot_system(background_tasks: BackgroundTasks, user: str = Depends(get_current_user)):
    write_log("WARN", f"Neustart wird in {settings.DELAY_REBOOT} Sekunden eingeleitet")
    background_tasks.add_task(delayed_reboot, settings.DELAY_REBOOT)
    return {"message": f"Neustart wird in {settings.DELAY_REBOOT} Sekunden eingeleitet"}

