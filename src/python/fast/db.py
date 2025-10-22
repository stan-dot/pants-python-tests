from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from fast.config import Settings
from loguru import logger
from sqlalchemy.orm import declarative_base

engine: AsyncEngine | None = None
AsyncSessionLocal: sessionmaker | None = None

Base = declarative_base()


def get_engine_and_sessionmaker(
    settings: Settings
) -> tuple[AsyncEngine, sessionmaker]:
    global engine, AsyncSessionLocal

    url = f"mysql+aiomysql://{settings.mysql.user}:{settings.mysql.password}@{settings.mysql.host}/{settings.mysql.db_name}"

    engine = create_async_engine(
        url,
        pool_size=20,
        max_overflow=40,
        pool_recycle=1800,
        pool_timeout=90,
        pool_pre_ping=True,
        echo=settings.mysql.use_dev,
        future=True,
        connect_args={"ssl": None},
    )

    AsyncSessionLocal = sessionmaker(
        bind=engine,  # type: ignore
        class_=AsyncSession,
        expire_on_commit=False,
    )  # pyright: ignore[reportCallIssue]

    return engine, AsyncSessionLocal
