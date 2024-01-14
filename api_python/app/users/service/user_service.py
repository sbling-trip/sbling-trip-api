from datetime import datetime
from typing import Annotated

from fastapi import Depends

from api_python.app.common.exceptions import credentials_exception, token_expired_exception
from api_python.app.security.oauth_config import oauth2_scheme
from api_python.app.security.service.security_service import decode_token, get_token_from_cookie
from api_python.app.users.repository.user_repository import find_by_external_id


async def get_current_user_by_token(token: str) -> int:
    payload = decode_token(token)
    external_id = payload.get("sub")
    expired_at = datetime.fromtimestamp(payload.get("exp"))

    if external_id is None:
        raise credentials_exception

    user_model = await find_by_external_id(external_id)
    if user_model is None:
        print("User not found")
        raise credentials_exception
    if datetime.utcnow() > expired_at:
        print("Token expired")
        raise token_expired_exception
    return user_model.user_seq


async def get_current_user_by_authorization(token: Annotated[str, Depends(oauth2_scheme)]):
    user_seq = await get_current_user_by_token(token)
    return user_seq


async def get_current_user_by_cookie(token: Annotated[str, Depends(get_token_from_cookie)]):
    user_seq = await get_current_user_by_token(token)
    return user_seq

