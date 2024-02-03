from api_python.app.stay.model.stay_model import StayInfoModel, StayInfoWishModel
from api_python.app.wish.repository.wish_repository import insert_by_user_seq_stay_seq, update_by_user_seq_stay_seq, \
    get_stay_info_for_user_wish, get_stay_info_with_for_user_wish_all


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
        user_seq: int
) -> list[StayInfoModel]:
    result = await get_stay_info_for_user_wish(user_seq)
    return result


async def get_stay_wish_all_list_service(
        user_seq: int
) -> list[StayInfoWishModel]:
    result = await get_stay_info_with_for_user_wish_all(user_seq)
    return result

