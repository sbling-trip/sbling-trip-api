from typing import Tuple, List

from sqlalchemy import select, ChunkedIteratorResult

from api_python.app.common.client.postgres.postgres_client import postgres_client

from api_python.app.users.model.user_model import UserModel, UserOrm


def user_orm_to_pydantic_model(result: ChunkedIteratorResult[Tuple[UserOrm]]) -> List[UserModel]:
    return [UserModel.model_validate(orm) for orm in result.scalars().all()]


async def find_by_external_id(external_id: str) -> list[UserModel]:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    UserOrm
                ).filter(
                    UserOrm.external_id == external_id
                )
            )
            # 만약 값이 있으면 리턴 없으면 None
            return user_orm_to_pydantic_model(result)


async def insert_user(user: UserModel) -> bool:
    async with postgres_client.session() as session:
        async with session.begin():
            user_orm = UserOrm(
                user_seq=user.user_seq,
                email=user.email,
                external_id=user.external_id,
                first_name=user.first_name,
                last_name=user.last_name,
                oauth_provider=user.oauth_provider,
                logo_url=user.logo_url,
                expired_at=user.expired_at,
                created_at=user.created_at,
                logged_in_at=user.logged_in_at,
            )
            session.add(user_orm)
            await session.flush()
    return True


async def insert_user_from_orm(user: UserOrm) -> bool:
    async with postgres_client.session() as session:
        async with session.begin():
            session.add(user)
            await session.flush()
    return True