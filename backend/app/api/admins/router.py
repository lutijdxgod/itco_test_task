from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from app.core.database import db_helper as db

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.oauth2 import get_current_user
from app.schemas.admin import AdminOut

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("/my_info", response_model=AdminOut)
async def get_my_info(
    current_user: AdminOut = Depends(get_current_user),
):
    return current_user
