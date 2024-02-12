from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.config.phase import IS_LOCAL
from api_python.app.common.depends.depends import user_seq_dependency_optional, user_seq_dependency
from api_python.app.review.model.review_model import UserResponseReviewModel
from api_python.app.review.service.review_service import get_review_info_by_stay_seq_service, add_review_info_service, \
    update_review_info_service, remove_review_service

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
    description="숙소의 리뷰를 추가합니다. 현재 이미지 업로드는 미구현 상태입니다. 추후 업데이트 예정입니다.",
    tags=["리뷰"],
)
async def add_review_info(
        user_seq: Annotated[int, user_seq_dependency_optional if IS_LOCAL else user_seq_dependency],
        stay_seq: Annotated[int, Query(alias="staySeq", description="숙소 seq", ge=1)],
        room_seq: Annotated[int, Query(alias="roomSeq", description="객실 seq", ge=1)],
        review_title: Annotated[str, Query(alias="reviewTitle", description="리뷰 제목", min_length=1, max_length=50)],
        review_content: Annotated[str, Query(alias="reviewContent", description="리뷰 내용", min_length=1, max_length=200)],
        review_score: Annotated[int, Query(alias="reviewScore", description="별점", ge=1, le=5)],
) -> ApiResponse[str]:
    await add_review_info_service(
        user_seq=user_seq,
        stay_seq=stay_seq,
        room_seq=room_seq,
        review_title=review_title,
        review_content=review_content,
        review_score=review_score
    )
    return ApiResponse.success("Success")


@review_router.put(
    "/update",
    summary="리뷰 수정",
    description="숙소의 리뷰를 수정합니다. 리뷰 seq를 통해 수정합니다. 입력하지 않은 필드 값 데이터는 수정되지 않습니다."
                " 현재 이미지 수정은 미구현 상태입니다. 추후 업데이트 예정입니다.",
    tags=["리뷰"],
)
async def update_review_info(
        review_seq: Annotated[int, Query(alias="reviewSeq", description="리뷰 seq", ge=1)],
        review_title: Annotated[str | None, Query(alias="reviewTitle", description="리뷰 제목", min_length=1, max_length=50)] = None,
        review_content: Annotated[str | None, Query(alias="reviewContent", description="리뷰 내용", min_length=1, max_length=200)] = None,
        review_score: Annotated[int | None, Query(alias="reviewScore", description="별점", ge=1, le=5)] = None,
) -> ApiResponse[str]:
    await update_review_info_service(
        review_seq=review_seq,
        review_title=review_title,
        review_content=review_content,
        review_score=review_score
    )
    return ApiResponse.success("Success")


@review_router.delete(
    "/remove",
    summary="리뷰 삭제",
    description="숙소의 리뷰를 삭제합니다.",
    tags=["리뷰"],
)
async def remove_review_info(
        review_seq: Annotated[int, Query(alias="reviewSeq", description="리뷰 seq", ge=1)]
) -> ApiResponse[str]:
    await remove_review_service(
        review_seq=review_seq,
    )
    return ApiResponse.success("Success")