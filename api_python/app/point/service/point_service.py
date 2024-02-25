from typing import Annotated

from fastapi import Depends


from api_python.app.point.model.point_model import PointModel
from api_python.app.point.repository.point_repository import (
    find_by_user_seq_point_model,
    update_point,
)


async def get_point_service(
    user_seq: int,
) -> PointModel:
    return await find_by_user_seq_point_model(
        user_seq=user_seq,
    )


async def update_point_service(user_seq: int, point: int) -> bool:
    await update_point(user_seq=user_seq, point=point)

    return True
