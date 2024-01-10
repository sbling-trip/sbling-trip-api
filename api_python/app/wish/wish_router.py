from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse

wish_router = APIRouter(
    prefix="/wish",
)


@wish_router.get(
    "/add",
    summary="숙소 찜 목록 추가",
    tags=["숙소", "찜"],
    description="아직 미구현 된 API 입니다."
)
async def add_stay_wish(
        stay_seq: Annotated[int, Query(alias="staySeq", description="찜 추가할 숙소 seq")],
        user_seq: Annotated[int, Query(description="찜 추가할 유저 seq")]
) -> ApiResponse[str]:
    return ApiResponse.success("Success")


@wish_router.get(
    "/remove",
    summary="숙소 찜 목록 삭제",
    tags=["숙소", "찜"],
    description="아직 미구현 된 API 입니다."
)
async def remove_stay_wish(
        stay_seq: Annotated[int, Query(description="찜 삭제할 숙소 seq")],
        user_seq: Annotated[int, Query(description="찜 삭제할 유저 seq")]
) -> ApiResponse[str]:
    return ApiResponse.success("Success")


@wish_router.get(
    "list",
    summary="숙소 찜 목록 조회",
    description="아직 미구현 된 API 입니다."
)
async def get_stay_wish_list() -> ApiResponse[str]:
    return ApiResponse.success("Success")