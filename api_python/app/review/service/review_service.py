from typing import List

from api_python.app.review.model.review_model import UserResponseReviewModel
from api_python.app.review.repository.review_repository import get_stay_review_limit_offset, add_review

LIMIT_COUNT = 10


async def get_review_info_by_stay_seq_service(stay_seq: int, cursor: int) -> List[UserResponseReviewModel]:
    return await get_stay_review_limit_offset(
        stay_seq=stay_seq,
        offset=cursor*LIMIT_COUNT,
        limit=LIMIT_COUNT
    )


async def add_review_info_service(
        stay_seq: int,
        user_seq: int,
        room_seq: int,
        review_title: str,
        review_content: str,
        review_score: int
) -> bool:
    await add_review(
        stay_seq=stay_seq,
        user_seq=user_seq,
        room_seq=room_seq,
        review_title=review_title,
        review_content=review_content,
        review_score=review_score
    )
    return True
