from typing import Annotated, List

from fastapi import APIRouter, Query

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.config.phase import IS_LOCAL
from api_python.app.common.depends.depends import user_seq_dependency, user_seq_dependency_optional
from api_python.app.reservation.model.reservation_model import UserResponseReservationInfoModel, \
    ReservationRequestModel, ReservationSeqModel
from api_python.app.reservation.service.reservation_service import get_reservation_room_list_service, \
    add_reservation_service, cancel_reservation_service, reservation_repayment_service

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
        user_seq: Annotated[int, user_seq_dependency_optional if IS_LOCAL else user_seq_dependency],
) -> ApiResponse[List[UserResponseReservationInfoModel]]:
    result = await get_reservation_room_list_service(
        user_seq=user_seq,
        reservation_status=["confirmed", "pending"]
    )
    return ApiResponse.success(result)


@reservation_router.get(
    "/list/cancel",
    summary="취소한 예약 목록 조회",
    description="취소한 예약 목록을 조회합니다.",
    tags=["예약"],
)
async def get_reservation_list(
        user_seq: Annotated[int, user_seq_dependency_optional if IS_LOCAL else user_seq_dependency],
) -> ApiResponse[List[UserResponseReservationInfoModel]]:
    result = await get_reservation_room_list_service(
        user_seq,
        reservation_status=["cancelled"]
    )
    return ApiResponse.success(result)


@reservation_router.post(
    "/add",
    summary="예약 추가",
    description="예약을 추가합니다.",
    tags=["예약"],
)
async def add_reservation(
        user_seq: Annotated[int, user_seq_dependency_optional if IS_LOCAL else user_seq_dependency],
        reservation_request_model: ReservationRequestModel,
) -> ApiResponse[str]:
    await add_reservation_service(
        user_seq=user_seq,
        stay_seq=reservation_request_model.stay_seq,
        room_seq=reservation_request_model.room_seq,
        check_in_date=reservation_request_model.check_in_date,
        check_out_date=reservation_request_model.check_out_date,
        adult_guest_count=reservation_request_model.adult_guest_count,
        child_guest_count=reservation_request_model.child_guest_count,
        special_requests=reservation_request_model.special_requests,
        payment_price=reservation_request_model.payment_price
    )
    return ApiResponse.success("Success")


@reservation_router.delete(
    "/cancel",
    summary="예약 취소",
    description="예약을 취소합니다.",
    tags=["예약"],
)
async def cancel_reservation(
        user_seq: Annotated[int, user_seq_dependency],
        reservation_seq: Annotated[int, Query(alias="reservationSeq", description="예약 취소할 seq")]
) -> ApiResponse[str]:
    await cancel_reservation_service(
        user_seq=user_seq,
        reservation_seq=reservation_seq
    )
    return ApiResponse.success("Success")


@reservation_router.post(
    "/retry-payment",
    summary="예약 재시도",
    description="예약을 재시도합니다.",
    tags=["예약"],
)
async def retry_payment(
        user_seq: Annotated[int, user_seq_dependency],
        reservation_seq_model: ReservationSeqModel,
) -> ApiResponse[str]:
    await reservation_repayment_service(
        user_seq=user_seq,
        reservation_seq=reservation_seq_model.reservation_seq
    )
    return ApiResponse.success("Success")
