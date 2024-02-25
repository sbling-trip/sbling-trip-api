import datetime
from textwrap import dedent

from api_python.app.common.client.postgres.postgres_client import postgres_client
from sqlalchemy import text

from api_python.app.common.exceptions import get_reservation_count_exception


async def get_reservation_count_by_room_seq(room_seq: int, check_in_date: datetime.date, check_out_date: datetime.date):
    async with postgres_client.session() as session:
        try:
            get_reservation_count_query = text(dedent(f"""
            SELECT room_seq, COUNT(*) AS reservation_count
            FROM public.reservations
            WHERE room_seq = {room_seq}
            AND (
                (check_in_date <= '{check_in_date}' AND check_in_date < '{check_out_date}') OR
                (check_out_date > '{check_in_date}' AND check_out_date <= '{check_out_date}')
                )
            GROUP BY room_seq
            """))
            result = await session.execute(get_reservation_count_query)
            reservation_count = result.scalar()
            return reservation_count if reservation_count else 0
        except Exception as e:
            raise get_reservation_count_exception(str(e))
