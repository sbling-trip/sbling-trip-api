from abc import ABC, abstractmethod
from contextlib import AsyncExitStack


class AsyncContextResource(ABC):
    """
    fastapi의 lifecycle에 따라 관리되는 싱글톤을 위한 추상클래스
    """

    @abstractmethod
    async def manage_context(self, exit_stack: AsyncExitStack):
        """
        async context manager를 사용하기 위한 메서드

        **예제**
        client = await exit_stack.enter_async_context(SomeAsyncClient())
        await client.do_something()

        위 코드는 아래 코드와 의미적으로 동일하다.
        단, 위 코드의 경우 인자로 받은 exit_stack이 종료될 때 client가 정리된다. 아래 코드는 with문을 탈출할 때 client가 정리된다.

        async with SomeAsyncClient() as client:
            await client.do_something()

        fastapi의 main lifecycle에서 아래와 같이 중첩된 async context manager를 사용하면 모든 client들이 main app에 import된다.
        그리고 만들어진 client를 각 클라이언트 객체들이 다시 주입받아야 한다. 그럴 경우 main app에 너무 많은 dependency가 생기고 관리가 어려워진다.

        async with RedisClient() as redis_client,
                HttpClient() as http_client,
                SomeAsyncClient1() as client1,
                SomeAsyncClient2() as client2,
                ~~~~~:
            RedisClientManager.client = redis_client
            HttpClientManager.client = http_client
            SomeAsyncClient1Manager.client = client1
            SomeAsyncClient2Manager.client = client2
            ~~~~~

            yield

        이를 아래와 같이 개선할 수 있다.

        client_manager_list = [
            RedisClientManager, HttpClientManager, SomeAsyncClient3Manager, SomeAsyncClient4Manager, ...
        ]
        async with AsyncExitStack() as stack:
            for client_manager in client_manager_list:
                await client_manager.manage_context(stack)

            yield
        """
        pass
