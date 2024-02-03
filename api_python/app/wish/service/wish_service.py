from api_python.app.stay.model.stay_model import StayInfoWishModel
from api_python.app.wish.repository.wish_repository import insert_by_user_seq_stay_seq, update_by_user_seq_stay_seq, \
    get_stay_info_for_user_wish

LIMIT_COUNT = 20


async def add_stay_wish_service(
        user_seq: int,
        stay_seq: int
) -> bool:
    await insert_by_user_seq_stay_seq(user_seq, stay_seq)
    return True


async def remove_stay_wish_service(
        user_seq: int,
        stay_seq: int
) -> bool:
    await update_by_user_seq_stay_seq(user_seq, stay_seq)
    return True


async def get_stay_wish_list_service(
        user_seq: int,
        cursor: int
) -> list[StayInfoWishModel]:
    result = await get_stay_info_for_user_wish(
        user_seq=user_seq,
        offset=cursor*LIMIT_COUNT,
        limit=LIMIT_COUNT
    )
    return result

