import datetime
from typing import Annotated, Dict, Any

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.reservation.service.reservation_service import get_reservation_count_by_room_seq_service

reservation_router = APIRouter(
    prefix="/reservation",
)


@reservation_router.get(
    "/available-room",
    summary="예약 가능한 수 조회",
    description="특정 일자에 예약 가능한 숙소를 조회 합니다. 예약 희망 성인 수, 아동 수, 체크인, 체크 아웃 날짜를 통해 조회합니다.",
    tags=["예약"],
)
async def get_reservation_stay(
        check_in_date: Annotated[str, Query(alias="checkInDate", description="체크인 날짜")],
        check_out_date: Annotated[str, Query(alias="checkOutDate", description="체크 아웃 날짜")],
        adult_guest_count: Annotated[int, Query(alias="adultGuestCount", description="성인 수")],
        child_guest_count: Annotated[int, Query(alias="childGuestCount", description="아동 수")],
) -> ApiResponse[int]:
    return ApiResponse.success(result="Success")
