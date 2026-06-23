from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from devspace_bot.models import Base


def build_engine(database_url: str):
    return create_async_engine(database_url, pool_pre_ping=True)


def build_session_factory(database_url: str) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(build_engine(database_url), expire_on_commit=False)


async def init_db(session_factory: async_sessionmaker[AsyncSession]) -> None:
    engine = session_factory.kw["bind"]
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def session_scope(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        async with session.begin():
            yield session

