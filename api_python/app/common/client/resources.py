from api_python.app.common.client.async_context_resource import AsyncContextResource
from api_python.app.common.client.postgres.postgres_client import postgres_client

# 순환 참조를 방지하기 위해 AsyncContextResource와 다른 파일로 분리함
async_resource_list: list[AsyncContextResource] = [
    postgres_client,
]
