from datetime import timedelta, datetime

from fastapi import APIRouter
from starlette.requests import Request

from api_python.app.common.configuration import config
from api_python.app.security.oauth_config import oauth

from api_python.app.users.model.user_model import  UserOrm
from api_python.app.users.repository.user_repository import find_by_external_id, insert_user_from_orm
from api_python.resources.credentials import SECRET_KEY, ALGORITHM

from jose import jwt


auth_router = APIRouter(
    prefix="/oauth/login"
)


@auth_router.get('/{provider}')
async def login_by_oauth(request: Request, provider: str):
    base_url = config["fastapi"]["base_url"]
    redirect_uri = f'{base_url}/oauth/login/{provider}/callback'
    # callback 주소를 담아 oauth 제공사들에 맞게 redirect를 요청
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@auth_router.get("/google/callback")
async def auth_via_google(request: Request):
    token = await oauth.google.authorize_access_token(request)

    user = token['userinfo']
    user_model = await find_by_external_id(user['sub'])
    if user_model:
        # TODO: expired_at 업데이트
        pass
    else:
        new_user = UserOrm(
            email=user['email'],
            external_id=user['sub'],
            first_name=user['given_name'],
            last_name=user['family_name'],
            oauth_provider="google",
            logo_url=user['picture'],
            # utcnow()에서 12시간을 더한 값을 unix timestamp로 변환
            expired_at=(datetime.utcnow() + timedelta(hours=12)),
            created_at=datetime.utcnow(),
            logged_in_at=datetime.utcnow(),
        )
        result = await insert_user_from_orm(new_user)
    access_token = create_access_token(
        data={"sub": user["sub"]},
        # expires_delta=timedelta(seconds=users["exp"] - int(datetime.utcnow().timestamp()))
    )
    return access_token


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=12)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
