from typing import Annotated

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api_python.app.users.model.user_model import UserModel
from api_python.app.users.repository.user_repository import find_by_external_id
from api_python.resources.credentials import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        external_id = payload.get("sub")
        if external_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_model = await find_by_external_id(external_id)
    # TODO: 만료일자 체크 로직 추가(위의 ORM 쿼리에서 만료일자를 체크할 수도 있음)

    if user_model is None:
        raise credentials_exception
    return user_model


async def get_current_active_user(current_user: Annotated[UserModel, Depends(get_current_user)]):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
