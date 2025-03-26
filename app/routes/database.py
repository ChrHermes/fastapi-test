# app/routes/system.py

import docker

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.services.database_service import database_reset, database_info
from app.schemas.errors import *
from app.utils.auth import get_current_user

router = APIRouter()

try:
    docker_client = docker.from_env()
except Exception as e:
    docker_client = None


# =====================================
#          DATABASE
# ===================================== 

@router.post("/database/reset")
async def post_database_reset(user: str = Depends(get_current_user)):
    try:
        result = await database_reset(
            backend_container=settings.BACKEND_CONTAINER,
            database_path=settings.DB_PATH
        )
        return result
    except DockerClientNotAvailableError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ContainerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (ContainerStopError, ContainerStartError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    except DatabaseResetError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/database/info")
async def get_database_info(user: str = Depends(get_current_user)):
    try:
        result = await database_info(
            database_path=settings.DB_PATH
        )
        return result
    except DatabaseInfoError as e:
        raise HTTPException(status_code=500, detail=str(e))
