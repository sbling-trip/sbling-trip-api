from datetime import datetime
from api_python.app.common.kst_time import get_kst_time_now
from typing import Tuple, List
from textwrap import dedent
from api_python.app.common.exceptions import get_user_exception, update_user_exception

from sqlalchemy import text

from api_python.app.common.client.postgres.postgres_client import postgres_client

from api_python.app.user.model.user_model import UserModel


async def update_user(
    user_seq: int,
    user_name: str | None,
    location_agree: bool | None,
    marketing_agree: bool | None,
) -> bool:
    user = await find_by_user_seq_user_model(user_seq)
    async with postgres_client.session() as session:
        try:
            async with session.begin():
                update_user = text(
                    dedent(
                        f"""
                            UPDATE users 
                                SET
                                user_name = '{user.user_name if user_name == None else user_name}',
                                location_agree = {user.location_agree if location_agree == None else location_agree},
                                marketing_agree = {user.marketing_agree if marketing_agree == None else marketing_agree},
                                updated_at = '{get_kst_time_now()}'
                                WHERE
                                user_seq = {user_seq};
                           """
                    )
                )
                await session.execute(update_user)
                return True

        except Exception as e:
            await session.rollback()
            raise update_user_exception(str(e))


async def find_by_user_seq_user_model(user_seq: int) -> UserModel:
    async with postgres_client.session() as session:
        try:
            get_user_me = text(
                dedent(
                    f"""
                     SELECT 
                        users.user_seq,
                        users.user_name,
                        users.user_status,
                        accounts.email AS user_email,
                        users.gender,
                        users.birth_at,
                        users.created_at,
                        users.updated_at,
                        users.deleted_at,
                        users.image,
                        users.service_agree,
                        users.location_agree,
                        users.marketing_agree
                     FROM users
                     JOIN accounts ON users.user_seq = accounts.user_seq
                     WHERE users.user_seq = {user_seq}
                     """
                )
            )

            result = await session.execute(get_user_me)

            result_model = result.mappings().fetchone()
            user = UserModel(**result_model)
            return user

        except Exception as e:
            raise get_user_exception(str(e))
