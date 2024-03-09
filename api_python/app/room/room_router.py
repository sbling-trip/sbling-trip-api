from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.room.model.room_model import UserResponseRoomModel, UserResponseAvailableRoomModel
from api_python.app.room.service.room_service import get_room_info_by_stay_seq, \
    get_available_room_info_by_stay_seq_service

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


@room_router.get(
    "/info/available",
    summary="예약 가능 객실 정보 조회",
    description="예약 가능한 객실 정보를 조회 합니다. stay_seq를 통해 조회 합니다.",
    tags=["예약"],
)
async def get_available_room_info(
        stay_seq: Annotated[int, Query(alias="staySeq", description="숙소 seq", ge=1)],
        check_in_date: Annotated[date, Query(alias="checkInDate", description="체크인 날짜")],
        check_out_date: Annotated[date, Query(alias="checkOutDate", description="체크 아웃 날짜")],
        adult_guest_count: Annotated[int, Query(alias="adultGuestCount", description="성인 수")],
        child_guest_count: Annotated[int, Query(alias="childGuestCount", description="아동 수")]
) -> ApiResponse[list[UserResponseAvailableRoomModel]]:
    result = await get_available_room_info_by_stay_seq_service(
        stay_seq=stay_seq,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count
    )
    return ApiResponse.success(result)
