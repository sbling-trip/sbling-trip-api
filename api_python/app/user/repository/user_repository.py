from datetime import datetime
from typing import Tuple, List

from sqlalchemy import select, ChunkedIteratorResult, update

from api_python.app.common.client.postgres.postgres_client import postgres_client

from api_python.app.user.model.user_model import UserModel, UserOrm, UserResponseModel


def user_orm_to_pydantic_model(result: ChunkedIteratorResult[Tuple[UserOrm]]) -> List[UserModel]:
    return [UserModel.model_validate(orm) for orm in result.scalars().all()]


async def find_by_external_id_user_model(external_id: str) -> UserModel:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(UserOrm).filter(UserOrm.external_id == external_id)
            )
            orm = result.scalars().first()
            return UserModel.model_validate(orm) if orm else None


async def find_by_external_id_user_response_model(external_id: str) -> UserResponseModel:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(UserOrm).filter(UserOrm.external_id == external_id)
            )
            orm = result.scalars().first()
            return UserResponseModel.model_validate(orm) if orm else None


async def insert_user_from_orm(user: UserOrm) -> bool:
    async with postgres_client.session() as session:
        async with session.begin():
            session.add(user)
            await session.flush()
    return True


async def update_user_expiration(external_id: str, update_data: datetime) -> bool:
    async with postgres_client.session() as session:
        async with session.begin():
            await session.execute(
                update(UserOrm).where(UserOrm.external_id == external_id).values(expired_at=update_data)
            )
    return True


async def update_user_login_at(external_id: str, last_login_at: datetime) -> bool:
    async with postgres_client.session() as session:
        async with session.begin():
            await session.execute(
                update(UserOrm).where(UserOrm.external_id == external_id).values(last_login_at=last_login_at)
            )
    return True
