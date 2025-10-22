
from collections.abc import AsyncGenerator, Generator
from typing import Literal

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.mysql import MySqlContainer

from app.main import app
from app.db import Base
from app.dependencies import get_session

import os


@pytest.fixture(scope="session")
def anyio_backend() -> Literal["asyncio"]:
    return "asyncio"


@pytest.fixture(scope="session")
def mysql_container(
    anyio_backend: Literal["asyncio"],
) -> Generator[MySqlContainer, None, None]:
    with MySqlContainer(
        "mysql:8.0.41", dbname="mydb", username="testuser", password="testpassword"
    ) as mysql:
        mysql.start()
        url = mysql.get_connection_url().replace("mysql://", "mysql+aiomysql://")
        os.environ["MYSQL_URL"] = url
        print(f"Started MySQL container with URL: {url}")
        yield mysql


@pytest.fixture
async def async_session(
    mysql_container: MySqlContainer,
) -> AsyncGenerator[AsyncSession, None]:
    db_url = mysql_container.get_connection_url().replace(
        "mysql://", "mysql+aiomysql://"
    )

    async_engine = create_async_engine(db_url)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with async_session_maker() as session:
        yield session

    await async_engine.dispose()


@pytest.fixture
async def async_client(
    async_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: async_session
    _transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=_transport, base_url="http://test", follow_redirects=True
    ) as client:
        yield client

    app.dependency_overrides.clear()
