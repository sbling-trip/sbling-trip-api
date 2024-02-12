from typing import Annotated, List

from fastapi import APIRouter, Query, File, UploadFile, Body, Depends

from api_python.app.common.api_response import ApiResponse
from api_python.app.review.model.review_model import UserResponseReviewModel
from api_python.app.review.service.review_service import get_review_info_by_stay_seq_service, add_review_info_service
from api_python.app.user.service.user_service import get_user_seq_by_authorization

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
    result = await get_review_info_by_stay_seq_service(stay_seq, cursor)
    return ApiResponse.success(result)


@review_router.post(
    "/add",
    summary="리뷰 추가",
    description="숙소의 리뷰를 추가합니다.",
    tags=["리뷰"],
)
async def add_review_info(
        user_seq: Annotated[int, Depends(get_user_seq_by_authorization)],
        stay_seq: Annotated[int, Query(alias="staySeq", description="숙소 seq", ge=1)],
        room_seq: Annotated[int, Query(alias="roomSeq", description="객실 seq", ge=1)],
        review_title: Annotated[str, Query(alias="reviewTitle", description="리뷰 제목", min_length=1, max_length=50)],
        review_content: Annotated[str, Query(alias="reviewContent", description="리뷰 내용", min_length=1, max_length=200)],
        review_score: Annotated[int, Query(alias="reviewScore", description="별점", ge=1, le=5)],
) -> ApiResponse[str]:
    await add_review_info_service(
        user_seq,
        stay_seq,
        room_seq,
        review_title,
        review_content,
        review_score
    )
    return ApiResponse.success("Success")
