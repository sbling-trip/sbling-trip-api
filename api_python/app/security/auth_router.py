from datetime import timedelta, datetime

from fastapi import APIRouter
from starlette.requests import Request

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.configuration import config
from api_python.app.security.model.token import Token
from api_python.app.security.oauth_config import oauth
from api_python.app.security.service.security_service import create_access_token

from api_python.app.users.model.user_model import UserOrm
from api_python.app.users.repository.user_repository import find_by_external_id, insert_user_from_orm, \
    update_user_expiration

auth_router = APIRouter(
    prefix="/oauth/login"
)

# TODO: oauth 제공사들에 맞게 redirect를 요청, id, password를 입력받아 로그인을 진행 API 추가.


@auth_router.get(
    "/{provider}",
    summary="oauth 로그인",
    description="oauth 제공사들에 맞게 redirect를 요청합니다. provider현재 google만 제공됩니다.",
    tags=["oauth"],
)
async def login_by_oauth(request: Request, provider: str):
    base_url = config["fastapi"]["base_url"]
    redirect_uri = f'{base_url}/oauth/login/{provider}/callback'
    # callback 주소를 담아 oauth 제공사들에 맞게 redirect를 요청
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@auth_router.get(
    "/google/callback",
    summary="oauth 로그인 콜백",
    description="oauth 제공사들에 맞게 redirect를 요청합니다. response에 access_token을 담아 반환합니다.",
    tags=["oauth"],
)
async def auth_via_google(request: Request) -> ApiResponse[Token]:
    token = await oauth.google.authorize_access_token(request)

    user = token['userinfo']
    user_model = await find_by_external_id(user['sub'])
    expired_at = datetime.utcnow() + timedelta(hours=12)
    if user_model:
        await update_user_expiration(user['sub'], expired_at)
        print(f"update user expiration {user['name']}")
    else:
        new_user = UserOrm(
            email=user['email'],
            external_id=user['sub'],
            first_name=user['given_name'],
            last_name=user['family_name'],
            oauth_provider="google",
            logo_url=user['picture'],
            # utcnow()에서 12시간을 더한 값을 unix timestamp로 변환
            expired_at=expired_at,
            created_at=datetime.utcnow(),
            logged_in_at=datetime.utcnow(),
        )
        await insert_user_from_orm(new_user)
        print(f"insert new user {user['name']}")

    access_token = create_access_token(
        data={"sub": user["sub"], "exp": expired_at}
    )

    return ApiResponse.success(Token(access_token=access_token))
