from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.room.model.room_model import UserResponseRoomModel
from api_python.app.room.service.room_service import get_room_info_by_stay_seq

room_router = APIRouter(
    prefix="/room",
)


@room_router.get(
    "/info",
    summary="객실 정보 조회",
    description="객실 정보를 조회 합니다. stay_seq를 통해 조회 합니다.",
    tags=["객실"],
)
async def get_room_info(
        stay_seq: Annotated[int, Query(alias="staySeq", description="숙소 seq", ge=1)]
) -> ApiResponse[list[UserResponseRoomModel]]:
    result = await get_room_info_by_stay_seq(stay_seq)
    return ApiResponse.success(result)
