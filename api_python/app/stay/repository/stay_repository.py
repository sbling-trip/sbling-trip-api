from typing import Tuple

from sqlalchemy import select, ChunkedIteratorResult

from api_python.app.common.client.postgres.postgres_client import postgres_client
from api_python.app.stay.model.stay_model import StayInfoModel, StayInfoOrm, StayInfoWishModel


def stay_orm_to_pydantic_model(result: ChunkedIteratorResult[Tuple[StayInfoOrm]]) -> list[StayInfoModel]:
    return [StayInfoModel.model_validate(orm) for orm in result.scalars().all()]


def stay_orm_to_wish_pydantic_model(result: ChunkedIteratorResult[Tuple[StayInfoOrm]]) -> list[StayInfoWishModel]:
    return [StayInfoWishModel.model_validate(orm) for orm in result.scalars().all()]


async def find_all() -> list[StayInfoModel]:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    StayInfoOrm
                )
            )
            return stay_orm_to_pydantic_model(result)


async def find_by_seq_limit_offset(offset: int, limit: int) -> list[StayInfoModel]:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(
                    StayInfoOrm
                ).filter(
                    StayInfoOrm.stay_seq > offset
                ).order_by(StayInfoOrm.stay_seq)
                .limit(limit)
            )
            return stay_orm_to_pydantic_model(result)
