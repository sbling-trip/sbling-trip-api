from datetime import datetime, date
from textwrap import dedent
from typing import Tuple, List

from sqlalchemy import select, ChunkedIteratorResult, TextClause, text

from api_python.app.common.client.postgres.postgres_client import postgres_client
from api_python.app.common.exceptions import get_room_info_exception
from api_python.app.room.model.room_model import RoomOrm, RoomModel, \
    UserAvailableRoomModel, convert_available_room_model_to_response, \
    UserResponseAvailableRoomModel


def reservation_room_sql_generator(
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
        stay_seq: int | None = None
) -> TextClause:
    return text(dedent(f"""
        WITH available_room_info AS (
             SELECT 
                ri.room_seq,
                ri.stay_seq,
                ri.stay_name,
                ri.stay_type,
                ri.room_name,
                ri.room_type,
                ri.room_price + CASE
                      WHEN ({adult_guest_count} - ri.min_people) >= 0 THEN
                        ({adult_guest_count} - ri.min_people) * ri.additional_charge + {child_guest_count} * ri.child_additional_charge
                      ELSE
                        ({child_guest_count} + {adult_guest_count} - ri.min_people) * ri.child_additional_charge
                    END AS room_price,
                ri.room_available_count,
                ri.room_image_url_list,
                ri.ott_service,
                ri.toilet_option,
                ri.room_option,
                ri.special_room_option,
                ri.min_people,
                ri.max_people,
                ri.additional_charge,
                ri.child_discount_price,
                ri.child_additional_charge
             FROM room_info ri
             WHERE 
             min_people <= {adult_guest_count + child_guest_count}
             AND max_people >= {adult_guest_count + child_guest_count}
             {f"AND ri.stay_seq = {stay_seq}" if stay_seq else ""}
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
        SELECT ari.room_seq, GREATEST(ari.room_available_count - COALESCE(prc.reservation_count, 0), 0) AS available_room_count
        FROM available_room_info ari 
        LEFT JOIN pre_reservation_count prc ON ari.room_seq = prc.room_seq
        )
        SELECT
            ri.room_seq,
            stay_seq,
            stay_name,
            stay_type,
            room_name,
            room_type,
            room_price,
            room_available_count,
            room_image_url_list,
            ott_service,
            toilet_option,
            room_option,
            special_room_option,
            {adult_guest_count} AS adult_guest_count,
            {child_guest_count} AS child_guest_count
        FROM
            available_room_info ri
        JOIN
            available_room_data ard ON ri.room_seq = ard.room_seq 
        WHERE 1 = 1
    """))


def room_orm_to_pydantic_model(result: ChunkedIteratorResult[Tuple[RoomOrm]]) -> List[RoomModel]:
    return [RoomModel.model_validate(orm) for orm in result.scalars().all()]


async def find_by_stay_seq_room_model(stay_seq: int) -> List[RoomModel]:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                result = await session.execute(
                    select(RoomOrm).filter(RoomOrm.stay_seq == stay_seq)
                )
                return room_orm_to_pydantic_model(result)
        except Exception as e:
            raise get_room_info_exception(str(e))


async def get_available_room_info_by_stay_seq(
        stay_seq: int,
        check_in_date: date,
        check_out_date: date,
        adult_guest_count: int,
        child_guest_count: int
) -> List[UserResponseAvailableRoomModel]:
    async with postgres_client.session() as session:
        try:
            get_room_info_query = reservation_room_sql_generator(
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                adult_guest_count=adult_guest_count,
                child_guest_count=child_guest_count,
                stay_seq=stay_seq
            )
            print(get_room_info_query)

            result = await session.execute(get_room_info_query)
            room_model_list = [convert_available_room_model_to_response(UserAvailableRoomModel(**row))
                               for row in result.mappings().all()]
            return room_model_list
        except Exception as e:
            raise get_room_info_exception(str(e))
