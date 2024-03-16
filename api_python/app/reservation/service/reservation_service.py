from datetime import datetime
from typing import List

from api_python.app.common.exceptions import get_validate_stay_room_seq_exception, get_validate_room_exception
from api_python.app.point.service.point_service import point_payment_service, update_point_service
from api_python.app.reservation.model.reservation_model import UserResponseReservationInfoModel
from api_python.app.reservation.repository.reservation_repository import get_reservation_stay_repository, \
    get_reservation_room_list, add_reservation_repository, is_validate_stay_room_seq, is_reservation_available, \
    update_reservation_payment, cancel_reservation, get_reservation
from api_python.app.stay.model.stay_model import UserResponseStayInfoModel
import backoff

LIMIT_COUNT = 20


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
async def safe_update_reservation_payment(reservation_seq: int):
    await update_reservation_payment(reservation_seq=reservation_seq)


async def get_reservation_available_stay_service(
        user_seq: int,
        cursor: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
        stay_type: int,
) -> List[UserResponseStayInfoModel]:
    result = await get_reservation_stay_repository(
        user_seq=user_seq,
        offset=cursor*LIMIT_COUNT,
        limit=LIMIT_COUNT,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count,
        stay_type=stay_type
    )
    return result


async def get_reservation_room_list_service(
        user_seq: int,
        reservation_status: list[str]
) -> List[UserResponseReservationInfoModel]:
    result = await get_reservation_room_list(
        user_seq=user_seq,
        reservation_status=reservation_status
    )
    return result


async def add_reservation_service(
        user_seq: int,
        stay_seq: int,
        room_seq: int,
        check_in_date: datetime.date,
        check_out_date: datetime.date,
        adult_guest_count: int,
        child_guest_count: int,
        special_requests: str,
        payment_price: int
) -> bool:
    validate_stay_room_seq = await is_validate_stay_room_seq(
        stay_seq=stay_seq,
        room_seq=room_seq
    )
    if not validate_stay_room_seq:
        raise get_validate_stay_room_seq_exception("올바르지 않은 숙소 또는 방입니다. staySeq와 roomSeq를 확인해주세요.")

    reservation_available = await is_reservation_available(
        room_seq=room_seq,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count
    )

    if not reservation_available:
        raise get_validate_room_exception()

    reservation_seq = await add_reservation_repository(
        user_seq=user_seq,
        stay_seq=stay_seq,
        room_seq=room_seq,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adult_guest_count=adult_guest_count,
        child_guest_count=child_guest_count,
        special_requests=special_requests,
        payment_price=payment_price
    )

    await point_payment_service(
        user_seq=user_seq,
        payment_price=payment_price,
    )

    try:
        await safe_update_reservation_payment(reservation_seq=reservation_seq)
    except Exception as e:
        # TODO: 에러 로그 저장, 추후 DB 자체에서 업데이트 처리
        print(f"Update reservation payment failed after retries: {str(e)}")
    return True


async def cancel_reservation_service(
        user_seq: int,
        reservation_seq: int
) -> bool:
    reservation_model = await get_reservation(
        reservation_seq=reservation_seq
    )

    # 예약 취소 시 결제 상태가 paid인 경우 포인트 환불
    if reservation_model.payment_status == "paid":
        await update_point_service(
            user_seq=user_seq,
            point=reservation_model.payment_price
        )

    result = await cancel_reservation(
        reservation_seq=reservation_seq
    )
    return result


async def reservation_repayment_service(
        user_seq: int,
        reservation_seq: int
) -> bool:
    reservation_model = await get_reservation(
        reservation_seq=reservation_seq
    )

    if reservation_model.payment_status == "unpaid":
        await point_payment_service(
            user_seq=user_seq,
            payment_price=reservation_model.payment_price,
        )

    try:
        await safe_update_reservation_payment(reservation_seq=reservation_seq)
    except Exception as e:
        # TODO: 에러 로그 저장, 추후 DB 자체에서 업데이트 처리
        print(f"Update reservation payment failed after retries: {str(e)}")
    return True
