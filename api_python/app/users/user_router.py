from typing import Annotated

from fastapi import APIRouter, Depends

from api_python.app.users.model.user_model import UserModel
from api_python.app.users.service.user_service import get_current_active_user

user_router = APIRouter(
    prefix="/user"
)


@user_router.get("/info")
async def get_user_info(current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    return current_user
