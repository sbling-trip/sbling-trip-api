from starlette import status
from starlette.exceptions import HTTPException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials(자격 증명을 확인할 수 없습니다. 토큰을 확인 해 주세요.)",
    headers={"WWW-Authenticate": "Bearer"},
)

token_expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired(토큰이 만료되었습니다.)",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_review_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to get review(리뷰 조회에 실패했습니다.): " + error_message,
    )


def get_room_info_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to get room(객실 조회에 실패했습니다.): " + error_message,
    )


def get_stay_info_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to get stay(숙소 조회에 실패했습니다.): " + error_message,
    )


def add_review_not_found_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Failed to add review(리뷰 추가에 실패했습니다.): " + error_message,
    )


def add_review_server_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to add review(리뷰 추가에 실패했습니다.): " + error_message,
    )


def update_review_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to update review(리뷰 수정에 실패했습니다.): " + error_message,
    )


def remove_review_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to delete review(리뷰 삭제에 실패했습니다.): " + error_message,
    )


def add_wish_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to add wish(찜 추가에 실패했습니다.): " + error_message,
    )


def delete_wish_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to delete wish(찜 삭제에 실패했습니다.): " + error_message,
    )


def get_wish_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to get wish(찜 조회에 실패했습니다.): " + error_message,
    )


def get_user_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to get user(유저 조회에 실패했습니다.): " + error_message,
    )


def update_user_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to update user(유저 업데이트에 실패했습니다.): " + error_message,
    )


def get_point_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to get point(포인트 조회에 실패했습니다.): " + error_message,
    )


def update_point_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to update point(포인트 업데이트에 실패했습니다.): " + error_message,
    )


def get_reservation_available_stay_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to get reservation available stay(예약 가능 숙소 조회에 실패했습니다.): " + error_message
    )


def get_reservation_room_list_stay_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to get reservation list stay(예약 목록 조회에 실패했습니다.): " + error_message
    )


def get_reservation_available_room_list_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to get reservation room list(예약 가능 객실 조회에 실패했습니다.): " + error_message
    )


def get_reservation_available(exception_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to get reservation available(예약 가능 조회에 실패했습니다.): " + exception_message
    )


def cancel_reservation_exception(exception_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to delete reservation(예약 삭제에 실패했습니다.): " + exception_message
    )


def update_reservation_exception(exception_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to update reservation(예약 업데이트에 실패했습니다.): " + exception_message
    )


def get_validate_stay_room_seq_exception(exception_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to validate stay room seq(숙소 객실 seq 유효성 검사에 실패했습니다.): " + exception_message
    )


def get_validate_room_exception(exception_message: str = "") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to validate room(객실 유효성 검사에 실패했습니다. 현재 예약이 불가능 합니다.): " + exception_message
    )
