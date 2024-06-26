from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.depends.depends import user_seq_dependency_optional
from api_python.app.common.model.stay_type import StayType
from api_python.app.stay.model.stay_model import UserResponseStayInfoModel
from api_python.app.stay.service.stay_service import get_stay_info_service, \
    get_stay_wish_review_list_by_stay_type_service, get_stay_wish_review_list_by_stay_type_order_by_rank_service, \
    get_stay_wish_review_list_by_stay_type_order_by_review_count_service

stay_router = APIRouter(
    prefix="/stay",
)


@stay_router.get(
    "/list",
    summary="숙소 목록 조회",
    description="숙소 목록을 조회합니다, stayType으로 특정 숙소 타입을 정할 수 있습니다. cursor를 통해 페이징 처리가 가능합니다(cursor는 0부터 시작, 기본값은 0 입니다.)",
    tags=["숙소"],
)
async def get_stay_list(
        user_seq: Annotated[int, user_seq_dependency_optional],
        cursor: Annotated[int, Query(description="id 참조 지점", ge=0)] = 0,
        stay_type: Annotated[StayType | None, Query(alias="stayType", description="숙소 타입", ge=0, le=4)] = None
) -> ApiResponse[list[UserResponseStayInfoModel]]:
    result = await get_stay_wish_review_list_by_stay_type_service(
        cursor=cursor,
        user_seq=user_seq,
        stay_type=stay_type
    )
    return ApiResponse.success(result)


@stay_router.get(
    "/list/recommend/review-rank",
    summary="추천 숙소 목록 조회(별점 높은 순)",
    description="추천 숙소 목록을 조회합니다, stayType으로 특정 숙소 타입을 정할 수 있습니다. "
                "리뷰 별점 높은 순으로 정렬해서 제공합니다. 만약 평균 평점이 동일하면 리뷰가 많은 순으로 제공됨",
    tags=["숙소"],
)
async def get_stay_list_recommend_rank(
        user_seq: Annotated[int, user_seq_dependency_optional],
        stay_type: Annotated[StayType | None, Query(alias="stayType", description="숙소 타입", ge=0, le=4)] = None
) -> ApiResponse[list[UserResponseStayInfoModel]]:
    result = await get_stay_wish_review_list_by_stay_type_order_by_rank_service(
        user_seq=user_seq,
        stay_type=stay_type
    )
    return ApiResponse.success(result)


@stay_router.get(
    "/list/recommend/review-count",
    summary="추천 숙소 목록 조회(리뷰 많은 순)",
    description="추천 숙소 목록을 조회합니다, stayType으로 특정 숙소 타입을 정할 수 있습니다. 리뷰 많은 순으로 정렬해서 제공합니다. 만약 리뷰 개수가 동일하면 별점 높은 순으로 제공됨",
    tags=["숙소"],
)
async def get_stay_list_recommend_rank(
        user_seq: Annotated[int, user_seq_dependency_optional],
        stay_type: Annotated[StayType | None, Query(alias="stayType", description="숙소 타입", ge=0, le=4)] = None
) -> ApiResponse[list[UserResponseStayInfoModel]]:
    result = await get_stay_wish_review_list_by_stay_type_order_by_review_count_service(
        user_seq=user_seq,
        stay_type=stay_type
    )
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
) -> ApiResponse[UserResponseStayInfoModel]:
    result = await get_stay_info_service(
        user_seq=user_seq,
        stay_seq=stay_seq
    )
    return ApiResponse.success(result)


