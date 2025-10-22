from __future__ import annotations

import typing

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> typing.AsyncGenerator[AsyncSession, None]:
    session_maker = request.app.state.sessionmaker
    async with session_maker() as session:
        yield session
