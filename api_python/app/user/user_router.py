from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.depends.depends import user_seq_dependency
from api_python.app.common.api_response import ApiResponse
from api_python.app.user.service.user_service import (
    get_user_info_service,
)
from api_python.app.user.model.user_model import UserUpdateModel
from api_python.app.user.repository.user_repository import update_user

user_router = APIRouter(
    prefix="/user",
)


@user_router.get(
    "/me",
    summary="현재 로그인한 유저 정보 조회",
    description="현재 로그인 한 유저 정보를 조회합니다. 로그인 유저의 seq를 반환합니다.",
    tags=["유저"],
)
async def get_user_info(
    user_seq: Annotated[int, user_seq_dependency],
):
    result = await get_user_info_service(user_seq=user_seq)
    return ApiResponse.success(result)


@user_router.put(
    "/update",
    summary="유저 수정",
    description="유저의 정보를 수정합니다. 현재 로그인한 유저를 수정합니다. 입력하지 않은 필드 값 데이터는 수정되지 않습니다."
    " 현재 이미지 수정은 미구현 상태입니다. 추후 업데이트 예정입니다.",
    tags=["유저"],
)
async def update_user_info(
    user_seq: Annotated[int, user_seq_dependency], user: UserUpdateModel
) -> ApiResponse[str]:
    await update_user(
        user_seq=user_seq,
        user_name=user.user_name,
        location_agree=user.location_agree,
        marketing_agree=user.marketing_agree,
    )
    return ApiResponse.success("Success")
