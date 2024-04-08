from jose import jwt, JWTError
from starlette.exceptions import HTTPException

from api_python.resources.credentials import SECRET_KEY, ALGORITHM


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str, non_login_available: bool = False) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        if non_login_available:
            return {"userSeq": -1}
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return payload
