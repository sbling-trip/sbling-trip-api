from typing import Tuple, List

from sqlalchemy import select, ChunkedIteratorResult

from api_python.app.common.client.postgres.postgres_client import postgres_client
from api_python.app.room.model.room_model import RoomOrm, RoomModel


def room_orm_to_pydantic_model(result: ChunkedIteratorResult[Tuple[RoomOrm]]) -> List[RoomModel]:
    return [RoomModel.model_validate(orm) for orm in result.scalars().all()]


async def find_by_stay_seq_room_model(stay_seq: int) -> List[RoomModel]:
    async with postgres_client.session() as session:
        async with session.begin():
            result = await session.execute(
                select(RoomOrm).filter(RoomOrm.stay_seq == stay_seq)
            )
            return room_orm_to_pydantic_model(result)
