from models import Base
from settings import api_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

postgres_engine = create_async_engine(
    api_settings.POSTGRES_CONNECT,
    pool_pre_ping=True,
    pool_recycle=60 * 60,
    pool_size=api_settings.POOL,
    max_overflow=api_settings.MAX_OVER,
    echo=api_settings.DEBUG
)


def get_async_sessionmaker():
    return async_sessionmaker(
        postgres_engine, class_=AsyncSession, expire_on_commit=False,
    )


async def get_async_session() -> AsyncSession:
    session = get_async_sessionmaker()
    async with session() as session_connect:
        try:
            yield session_connect
        finally:
            await session_connect.close()


# async def init_db():
#     async with postgres_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
