from typing import Annotated

from fastapi import Depends

from api_python.app.common.exceptions import credentials_exception
from api_python.app.security.oauth_config import oauth2_scheme
from api_python.app.security.service.security_service import decode_token, get_token_from_cookie
from api_python.app.user.model.user_model import UserResponseModel


def get_user_seq_by_token(token: str) -> UserResponseModel:
    payload = decode_token(token)
    return payload.get("user_seq")


def get_user_seq_by_authorization(token: Annotated[str, Depends(oauth2_scheme)]):
    if token:
        return get_user_seq_by_token(token)
    else:
        raise credentials_exception


# 비 로그인 유저 가능할 경우
def get_user_seq_by_authorization_optional(token: Annotated[str, Depends(oauth2_scheme)]):
    if token:
        try:
            return get_user_seq_by_token(token)
        except credentials_exception:
            return -1
    else:
        return -1


async def get_current_user_by_cookie(token: Annotated[str, Depends(get_token_from_cookie)]):
    user_model = await get_user_seq_by_token(token)
    return user_model

