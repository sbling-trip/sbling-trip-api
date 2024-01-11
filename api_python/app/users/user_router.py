from typing import Annotated

from fastapi import APIRouter, Depends

from api_python.app.common.api_response import ApiResponse
from api_python.app.users.service.user_service import get_current_user

user_router = APIRouter(
    prefix="/user"
)


@user_router.get("/info")
async def get_user_info(user_seq: Annotated[int, Depends(get_current_user)]):
    return ApiResponse.success(user_seq)
