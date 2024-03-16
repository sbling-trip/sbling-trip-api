from typing import Annotated

from fastapi import Depends

from api_python.app.common.exceptions import update_point_exception
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


async def point_payment_service(
    user_seq: int,
    payment_price: int,
) -> bool:
    point_model = await find_by_user_seq_point_model(user_seq=user_seq)

    if point_model.point < payment_price:
        raise update_point_exception(error_message="결제를 위한 포인트가 부족합니다.")

    await update_point(user_seq=user_seq, point=-payment_price)

    return True
