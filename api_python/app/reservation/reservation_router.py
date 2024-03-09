import datetime
from typing import Annotated, List

from fastapi import APIRouter

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.depends.depends import user_seq_dependency
from api_python.app.reservation.model.reservation_model import UserResponseReservationInfoModel
from api_python.app.reservation.service.reservation_service import get_reservation_room_list_service

reservation_router = APIRouter(
    prefix="/reservation",
)


@reservation_router.get(
    "/list",
    summary="예약 목록 조회",
    description="예약 목록을 조회합니다.",
    tags=["예약"],
)
async def get_reservation_list(
    user_seq: Annotated[int, user_seq_dependency],
) -> ApiResponse[List[UserResponseReservationInfoModel]]:
    result = await get_reservation_room_list_service(
        user_seq=user_seq,
        reservation_status=["confirmed", "pending"]
    )
    return ApiResponse.success(result)


@reservation_router.get(
    "/list/cancel",
    summary="예약 목록 조회",
    description="취소한 예약 목록을 조회합니다.",
    tags=["예약"],
)
async def get_reservation_list(
    user_seq: Annotated[int, user_seq_dependency],
) -> ApiResponse[List[UserResponseReservationInfoModel]]:
    result = await get_reservation_room_list_service(
        user_seq,
        reservation_status=["cancelled"]
    )
    return ApiResponse.success(result)
