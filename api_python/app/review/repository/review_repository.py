from textwrap import dedent

from api_python.app.common.client.postgres.postgres_client import postgres_client
from sqlalchemy import text, dialects, update

from api_python.app.common.exceptions import add_review_not_found_exception, get_review_exception, \
    update_review_exception, \
    remove_review_exception, add_review_server_exception
from api_python.app.common.kst_time import get_kst_time_now
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
                review_content, review_score, review_image_url_list, modified_at
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
            raise get_review_exception(str(e))


async def add_review(
        stay_seq: int,
        user_seq: int,
        room_seq: int,
        review_title: str,
        review_content: str,
        review_score: int,
        review_image_url_list: list[str]
) -> bool:
    async with postgres_client.session() as session:
        # 해당 stay_seq와 room_seq가 존재하는지 확인
        check_room_query = text(dedent(f"""
        SELECT room_seq, stay_seq
        FROM public.room_info
        WHERE room_seq = {room_seq} AND stay_seq = {stay_seq}
        LIMIT 1
        """))

        result = await session.execute(check_room_query)
        room_exists = result.fetchone()
        if not room_exists:
            raise add_review_not_found_exception("해당 숙소와 방이 존재하지 않습니다. staySeq와 roomSeq를 확인해주세요.")
        try:
            stmt = dialects.postgresql.insert(ReviewOrm).values(
                user_seq=user_seq,
                stay_seq=stay_seq,
                room_seq=room_seq,
                review_title=review_title,
                review_content=review_content,
                review_score=review_score,
                review_image_url_list=str(review_image_url_list),
                created_at=get_kst_time_now(),
                modified_at=get_kst_time_now(),
                exposed=True
            )
            await session.execute(stmt)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            raise add_review_server_exception(str(e))


async def update_review(
        review_seq: int,
        review_title: str | None,
        review_content: str | None,
        review_score: int | None
) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                stmt = update(ReviewOrm).where(ReviewOrm.review_seq == review_seq).values(
                    review_title=review_title if review_title else ReviewOrm.review_title,
                    review_content=review_content if review_content else ReviewOrm.review_content,
                    review_score=review_score if review_score else ReviewOrm.review_score,
                    modified_at=get_kst_time_now()
                )
                await session.execute(stmt)
                return True
        except Exception as e:
            raise update_review_exception(str(e))


async def remove_review(review_seq: int) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                stmt = update(ReviewOrm).where(ReviewOrm.review_seq == review_seq).values(
                    exposed=False
                )
                await session.execute(stmt)
                return True
        except Exception as e:
            raise remove_review_exception(str(e))
