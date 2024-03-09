from typing import Tuple, List
from textwrap import dedent

from sqlalchemy import select, ChunkedIteratorResult, TextClause

from api_python.app.common.client.postgres.postgres_client import postgres_client
from api_python.app.common.exceptions import get_stay_info_exception
from api_python.app.stay.model.stay_model import StayInfoModel, StayInfoOrm, StayInfoWishReviewModel, \
    convert_stay_info_model_to_response, UserResponseStayInfoModel
from sqlalchemy import text


def stay_sql_query_generator(
        user_seq: int,
        offset: int,
        limit: int,
        adult_guest_count: int = 0,
        child_guest_count: int = 0,
        stay_seq: int | None = None,
        stay_type: int | None = None,
        order_by_list: List[str] | None = None
) -> TextClause:
    stay_sql = text(dedent(f"""
        WITH review_stat AS (
            SELECT 
                stay_seq,
                count(review_seq) AS review_count,
                AVG(review_score)::numeric(10,1) AS review_score_average
            FROM public.review
            WHERE exposed = true
            GROUP BY stay_seq
        ),
        room_data AS (
            SELECT
                si.stay_seq,
                ri.room_image_url_list,
                room_price + additional_charge * {adult_guest_count} + child_additional_charge * {child_guest_count} AS minimum_room_price
            FROM
                stay_info si
            JOIN
                room_info ri ON si.stay_seq = ri.stay_seq
            WHERE
                room_price + additional_charge * {adult_guest_count} + child_additional_charge * {child_guest_count} = (
                    SELECT MIN(room_price + additional_charge * {adult_guest_count} + child_additional_charge * {child_guest_count})
                    FROM room_info ri2
                    WHERE ri2.stay_seq = si.stay_seq
                ) 
                {f"AND ri.stay_type = {stay_type}" if stay_type else ""}
        )
        SELECT
            si.stay_seq AS stay_seq, stay_name, manager, contact_number, address,
            TO_CHAR(check_in_time, 'HH24:MI') AS check_in_time, TO_CHAR(check_out_time, 'HH24:MI') AS check_out_time,
            description, refund_policy, homepage_url, reservation_info, parking_available, latitude,
            longitude, facilities_detail, food_beverage_area,
            CASE WHEN w.stay_seq IS NOT NULL AND w.state = 'Y' THEN True ELSE False END AS wish_state,
            rs.review_count, rs.review_score_average, rd.room_image_url_list, rd.minimum_room_price
        FROM public.stay_info si
        LEFT JOIN public.wish w ON si.stay_seq = w.stay_seq AND w.user_seq = {user_seq}
        JOIN review_stat rs ON si.stay_seq = rs.stay_seq
        JOIN room_data rd ON si.stay_seq = rd.stay_seq
        WHERE 1 = 1
        {f"AND si.stay_seq = {stay_seq}" if stay_seq else ""}
        ORDER BY {f"si.stay_seq ASC" if order_by_list is None else f"{' DESC, '.join(order_by_list)} DESC"}
        LIMIT {limit} OFFSET {offset}
        ;
        """))
    return stay_sql


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
        offset: int = 0,
        limit: int = 20,
        adult_guest_count: int = 0,
        child_guest_count: int = 0,
        stay_type: int | None = None,
        order_by_list: List[str] | None = None
) -> list[UserResponseStayInfoModel]:
    async with postgres_client.session() as session:
        try:
            get_stay_info_with_wish_review_query = stay_sql_query_generator(user_seq=user_seq, offset=offset,
                                                                            limit=limit,
                                                                            adult_guest_count=adult_guest_count,
                                                                            child_guest_count=child_guest_count,
                                                                            stay_seq=None, stay_type=stay_type,
                                                                            order_by_list=order_by_list)

            result = await session.execute(get_stay_info_with_wish_review_query)
            stay_model_list = [convert_stay_info_model_to_response(StayInfoWishReviewModel(**row))
                               for row in result.mappings().all()]
            return stay_model_list

        except Exception as e:
            raise get_stay_info_exception(str(e))


async def get_stay_info_by_stay_seq(user_seq: int, stay_seq: int) -> UserResponseStayInfoModel:
    async with postgres_client.session() as session:
        try:
            get_stay_info_with_wish_review_query = stay_sql_query_generator(user_seq=user_seq, offset=0, limit=1,
                                                                            adult_guest_count=0, child_guest_count=0,
                                                                            stay_seq=stay_seq)

            result = await session.execute(get_stay_info_with_wish_review_query)

            result_model = result.mappings().fetchone()
            stay_info_wish_review = convert_stay_info_model_to_response(StayInfoWishReviewModel(**result_model))
            return stay_info_wish_review

        except Exception as e:
            raise get_stay_info_exception(str(e))
