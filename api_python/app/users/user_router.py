from typing import Annotated

from fastapi import APIRouter, Depends

from api_python.app.common.api_response import ApiResponse
from api_python.app.users.service.user_service import get_current_user

user_router = APIRouter(
    prefix="/user",
)


@user_router.get(
    "/info",
    summary="유저 정보 조회",
    description="유저 정보를 조회합니다. 해당 유저의 seq를 반환합니다.",
    tags=["유저"],
)
async def get_user_info(user_seq: Annotated[int, Depends(get_current_user)]):
    return ApiResponse.success(user_seq)
