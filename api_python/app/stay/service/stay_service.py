from api_python.app.stay.model.stay_model import StayInfoModel, StayInfoWishModel, StayInfoWishReviewModel
from api_python.app.stay.repository.stay_repository import find_by_seq_limit_offset, \
    get_stay_info_with_review_for_user_seq_limit_offset
from api_python.app.wish.repository.wish_repository import get_stay_info_with_for_user_seq_limit_offset

LIMIT_COUNT = 20


async def get_stay_info_by_cursor(cursor: int) -> list[StayInfoModel]:
    return await find_by_seq_limit_offset(offset=cursor*LIMIT_COUNT, limit=LIMIT_COUNT)


async def get_stay_wish_all_list_service(
        user_seq: int,
        cursor: int
) -> list[StayInfoWishModel]:
    result = await get_stay_info_with_for_user_seq_limit_offset(
        user_seq=user_seq,
        offset=cursor*LIMIT_COUNT,
        limit=LIMIT_COUNT
    )
    return result


async def get_stay_wish_review_list_service(
        user_seq: int,
        cursor: int
) -> list[StayInfoWishReviewModel]:
    result = await get_stay_info_with_review_for_user_seq_limit_offset(
        user_seq=user_seq,
        offset=cursor*LIMIT_COUNT,
        limit=LIMIT_COUNT
    )
    return result
