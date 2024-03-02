import datetime
from typing import Annotated, Dict, Any

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.config.phase import IS_LOCAL
from api_python.app.common.depends.depends import user_seq_dependency_optional, user_seq_dependency
from api_python.app.common.model.stay_type import StayType
from api_python.app.reservation.service.reservation_service import get_reservation_stay_service
from api_python.app.stay.model.stay_model import UserResponseStayInfoModel

reservation_router = APIRouter(
    prefix="/reservation",
)


@reservation_router.get(
    "/available-stay",
    summary="예약 가능한 숙소 조회",
    description="특정 일자에 예약 가능한 숙소를 조회 합니다. 예약 희망 성인 수, 아동 수, 체크인, 체크 아웃, 숙소 타입을 통해 조회합니다.",
    tags=["예약"],
)
async def get_reservation_stay(
        user_seq: Annotated[int, user_seq_dependency_optional if IS_LOCAL else user_seq_dependency],
        check_in_date: Annotated[str, Query(alias="checkInDate", description="체크인 날짜")],
        check_out_date: Annotated[str, Query(alias="checkOutDate", description="체크 아웃 날짜")],
        adult_guest_count: Annotated[int, Query(alias="adultGuestCount", description="성인 수")],
        child_guest_count: Annotated[int, Query(alias="childGuestCount", description="아동 수")],
        cursor: Annotated[int, Query(description="id 참조 지점", ge=0)] = 0,
        stay_type: Annotated[StayType | None, Query(alias="stayType", description="숙소 타입", ge=0, le=4)] = None
) -> ApiResponse[list[UserResponseStayInfoModel]]:
    result = await get_reservation_stay_service(
        user_seq=user_seq,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count,
        cursor=cursor,
        stay_type=stay_type,
    )
    return ApiResponse.success(result=result)
