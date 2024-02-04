from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.review.model.review_model import UserResponseReviewModel
from api_python.app.review.service.review_service import get_review_info_by_stay_seq

review_router = APIRouter(
    prefix="/review",
)


@review_router.get(
    "/info",
    summary="리뷰 조회",
    description="숙소의 리뷰를 조회합니다. staySeq와 cursor를 통해 조회합니다. 10개씩 조회합니다.",
    tags=["리뷰"],
)
async def get_review_info(
        stay_seq: Annotated[int, Query(alias="staySeq", description="숙소 seq", ge=1)],
        cursor: Annotated[int, Query(description="id 참조 지점", ge=0)] = 0
) -> ApiResponse[list[UserResponseReviewModel]]:
    result = await get_review_info_by_stay_seq(stay_seq, cursor)
    return ApiResponse.success(result)
