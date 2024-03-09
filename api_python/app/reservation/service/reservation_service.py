from datetime import datetime
from typing import List

from api_python.app.common.exceptions import get_validate_stay_room_seq_exception
from api_python.app.reservation.model.reservation_model import UserResponseReservationInfoModel
from api_python.app.reservation.repository.reservation_repository import get_reservation_stay_repository, \
    get_reservation_room_list, add_reservation_repository, is_validate_stay_room_seq
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


async def add_reservation_service(
        user_seq: int,
        stay_seq: int,
        room_seq: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
        special_requests: str,
        payment_price: int
) -> bool:
    validate_stay_room_seq = await is_validate_stay_room_seq(
        stay_seq=stay_seq,
        room_seq=room_seq
    )
    if not validate_stay_room_seq:
        raise get_validate_stay_room_seq_exception("올바르지 않은 숙소 또는 방입니다.")
    result = await add_reservation_repository(
        user_seq=user_seq,
        stay_seq=stay_seq,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count,
        special_requests=special_requests,
        payment_price=payment_price
    )