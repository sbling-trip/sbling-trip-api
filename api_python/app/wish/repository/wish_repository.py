from textwrap import dedent

from api_python.app.common.client.postgres.postgres_client import postgres_client
from sqlalchemy import text, dialects

from api_python.app.common.exceptions import add_wish_exception, delete_wish_exception, get_wish_exception
from api_python.app.common.kst_time import get_kst_time_now
from api_python.app.stay.model.stay_model import StayInfoWishModel
from api_python.app.wish.model.wish_model import WishOrm


async def insert_by_user_seq_stay_seq(user_seq: int, stay_seq: int) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                # 만약 이미 찜한 숙소라면 N으로 변경
                stmt = dialects.postgresql.insert(WishOrm).values(
                    user_seq=user_seq,
                    stay_seq=stay_seq,
                    state='Y',
                    wished_at=get_kst_time_now(),
                    modified_at=get_kst_time_now()
                ).on_conflict_do_update(
                    index_elements=['user_seq', 'stay_seq'],
                    set_={'state': 'Y', 'modified_at': get_kst_time_now()}
                )
                await session.execute(stmt)
                return True
        except Exception as e:
            raise add_wish_exception(str(e))


async def update_by_user_seq_stay_seq(user_seq: int, stay_seq) -> bool:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                # 만약 이미 찜한 숙소라면 N으로 변경
                stmt = dialects.postgresql.insert(WishOrm).values(
                    user_seq=user_seq,
                    stay_seq=stay_seq,
                    state='N',
                    wished_at=get_kst_time_now(),
                    modified_at=get_kst_time_now()
                ).on_conflict_do_update(
                    index_elements=['user_seq', 'stay_seq'],
                    set_={'state': 'N', 'modified_at': get_kst_time_now()}
                )
                await session.execute(stmt)
                return True
        except Exception as e:
            raise delete_wish_exception(str(e))


async def get_stay_info_for_user_wish(
        user_seq: int,
        offset: int,
        limit: int
) -> list[StayInfoWishModel]:
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                get_stay_info_with_wish_query = text(dedent(f"""
                SELECT 
                    si.stay_seq AS stay_seq, stay_name, manager, contact_number, address,
                    TO_CHAR(check_in_time, 'HH24:MI') AS check_in_time, TO_CHAR(check_out_time, 'HH24:MI') AS check_out_time,
                    description, refund_policy, homepage_url, reservation_info, parking_available, latitude,
                    longitude, facilities_detail, food_beverage_area, state AS wish_state
                FROM public.stay_info si
                JOIN public.wish w ON si.stay_seq = w.stay_seq AND w.user_seq = {user_seq}
                ORDER BY si.stay_seq
                LIMIT {limit} OFFSET {offset}
                ;
                """))
                result = await session.execute(get_stay_info_with_wish_query)

                stay_info_list = [StayInfoWishModel(**row) for row in result.mappings().all()]
                return stay_info_list
        except Exception as e:
            raise get_wish_exception(str(e))


async def get_stay_info_with_for_user_seq_limit_offset(
        user_seq: int,
        offset: int,
        limit: int
) -> list[StayInfoWishModel]:
    async with postgres_client.session() as session:
        try:
            get_stay_info_with_wish_query = text(dedent(f"""
            SELECT 
                si.stay_seq AS stay_seq, stay_name, manager, contact_number, address,
                TO_CHAR(check_in_time, 'HH24:MI') AS check_in_time, TO_CHAR(check_out_time, 'HH24:MI') AS check_out_time,
                description, refund_policy, homepage_url, reservation_info, parking_available, latitude,
                longitude, facilities_detail, food_beverage_area,
                CASE WHEN w.stay_seq IS NOT NULL THEN True ELSE False END AS wish_state
            FROM public.stay_info si
            LEFT JOIN public.wish w ON si.stay_seq = w.stay_seq AND w.user_seq = {user_seq}
            ORDER BY si.stay_seq
            LIMIT {limit} OFFSET {offset}
            ;
            """))

            result = await session.execute(get_stay_info_with_wish_query)

            stay_info_list = [StayInfoWishModel(**row) for row in result.mappings().all()]
            return stay_info_list

        except Exception as e:
            raise get_wish_exception(str(e))
