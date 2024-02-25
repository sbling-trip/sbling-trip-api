from datetime import datetime

from api_python.app.reservation.repository.reservation_repository import get_reservation_count_by_room_seq


async def get_reservation_count_by_room_seq_service(
        room_seq: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date)\
        -> int:
    result = await get_reservation_count_by_room_seq(
        room_seq=room_seq,
        check_in_date=check_in_date,
        check_out_date=check_out_date)
    return result
