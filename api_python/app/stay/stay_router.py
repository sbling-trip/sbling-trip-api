from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.stay.model.stay_info import StayInfoModel
from api_python.app.stay.service.stay_service import get_stay_info_by_cursor

stay_router = APIRouter(
    prefix="/stay",
)


@stay_router.get(
    "/list",
    summary="숙소 목록",
    tags=["숙소"],
)
async def get_stay_list(
        cursor: Annotated[int, Query(description="id 참조 지점")]
) -> ApiResponse[list[StayInfoModel]]:
    result = await get_stay_info_by_cursor(cursor)
    return ApiResponse.success(result)
