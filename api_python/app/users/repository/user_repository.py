from typing import Tuple, List

from sqlalchemy import select, ChunkedIteratorResult

from api_python.app.common.client.postgres.postgres_client import postgres_client

from api_python.app.users.model.user_model import UserModel, UserOrm


def user_orm_to_pydantic_model(result: ChunkedIteratorResult[Tuple[UserOrm]]) -> List[UserModel]:
    return [UserModel.model_validate(orm) for orm in result.scalars().all()]


async def find_by_external_id(external_id: str) -> UserModel:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(UserOrm).filter(UserOrm.external_id == external_id)
            )
            orm = result.scalars().first()
            return UserModel.model_validate(orm) if orm else None


async def insert_user_from_orm(user: UserOrm) -> bool:
    async with postgres_client.session() as session:
        async with session.begin():
            session.add(user)
            await session.flush()
    return True
