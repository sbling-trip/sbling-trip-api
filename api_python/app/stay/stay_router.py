from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.depends.depends import user_seq_dependency_optional
from api_python.app.stay.model.stay_model import StayInfoWishReviewModel
from api_python.app.stay.service.stay_service import get_stay_wish_review_list_service, get_stay_info_service

stay_router = APIRouter(
    prefix="/stay",
)


@stay_router.get(
    "/list",
    summary="숙소 목록 조회",
    description="숙소 목록을 조회합니다. cursor를 통해 페이징 처리가 가능합니다(cursor는 0부터 시작, 기본값은 0 입니다.)",
    tags=["숙소"],
)
async def get_stay_list(
        user_seq: Annotated[int, user_seq_dependency_optional],
        cursor: Annotated[int, Query(description="id 참조 지점", ge=0)] = 0
) -> ApiResponse[list[StayInfoWishReviewModel]]:
    result = await get_stay_wish_review_list_service(cursor=cursor, user_seq=user_seq)
    return ApiResponse.success(result)


@stay_router.get(
    "/info",
    summary="단일 숙소 조회",
    description="단일 숙소의 정보를 조회합니다.",
    tags=["숙소"],
)
async def get_stay_info(
        user_seq: Annotated[int, user_seq_dependency_optional],
        stay_seq: Annotated[int, Query(alias="staySeq", description="숙소 seq", ge=1)]
) -> ApiResponse[StayInfoWishReviewModel]:
    result = await get_stay_info_service(
        user_seq=user_seq,
        stay_seq=stay_seq
    )
    return ApiResponse.success(result)
