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


def add_review_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to add review(리뷰 추가에 실패했습니다.): " + error_message
    )


def get_review_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to get review(리뷰 조회에 실패했습니다.): " + error_message
    )


def get_room_info_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to get room(객실 조회에 실패했습니다.): " + error_message
    )


def get_stay_info_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to get stay(숙소 조회에 실패했습니다.): " + error_message
    )


def add_wish_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to add wish(찜 추가에 실패했습니다.): " + error_message
    )


def delete_wish_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to delete wish(찜 삭제에 실패했습니다.): " + error_message
    )


def get_wish_exception(error_message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to get wish(찜 조회에 실패했습니다.): " + error_message
    )

