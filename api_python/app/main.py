from contextlib import asynccontextmanager, AsyncExitStack

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

from api_python.app.common.client.resources import async_resource_list
from api_python.app.security.cors import allow_origins
from api_python.app.security.auth_router import auth_router
from api_python.app.stay.stay_router import stay_router
from api_python.app.wish.wish_router import wish_router

from api_python.resources.credentials import SESSION_MIDDLEWARE_KEY


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

app.add_middleware(SessionMiddleware, secret_key=SESSION_MIDDLEWARE_KEY)

app.include_router(stay_router)
app.include_router(wish_router)
app.include_router(auth_router)


@app.get("/actuator/health")
def health_check():
    """
    fastapi 프로젝트가 잘 작동하고 있는지 확인하기 위해 로드 밸런서가 주기적으로 health check를 호출한다.
    """
    return {"status": "UP"}


