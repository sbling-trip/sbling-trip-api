from typing import Annotated

from fastapi import APIRouter, Query, Depends

from api_python.app.common.api_response import ApiResponse
from api_python.app.stay.model.stay_model import StayInfoWishModel
from api_python.app.stay.service.stay_service import get_stay_wish_all_list_service
from api_python.app.user.service.user_service import get_user_seq_by_authorization_optional

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
        user_seq: Annotated[int, Depends(get_user_seq_by_authorization_optional)],
        cursor: Annotated[int, Query(description="id 참조 지점", ge=0)] = 0
) -> ApiResponse[list[StayInfoWishModel]]:
    result = await get_stay_wish_all_list_service(cursor=cursor, user_seq=user_seq)
    return ApiResponse.success(result)
