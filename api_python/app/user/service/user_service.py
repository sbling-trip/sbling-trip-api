from typing import Annotated

from fastapi import Depends

from api_python.app.common.exceptions import credentials_exception
from api_python.app.security.oauth_config import oauth2_scheme
from api_python.app.security.service.security_service import (
    decode_token,
)
from api_python.app.user.model.user_model import UserModel
from api_python.app.user.repository.user_repository import (
    find_by_user_seq_user_model,
    update_user,
)

from api_python.app.common.model.user import UserStatusType


def get_user_seq_by_token(token: str, non_login_available: bool = False) -> int:
    payload = decode_token(token, non_login_available)
    if payload.get("userStatus") != UserStatusType.IDEAL.value:
        raise credentials_exception

    return payload.get("userSeq")


def get_user_seq_by_authorization(token: Annotated[str, Depends(oauth2_scheme)]):
    if token:
        return get_user_seq_by_token(token)
    else:
        raise credentials_exception


# 비 로그인 유저 가능할 경우
def get_user_seq_by_authorization_optional(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    if token:
        result = get_user_seq_by_token(token, non_login_available=True)
        return result
    else:
        return -1


async def get_user_info_service(
    user_seq: int,
) -> UserModel:
    return await find_by_user_seq_user_model(
        user_seq=user_seq,
    )


async def update_user_info_service(
    user_seq: int,
    user_name: str | None,
    location_agree: bool | None,
    marketing_agree: bool | None,
) -> bool:
    await update_user(
        user_seq=user_seq,
        user_name=user_name,
        location_agree=location_agree,
        marketing_agree=marketing_agree,
    )

    return True
