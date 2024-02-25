import datetime
from typing import Annotated, Dict, Any

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.reservation.service.reservation_service import get_reservation_count_by_room_seq_service

reservation_router = APIRouter(
    prefix="/reservation",
)


@reservation_router.get(
    "/count",
    summary="예약 수 조회",
    description="예약 수를 조회합니다. roomSeq, checkInDate, checkOutdate를 통해 조회합니다.",
    tags=["예약"],
)
async def get_reservation_count(
        room_seq: Annotated[int, Query(alias="roomSeq", description="객실 seq", ge=1)],
        check_in_date: Annotated[datetime.date, Query(alias="checkInDate", description="체크인 날짜")],
        check_out_date: Annotated[datetime.date, Query(alias="checkOutDate", description="체크 아웃 날짜")]
) -> ApiResponse[int]:
    result = await get_reservation_count_by_room_seq_service(room_seq, check_in_date, check_out_date)
    return ApiResponse.success(result=result)
