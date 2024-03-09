from datetime import date
from typing import List
from api_python.app.room.model.room_model import UserResponseRoomModel, convert_room_model_to_response, \
    UserResponseAvailableRoomModel
from api_python.app.room.repository.room_repository import find_by_stay_seq_room_model, \
    get_available_room_info_by_stay_seq


async def get_room_info_by_stay_seq(stay_seq: int) -> List[UserResponseRoomModel]:
    room_list = await find_by_stay_seq_room_model(stay_seq)
    result = [convert_room_model_to_response(room) for room in room_list]
    return result


async def get_available_room_info_by_stay_seq_service(
        stay_seq: int,
        check_in_date: date,
        check_out_date: date,
        adult_guest_count: int,
        child_guest_count: int
) -> List[UserResponseAvailableRoomModel]:
    result = await get_available_room_info_by_stay_seq(
        stay_seq=stay_seq,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count
    )
    return result
