from datetime import datetime
from typing import List

from api_python.app.reservation.model.reservation_model import UserResponseReservationInfoModel
from api_python.app.reservation.repository.reservation_repository import get_reservation_stay_repository, \
    get_reservation_room_list
from api_python.app.stay.model.stay_model import UserResponseStayInfoModel

LIMIT_COUNT = 20


async def get_reservation_available_stay_service(
        user_seq: int,
        cursor: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
        stay_type: int,
) -> List[UserResponseStayInfoModel]:
    result = await get_reservation_stay_repository(
        user_seq=user_seq,
        offset=cursor*LIMIT_COUNT,
        limit=LIMIT_COUNT,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count,
        stay_type=stay_type
    )
    return result


async def get_reservation_room_list_service(
        user_seq: int,
        reservation_status: list[str]
) -> List[UserResponseReservationInfoModel]:
    result = await get_reservation_room_list(
        user_seq=user_seq,
        reservation_status=reservation_status
    )
    return result
