from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.stay.model.stay_model import StayInfoModel, StayInfoWishModel
from api_python.app.wish.repository.wish_repository import update_by_user_seq_stay_seq
from api_python.app.wish.service.wish_service import add_stay_wish_service, get_stay_wish_list_service, \
    get_stay_wish_all_list_service

wish_router = APIRouter(
    prefix="/wish",
)


@wish_router.get(
    "/add",
    summary="숙소 찜 목록 추가",
    description="staySeq, userSeq를 받아서 찜 목록에 추가합니다.",
    tags=["숙소", "찜"],
)
async def add_stay_wish(
        stay_seq: Annotated[int, Query(alias="staySeq", description="찜 추가할 숙소 seq")],
        user_seq: Annotated[int, Query(alias="userSeq", description="찜 추가할 유저 seq")],
) -> ApiResponse[str]:
    await add_stay_wish_service(user_seq, stay_seq)
    return ApiResponse.success("Success")


@wish_router.get(
    "/remove",
    summary="숙소 찜 목록 삭제",
    description="staySeq, userSeq를 받아서 찜 목록에서 삭제합니다.",
    tags=["숙소", "찜"],
)
async def remove_stay_wish(
        stay_seq: Annotated[int, Query(description="찜 삭제할 숙소 seq")],
        user_seq: Annotated[int, Query(alias="userSeq", description="찜 삭제할 유저 seq")],
) -> ApiResponse[str]:
    await update_by_user_seq_stay_seq(user_seq, stay_seq)
    return ApiResponse.success("Success")


@wish_router.get(
    "/list",
    summary="숙소 찜 목록 조회",
    description="userSeq를 받아서 찜 목록을 조회합니다.",
    tags=["숙소", "찜"],
)
async def get_stay_wish_list(
        user_seq: Annotated[int, Query(alias="userSeq", description="찜 목록을 조회할 유저 seq")],
) -> ApiResponse[list[StayInfoModel]]:
    result = await get_stay_wish_list_service(user_seq)
    return ApiResponse.success(result)


@wish_router.get(
    "/all",
    summary="숙소 찜과 이외 목록 모두 조회",
    description="userSeq를 받아서 찜 목록과 이외 목록을 모두 조회합니다.",
    tags=["숙소", "찜"],
)
async def get_stay_wish_all_list(
    user_seq: Annotated[int, Query(alias="userSeq", description="찜 목록을 조회할 유저 seq")],
) -> ApiResponse[list[StayInfoWishModel]]:
    result = await get_stay_wish_all_list_service(user_seq)
    return ApiResponse.success(result)
