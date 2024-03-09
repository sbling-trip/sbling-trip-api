import datetime
from typing import Annotated, Dict, Any

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.config.phase import IS_LOCAL
from api_python.app.common.depends.depends import user_seq_dependency_optional, user_seq_dependency
from api_python.app.reservation.model.reservation_model import UserResponseReservationInfoModel

reservation_router = APIRouter(
    prefix="/reservation",
)


@reservation_router.get(
    "/list",
    summary="예약 목록 조회",
    description="예약 목록을 조회합니다, cursor를 통해 페이징 처리가 가능합니다(cursor는 0부터 시작, 기본값은 0 입니다.)",
    tags=["예약"],
)
async def get_reservation_list(
    user_seq: Annotated[int, user_seq_dependency],
    cursor: Annotated[int, Query(description="id 참조 지점", ge=0)] = 0,
) -> ApiResponse[UserResponseReservationInfoModel]:
    return ApiResponse.success(UserResponseReservationInfoModel(
        reservation_seq=1,
        stay_seq=1,
        room_seq=1,
        check_in_date=datetime.datetime.now(),
        check_out_date=datetime.datetime.now(),
        adult_guest_count=1,
        child_guest_count=1,
        reservation_status="test",
        booking_date=datetime.datetime.now(),
        payment_status="test",
        special_requests="test"
    )
    )
