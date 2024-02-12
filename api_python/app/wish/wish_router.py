from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.depends.depends import user_seq_dependency
from api_python.app.stay.model.stay_model import StayInfoWishModel
from api_python.app.wish.repository.wish_repository import update_by_user_seq_stay_seq
from api_python.app.wish.service.wish_service import add_stay_wish_service, get_stay_wish_list_service, \
    remove_stay_wish_service

wish_router = APIRouter(
    prefix="/wish",
)


@wish_router.post(
    "/add",
    summary="숙소 찜 목록 추가",
    description="찜 목록에 추가합니다. 추가할 숙소 seq를 받아서 추가합니다.",
    tags=["찜"],
)
async def add_stay_wish(
        stay_seq: Annotated[int, Query(alias="staySeq", description="찜 추가할 숙소 seq")],
        user_seq: Annotated[int, user_seq_dependency],
) -> ApiResponse[str]:
    await add_stay_wish_service(user_seq=user_seq, stay_seq=stay_seq)
    return ApiResponse.success("Success")


@wish_router.delete(
    "/remove",
    summary="숙소 찜 목록 삭제",
    description="찜 목록에서 삭제합니다. 삭제할 숙소 seq를 받아 삭제합니다.",
    tags=["찜"],
)
async def remove_stay_wish(
        stay_seq: Annotated[int, Query(alias="staySeq", description="찜 삭제할 숙소 seq")],
        user_seq: Annotated[int, user_seq_dependency],
) -> ApiResponse[str]:
    await remove_stay_wish_service(user_seq=user_seq, stay_seq=stay_seq)
    return ApiResponse.success("Success")


@wish_router.get(
    "/list",
    summary="숙소 찜 목록 조회",
    description="찜 목록을 조회합니다. cursor를 통해 페이징 처리가 가능합니다(cursor는 0부터 시작, 기본값은 0 입니다.)",
    tags=["찜"],
)
async def get_stay_wish_list(
        user_seq: Annotated[int, user_seq_dependency],
        cursor: Annotated[int, Query(description="id 참조 지점", ge=0)] = 0,
) -> ApiResponse[list[StayInfoWishModel]]:
    result = await get_stay_wish_list_service(cursor=cursor, user_seq=user_seq)
    return ApiResponse.success(result)
