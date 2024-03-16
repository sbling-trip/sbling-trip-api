import datetime
from textwrap import dedent

from api_python.app.common.client.postgres.postgres_client import postgres_client
from sqlalchemy import text, TextClause, dialects

from api_python.app.common.exceptions import get_reservation_available_stay_exception, cancel_reservation_exception, \
    get_reservation_available, update_reservation_exception, \
    get_reservation_room_list_stay_exception
from api_python.app.common.kst_time import get_kst_time_now
from api_python.app.reservation.model.reservation_model import UserResponseReservationInfoModel, ReservationOrm
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
            WHERE ((r.check_in_date >= '{check_in_date}' AND r.check_in_date < '{check_out_date}') OR
                  (r.check_out_date > '{check_in_date}' AND r.check_out_date <= '{check_out_date}'))
                  AND r.reservation_status != 'cancelled'
            GROUP BY r.room_seq
        ),
        available_room_data AS (
        SELECT ari.room_seq, ari.stay_seq, GREATEST(ari.room_available_count - COALESCE(prc.reservation_count, 0), 0) AS available_room_count
        FROM available_room_info ari 
        LEFT JOIN pre_reservation_count prc ON ari.room_seq = prc.room_seq
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
                (ri.room_price +
                    CASE
                      WHEN ({adult_guest_count} - ri.min_people) >= 0 THEN
                        ({adult_guest_count} - ri.min_people) * ri.additional_charge + {child_guest_count} * ri.child_additional_charge
                      ELSE
                        ({child_guest_count} + {adult_guest_count} - ri.min_people) * ri.child_additional_charge
                    END) 
                    AS minimum_room_price
            FROM
                stay_info si
            JOIN
                room_info ri ON si.stay_seq = ri.stay_seq
            JOIN
                available_room_data ard ON si.stay_seq = ard.stay_seq
            WHERE
                ri.room_seq = (
                    SELECT room_seq
                    FROM room_info ri
                    WHERE stay_seq = si.stay_seq
                    ORDER BY ri.room_price +
                    CASE
                      WHEN ({adult_guest_count} - ri.min_people) >= 0 THEN
                        ({adult_guest_count} - ri.min_people) * ri.additional_charge + {child_guest_count} * ri.child_additional_charge
                      ELSE
                        ({child_guest_count} + {adult_guest_count} - ri.min_people) * ri.child_additional_charge
                    END
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


async def get_reservation_room_list(
        user_seq: int,
        reservation_status: list[str]
) -> list[UserResponseReservationInfoModel]:
    async with postgres_client.session() as session:
        try:
            formatted_status = ', '.join(f"'{status}'" for status in reservation_status)
            get_reservation_room_list_query = text(dedent(f"""
                SELECT 
                    r.reservation_seq,
                    r.stay_seq,
                    r.room_seq,
                    ri.stay_name,
                    ri.room_name,
                    r.check_in_date,
                    r.check_out_date,
                    r.adult_guest_count,
                    r.child_guest_count,
                    r.reservation_status,
                    r.booking_date,
                    r.payment_status,
                    r.special_requests,
                    r.payment_price
                FROM reservations r
                JOIN room_info ri ON r.room_seq = ri.room_seq
                WHERE reservation_status IN ({formatted_status}) AND user_seq = {user_seq}
            """))
            result = await session.execute(get_reservation_room_list_query)
            room_list = [UserResponseReservationInfoModel(**row) for row in result.mappings().all()]
            return room_list
        except Exception as e:
            raise get_reservation_room_list_stay_exception(str(e))


async def add_reservation_repository(
        user_seq: int,
        stay_seq: int,
        room_seq: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
        special_requests: str,
        payment_price: int
) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                request_timestamp = get_kst_time_now()
                stmt = dialects.postgresql.insert(ReservationOrm).values(
                    user_seq=user_seq,
                    stay_seq=stay_seq,
                    room_seq=room_seq,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    adult_guest_count=adult_guest_count,
                    child_guest_count=child_guest_count,
                    reservation_status='pending',
                    booking_date=request_timestamp,
                    payment_status='unpaid',
                    special_requests=special_requests,
                    created_at=request_timestamp,
                    updated_at=request_timestamp,
                    payment_price=payment_price
                ).on_conflict_do_update(
                    index_elements=[
                        "stay_seq",
                        "room_seq",
                        "user_seq",
                        "check_in_date",
                        "check_out_date",
                        "adult_guest_count",
                        "child_guest_count"
                    ],
                    set_={"booking_date": request_timestamp}
                )
                await session.execute(stmt)
                return True
        except Exception as e:
            raise get_reservation_available_stay_exception(str(e))


async def is_validate_stay_room_seq(
        stay_seq: int,
        room_seq: int
) -> bool:
    async with postgres_client.session() as session:
        try:
            stmt = text(dedent(f"""
                SELECT COUNT(*) AS count
                FROM room_info
                WHERE stay_seq = {stay_seq} AND room_seq = {room_seq}
            """))
            result = await session.execute(stmt)
            return result.scalar() > 0
        except Exception as e:
            raise get_reservation_available(str(e))


async def is_reservation_available(
        room_seq: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
) -> bool:
    async with postgres_client.session() as session:
        try:
            stmt = text(dedent(f"""
            WITH available_room_info AS (
                 SELECT room_seq
                 FROM room_info
                 WHERE 
                 min_people <= {adult_guest_count + child_guest_count}
                 AND max_people >= {adult_guest_count + child_guest_count}
                 {f"AND room_seq = {room_seq}"}
             ),
            pre_reservation_count AS(
                SELECT r.room_seq, COUNT(*) AS reservation_count FROM available_room_info ari
                JOIN public.reservations r ON ari.room_seq = r.room_seq
                WHERE ((r.check_in_date >= '{check_in_date}' AND r.check_in_date < '{check_out_date}') OR
                      (r.check_out_date > '{check_in_date}' AND r.check_out_date <= '{check_out_date}'))
                      AND r.reservation_status != 'cancelled'
                WHERE r.room_seq = {room_seq}
                GROUP BY r.room_seq
            ),
            available_room_data AS (
                SELECT GREATEST(ari.room_available_count - COALESCE(prc.reservation_count, 0), 0) AS available_room_count
                FROM available_room_info ari 
                LEFT JOIN pre_reservation_count prc ON ari.room_seq = prc.room_seq
            )
            SELECT COUNT(*) AS count FROM available_room_data
            WHERE available_room_count > 0
            """))
            result = await session.execute(stmt)
            return result.scalar() > 0
        except Exception as e:
            raise get_reservation_available(str(e))


async def update_reservation_payment(
        reservation_seq: int
) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                stmt = dialects.postgresql.insert(ReservationOrm).values(
                    reservation_seq=reservation_seq,
                ).on_conflict_do_update(
                    index_elements=['reservation_seq'],
                    set_={'reservation_status': 'confirmed',
                          'payment_status': 'paid',
                          'updated_at': get_kst_time_now()}
                )
                await session.execute(stmt)
                return True
        except Exception as e:
            raise update_reservation_exception(str(e))


async def cancel_reservation(
        reservation_seq: int
) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                stmt = dialects.postgresql.insert(ReservationOrm).values(
                    reservation_seq=reservation_seq,
                ).on_conflict_do_update(
                    index_elements=['reservation_seq'],
                    set_={'reservation_status': 'cancelled',
                          'updated_at': get_kst_time_now()}
                )
                await session.execute(stmt)
                return True
        except Exception as e:
            raise cancel_reservation_exception(str(e))
