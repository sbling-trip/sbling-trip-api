from typing import Annotated

from fastapi import APIRouter, Depends

from api_python.app.common.api_response import ApiResponse
from api_python.app.user.model.user_model import UserResponseModel
from api_python.app.user.service.user_service import get_current_user_by_authorization, get_current_user_by_cookie

user_router = APIRouter(
    prefix="/user",
)


@user_router.get(
    "/info",
    summary="유저 정보 조회",
    description="유저 정보를 조회합니다. 로그인 유저의 seq를 반환합니다.",
    tags=["유저"],
    deprecated=True,
)
async def get_user_info(user_response_model: Annotated[UserResponseModel, Depends(get_current_user_by_authorization)]):
    return ApiResponse.success(user_response_model)


@user_router.get(
    "/info/cookie",
    summary="유저 정보 조회",
    description="유저 정보를 반환합니다.. 세팅된 쿠키 값으로 인증된 사용자인지 검증합니다.",
    tags=["유저"],
)
async def get_user_info_from_cookie(user_response_model: Annotated[UserResponseModel, Depends(get_current_user_by_cookie)]):
    return ApiResponse.success(user_response_model)
