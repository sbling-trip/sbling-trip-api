from typing import Tuple
from textwrap import dedent

from sqlalchemy import select, ChunkedIteratorResult

from api_python.app.common.client.postgres.postgres_client import postgres_client
from api_python.app.stay.model.stay_model import StayInfoModel, StayInfoOrm, StayInfoWishReviewModel
from sqlalchemy import text


def stay_orm_to_pydantic_model(result: ChunkedIteratorResult[Tuple[StayInfoOrm]]) -> list[StayInfoModel]:
    return [StayInfoModel.model_validate(orm) for orm in result.scalars().all()]


async def find_all() -> list[StayInfoModel]:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    StayInfoOrm
                )
            )
            return stay_orm_to_pydantic_model(result)


async def find_by_seq_limit_offset(offset: int, limit: int) -> list[StayInfoModel]:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    StayInfoOrm
                ).filter(
                    StayInfoOrm.stay_seq > offset
                ).order_by(StayInfoOrm.stay_seq)
                .limit(limit)
            )
            return stay_orm_to_pydantic_model(result)


async def get_stay_info_with_review_for_user_seq_limit_offset(
        user_seq: int,
        offset: int,
        limit: int
) -> list[StayInfoWishReviewModel]:
    async with postgres_client.session() as session:
        try:
            get_stay_info_with_wish_review_query = text(dedent(f"""
            WITH review_stat AS (
                SELECT 
                    stay_seq,
                    count(review_seq) AS review_count,
                    AVG(review_score)::numeric(10,1) AS review_score_average
                FROM public.review
                GROUP BY stay_seq
            )
            SELECT
                si.stay_seq AS stay_seq, stay_name, manager, contact_number, address,
                TO_CHAR(check_in_time, 'HH24:MI') AS check_in_time, TO_CHAR(check_out_time, 'HH24:MI') AS check_out_time,
                description, refund_policy, homepage_url, reservation_info, parking_available, latitude,
                longitude, facilities_detail, food_beverage_area,
                CASE WHEN w.stay_seq IS NOT NULL THEN True ELSE False END AS wish_state,
                rs.review_count, rs.review_score_average
            FROM public.stay_info si
            LEFT JOIN public.wish w ON si.stay_seq = w.stay_seq AND w.user_seq = {user_seq}
            JOIN review_stat rs ON si.stay_seq = rs.stay_seq
            ORDER BY si.stay_seq
            LIMIT {limit} OFFSET {offset}
            ;
            """))

            result = await session.execute(get_stay_info_with_wish_review_query)

            stay_info_list = [StayInfoWishReviewModel(**row) for row in result.mappings().all()]
            return stay_info_list

        except Exception as e:
            print(e)
            return []
