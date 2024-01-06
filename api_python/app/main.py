from contextlib import asynccontextmanager, AsyncExitStack

from fastapi import FastAPI

from api_python.app.common.client.resources import async_resource_list
from api_python.app.stay.stay_router import stay_router


# noinspection PyShadowingNames,PyUnusedLocal
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        for resource in async_resource_list:
            await resource.manage_context(stack)

        # running application
        yield

app = FastAPI(lifespan=lifespan)

app.include_router(stay_router)


@app.get("/actuator/health")
def health_check():
    """
    fastapi 프로젝트가 잘 작동하고 있는지 확인하기 위해 로드 밸런서가 주기적으로 health check를 호출한다.
    """
    return {"status": "UP"}
