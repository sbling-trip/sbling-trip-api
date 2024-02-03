from jose import jwt, JWTError
from starlette.exceptions import HTTPException
from starlette.requests import Request

from api_python.app.common.exceptions import credentials_exception
from api_python.resources.credentials import SECRET_KEY, ALGORITHM


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str, non_login_available: bool = False) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        if non_login_available:
            return {"user_seq": -1}
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return payload


async def get_token_from_cookie(request: Request):
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token missing in cookies")
    return access_token
