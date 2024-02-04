from typing import List

from api_python.app.review.model.review_model import UserResponseReviewModel
from api_python.app.review.repository.review_repository import get_stay_review_limit_offset

LIMIT_COUNT = 10


async def get_review_info_by_stay_seq(stay_seq: int, cursor: int) -> List[UserResponseReviewModel]:
    return await get_stay_review_limit_offset(
        stay_seq=stay_seq,
        offset=cursor*LIMIT_COUNT,
        limit=LIMIT_COUNT
    )
