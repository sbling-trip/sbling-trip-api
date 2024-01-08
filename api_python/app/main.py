from contextlib import asynccontextmanager, AsyncExitStack

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from api_python.app.common.client.resources import async_resource_list
from api_python.app.common.cors import allow_origins
from api_python.app.stay.stay_router import stay_router
from api_python.app.wish.wish_router import wish_router

from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware

from api_python.resources.credentials import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# noinspection PyShadowingNames,PyUnusedLocal
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        for resource in async_resource_list:
            await resource.manage_context(stack)

        # running application
        yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="secret-string")

app.include_router(stay_router)
app.include_router(wish_router)


@app.get("/actuator/health")
def health_check():
    """
    fastapi 프로젝트가 잘 작동하고 있는지 확인하기 위해 로드 밸런서가 주기적으로 health check를 호출한다.
    """
    return {"status": "UP"}


oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.get('/oauth/login/{provider}')
async def login_by_oauth(request: Request, provider: str):
    base_url = 'http://localhost:8000'
    redirect_uri = f'{base_url}/oauth/login/{provider}/callback'
    # callback 주소를 담아 oauth 제공사들에 맞게 redirect를 요청
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@app.get("/oauth/login/google/callback")
async def auth_via_google(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token['userinfo']
    print(dict(user))
    return dict(user)

