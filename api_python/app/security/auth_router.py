from datetime import timedelta, datetime
from pytz import timezone
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api_python.app.common.api_response import ApiResponse
from api_python.app.common.configuration import config
from api_python.app.common.phase import IS_PROD
from api_python.app.security.oauth_config import oauth
from api_python.app.security.service.security_service import create_access_token

from api_python.app.users.model.user_model import UserOrm
from api_python.app.users.repository.user_repository import find_by_external_id_user_model, insert_user_from_orm, \
    update_user_expiration, update_user_login_at

auth_router = APIRouter(
    prefix="/oauth/login"
)

# TODO: oauth 제공사들에 맞게 redirect를 요청, id, password를 입력받아 로그인을 진행 API 추가.


@auth_router.get(
    "/google",
    summary="oauth 로그인",
    description="google 로그인",
    tags=["oauth"],
)
async def login_via_google(request: Request):
    # redirect_uri = request.url_for('auth_via_google')
    print(f"start google oauth! request.session: {request.session}, request.code: {request.query_params.get('code'),} request.state: {request.query_params.get('state')}")
    redirect_uri = config["fastapi"]["redirect_url"] if IS_PROD else request.url_for('auth_via_google')

    print(f"redirect_uri: {redirect_uri}")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.post(
    "/callback/google",
    summary="oauth 로그인 콜백",
    description="google 로그인 토큰 발급",
    tags=["oauth"],
)
async def auth_via_google(request: Request) -> RedirectResponse:
    print(f"start callback! request.session: {request.session},request.code: {request.query_params.get('code'),} request.state: {request.query_params.get('state')}")

    token = await oauth.google.authorize_access_token(request)

    user = token['userinfo']
    user_model = await find_by_external_id_user_model(user['sub'])
    expired_at = datetime.utcnow() + timedelta(hours=12)
    login_at = datetime.now(tz=timezone("Asia/Seoul")).replace(tzinfo=None)
    if user_model:
        await update_user_expiration(user['sub'], expired_at)
        await update_user_login_at(user['sub'], login_at)
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
    return ApiResponse.success(access_token)
