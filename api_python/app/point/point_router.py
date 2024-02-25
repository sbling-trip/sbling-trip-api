from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.depends.depends import user_seq_dependency
from api_python.app.common.api_response import ApiResponse
from api_python.app.point.service.point_service import (
    get_point_service,
    update_point_service,
)
from api_python.app.user.model.user_model import UserUpdateModel
from api_python.app.user.repository.user_repository import update_user

point_router = APIRouter(
    prefix="/point",
)


@point_router.get(
    "/me",
    summary="현재 로그인한 유저 포인트 조회",
    description="현재 로그인 한 유저의 포인트를 조회합니다.",
    tags=["포인트"],
)
async def get_point(
    user_seq: Annotated[int, user_seq_dependency],
):
    result = await get_point_service(user_seq=user_seq)
    return ApiResponse.success(result)
