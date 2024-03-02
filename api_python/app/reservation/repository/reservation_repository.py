import datetime
from textwrap import dedent

from api_python.app.common.client.postgres.postgres_client import postgres_client
from sqlalchemy import text, TextClause

from api_python.app.common.exceptions import get_reservation_available_stay_exception
from api_python.app.stay.model.stay_model import UserResponseStayInfoModel, convert_stay_info_model_to_response, \
    StayInfoWishReviewModel


def reservation_stay_sql_generator(
        user_seq: int,
        offset: int,
        limit: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
        stay_type: int | None = None,
        stay_seq: int | None = None
) -> TextClause:
    return text(dedent(f"""
        WITH available_room_info AS (
             SELECT room_seq, stay_seq, room_available_count, min_people, max_people, room_price, additional_charge, child_additional_charge
             FROM room_info
             WHERE 
             min_people <= {adult_guest_count + child_guest_count}
             AND max_people >= {adult_guest_count + child_guest_count}
             {f"AND stay_seq = {stay_seq}" if stay_seq else ""}
             {f"AND stay_type = {stay_type}" if stay_type else ""}
         ),
        pre_reservation_count AS(
            SELECT r.room_seq, COUNT(*) AS reservation_count FROM available_room_info ari
            JOIN public.reservations r ON ari.room_seq = r.room_seq
            WHERE (r.check_in_date >= '{check_in_date}' AND r.check_in_date < '{check_out_date}') OR
                  (r.check_out_date > '{check_in_date}' AND r.check_out_date <= '{check_out_date}')
            GROUP BY r.room_seq
        ),
        available_room_data AS (
        SELECT ari.room_seq, ari.stay_seq, GREATEST(ari.room_available_count - prc.reservation_count, 0) AS available_room_count
        FROM available_room_info ari JOIN pre_reservation_count prc ON ari.room_seq = prc.room_seq
        ),
        review_stat AS (
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
            JOIN
                available_room_data ard ON si.stay_seq = ard.stay_seq
            WHERE
                ri.room_seq = (
                    SELECT room_seq
                    FROM room_info
                    WHERE stay_seq = si.stay_seq
                    ORDER BY room_price + additional_charge * {adult_guest_count} + child_additional_charge * {child_guest_count}
                    LIMIT 1
                )
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
        ORDER BY si.stay_seq
        LIMIT {limit} OFFSET {offset}
    """))


async def get_reservation_stay_repository(
        user_seq: int,
        offset: int,
        limit: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
        stay_type: int | None = None
) -> list[UserResponseStayInfoModel]:
    async with postgres_client.session() as session:
        try:
            get_reservation_stay_query = reservation_stay_sql_generator(
                user_seq=user_seq,
                offset=offset,
                limit=limit,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                adult_guest_count=adult_guest_count,
                child_guest_count=child_guest_count,
                stay_type=stay_type

            )
            result = await session.execute(get_reservation_stay_query)
            stay_model_list = [convert_stay_info_model_to_response(StayInfoWishReviewModel(**row))
                               for row in result.mappings().all()]
            return stay_model_list
        except Exception as e:
            raise get_reservation_available_stay_exception(str(e))
