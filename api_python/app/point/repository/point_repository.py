from datetime import datetime
from api_python.app.common.kst_time import get_kst_time_now
from typing import Tuple, List
from textwrap import dedent
from api_python.app.common.exceptions import get_point_exception, update_point_exception

from sqlalchemy import text

from api_python.app.common.client.postgres.postgres_client import postgres_client

from api_python.app.point.model.point_model import PointModel


async def update_point(user_seq: int, point: int) -> bool:
    point_model = await find_by_user_seq_point_model(user_seq)
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                update_point = text(
                    dedent(
                        f"""
                            UPDATE points
                            SET
                            point = {point_model.point + point},
                            updated_at = '{get_kst_time_now()}'
                            WHERE
                            user_seq = {user_seq};
                           """
                    )
                )
                await session.execute(update_point)
                return True

        except Exception as e:
            await session.rollback()
            raise update_point_exception(str(e))


async def find_by_user_seq_point_model(user_seq: int) -> PointModel:
    async with postgres_client.session() as session:
        try:
            get_point = text(
                dedent(
                    f"""
                     SELECT *
                     FROM points
                     WHERE user_seq = {user_seq};
                     """
                )
            )

            result = await session.execute(get_point)

            result_model = result.mappings().fetchone()
            point = PointModel(**result_model)
            return point

        except Exception as e:
            raise get_point_exception(str(e))
