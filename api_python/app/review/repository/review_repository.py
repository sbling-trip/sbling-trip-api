from datetime import datetime
from textwrap import dedent

from api_python.app.common.client.postgres.postgres_client import postgres_client
from sqlalchemy import text, dialects

from api_python.app.review.model.review_model import UserResponseReviewModel, ReviewModel, \
    convert_review_model_to_response, ReviewOrm


async def get_stay_review_limit_offset(
        stay_seq: int,
        offset: int,
        limit: int
) -> list[UserResponseReviewModel]:
    async with postgres_client.session() as session:
        try:
            get_stay_review_query = text(dedent(f"""
            SELECT 
                review_seq, user_seq, r.room_seq, room_name, review_title,
                review_content, review_score, review_image_url_list, created_at
            FROM public.review r
            JOIN room_info ri ON r.room_seq = ri.room_seq AND r.stay_seq = {stay_seq}
            WHERE exposed = true
            ORDER BY review_seq
            LIMIT {limit} OFFSET {offset}
            ;
            """))

            result = await session.execute(get_stay_review_query)

            stay_review = [convert_review_model_to_response(ReviewModel(**row)) for row in result.mappings().all()]
            return stay_review

        except Exception as e:
            print(e)
            return []


async def add_review(
        stay_seq: int,
        user_seq: int,
        room_seq: int,
        review_title: str,
        review_content: str,
        review_score: int,
        review_image_url_list: list[str] = []
) -> bool:
    async with postgres_client.session() as session:
        try:
            stmt = dialects.postgresql.insert(ReviewOrm).values(
                user_seq=user_seq,
                stay_seq=stay_seq,
                room_seq=room_seq,
                review_title=review_title,
                review_content=review_content,
                review_score=review_score,
                review_image_url_list=review_image_url_list,
                created_at=datetime.utcnow(),
                modified_at=datetime.utcnow()
            )
            await session.execute(stmt)
            return True
        except Exception as e:
            print(e)
            return False
