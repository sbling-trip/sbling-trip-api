from fastapi import APIRouter
from starlette.requests import Request

from api_python.app.common.configuration import config
from api_python.app.security.oauth_config import oauth

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
    print(dict(user))
    return dict(user)
