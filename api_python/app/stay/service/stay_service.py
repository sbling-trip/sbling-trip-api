from api_python.app.stay.model.stay_info import StayInfoModel
from api_python.app.stay.repository.stay_repository import find_by_seq_limit_offset

LIMIT_COUNT = 20


async def get_stay_info_by_cursor(cursor: int) -> list[StayInfoModel]:
    return await find_by_seq_limit_offset(offset=cursor*LIMIT_COUNT, limit=LIMIT_COUNT)
