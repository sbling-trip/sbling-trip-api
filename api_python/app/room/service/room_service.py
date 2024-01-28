from typing import List
from api_python.app.room.model.room_model import UserResponseRoomModel, convert_room_model_to_response
from api_python.app.room.repository.room_repository import find_by_stay_seq_room_model


async def get_room_info_by_stay_seq(stay_seq: int) -> List[UserResponseRoomModel]:
    room_list = await find_by_stay_seq_room_model(stay_seq)
    result = [convert_room_model_to_response(room) for room in room_list]
    return result
