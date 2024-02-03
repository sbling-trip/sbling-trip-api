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
