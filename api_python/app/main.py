from contextlib import asynccontextmanager, AsyncExitStack

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

from api_python.app.common.client.resources import async_resource_list
from api_python.app.common.config.phase import IS_PROD
from api_python.app.reservation.reservation_router import reservation_router
from api_python.app.review.review_router import review_router
from api_python.app.room.room_router import room_router
from api_python.app.search.search_router import search_router
from api_python.app.security.cors import allow_origins
from api_python.app.stay.stay_router import stay_router
from api_python.app.wish.wish_router import wish_router
from api_python.app.user.user_router import user_router
from api_python.app.point.point_router import point_router 

import random
import string


def get_random_string(length=10):
    result_str = "".join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


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
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)


app.add_middleware(SessionMiddleware, secret_key=get_random_string())
if IS_PROD:
    app.include_router(user_router)
    app.include_router(stay_router)
    app.include_router(wish_router)
    app.include_router(room_router)
    app.include_router(review_router)
    app.include_router(point_router)
    app.include_router(reservation_router)
    app.include_router(search_router)
else:
    app.include_router(user_router, prefix="/api")
    app.include_router(stay_router, prefix="/api")
    app.include_router(wish_router, prefix="/api")
    app.include_router(room_router, prefix="/api")
    app.include_router(review_router, prefix="/api")
    app.include_router(point_router, prefix="/api")
    app.include_router(reservation_router, prefix="/api")
    app.include_router(search_router, prefix="/api")


@app.get("/actuator/health")
def health_check():
    """
    fastapi 프로젝트가 잘 작동하고 있는지 확인하기 위해 로드 밸런서가 주기적으로 health check를 호출한다.
    """
    return {"status": "UP", "is_prod": IS_PROD}
