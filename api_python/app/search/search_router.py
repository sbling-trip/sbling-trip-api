from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.depends.depends import user_seq_dependency_optional
from api_python.app.common.model.stay_type import StayType
from api_python.app.reservation.service.reservation_service import get_reservation_available_stay_service
from api_python.app.room.model.room_model import UserResponseAvailableRoomModel
from api_python.app.room.service.room_service import get_available_room_info_by_stay_seq_service
from api_python.app.stay.model.stay_model import UserResponseStayInfoModel

search_router = APIRouter(
    prefix="/search",
)


@search_router.get(
    "/stay/list",
    summary="예약 가능한 숙소 조회",
    description="특정 일자에 예약 가능한 숙소를 조회 합니다. 예약 희망 성인 수, 아동 수, 체크인, 체크 아웃, 숙소 타입을 통해 조회합니다.",
    tags=["검색"],
)
async def get_reservation_stay(
        user_seq: Annotated[int, user_seq_dependency_optional],
        check_in_date: Annotated[date, Query(alias="checkInDate", description="체크인 날짜")],
        check_out_date: Annotated[date, Query(alias="checkOutDate", description="체크 아웃 날짜")],
        adult_guest_count: Annotated[int, Query(alias="adultGuestCount", description="성인 수")],
        child_guest_count: Annotated[int, Query(alias="childGuestCount", description="아동 수")],
        cursor: Annotated[int, Query(description="id 참조 지점", ge=0)] = 0,
        stay_type: Annotated[StayType | None, Query(alias="stayType", description="숙소 타입", ge=0, le=4)] = None
) -> ApiResponse[list[UserResponseStayInfoModel]]:
    result = await get_reservation_available_stay_service(
        user_seq=user_seq,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count,
        cursor=cursor,
        stay_type=stay_type,
    )
    return ApiResponse.success(result=result)


@search_router.get(
    "/room/list",
    summary="예약 가능 객실 정보 조회",
    description="예약 가능한 객실 정보를 조회 합니다. stay_seq를 통해 조회 합니다.",
    tags=["검색"],
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