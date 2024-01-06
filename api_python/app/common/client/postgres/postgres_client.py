import contextlib
from contextlib import asynccontextmanager
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine

from api_python.app.common.client.async_context_resource import AsyncContextResource
from api_python.app.common.configuration import config


class PostgresClient(AsyncContextResource):
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    async def close(self):
        if self._engine is None:
            raise Exception("SqlAlchemy AsyncEngine is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def session(self):
        if self._sessionmaker is None:
            raise Exception("SqlAlchemy AsyncEngine is not initialized")

        async with self._sessionmaker() as session:
            yield session

    @asynccontextmanager
    async def connect(self):
        if self._engine is None:
            raise Exception("SqlAlchemy AsyncEngine is not initialized")

        async with self._engine.connect() as conn:
            yield conn

    @asynccontextmanager
    async def _get_engine(self):
        async_dialect = "asyncpg"
        postgres_config = config["postgresql"]
        username = postgres_config["username"]
        password = postgres_config["password"]
        host = postgres_config["host"]
        port = postgres_config["port"]
        database = postgres_config["database"]

        uri = f"postgresql+{async_dialect}://{username}:{quote_plus(password)}@{host}:{port}"

        if database is not None:
            uri = f"{uri}/{database}"

        try:
            yield create_async_engine(uri)
        finally:
            await self.close()

    async def manage_context(self, exit_stack: contextlib.AsyncExitStack):
        self._engine = await exit_stack.enter_async_context(self._get_engine())
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)


postgres_client = PostgresClient()
