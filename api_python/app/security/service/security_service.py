from typing import Annotated

from fastapi import Depends
from jose import jwt, JWTError

from api_python.app.common.exceptions import credentials_exception
from api_python.app.security.oauth_config import oauth2_scheme
from api_python.resources.credentials import SECRET_KEY, ALGORITHM


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    return payload
