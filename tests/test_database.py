from sqlalchemy import select

from devspace_bot.database import build_session_factory, init_db, session_scope
from devspace_bot.models import PortfolioCategory


async def test_init_db_supports_local_sqlite_database(tmp_path):
    database_url = f"sqlite+aiosqlite:///{tmp_path / 'devspace_bot.db'}"
    session_factory = build_session_factory(database_url)

    await init_db(session_factory)

    async for session in session_scope(session_factory):
        session.add(PortfolioCategory(title="Telegram-боты", slug="telegram-bots"))

    async for session in session_scope(session_factory):
        result = await session.execute(select(PortfolioCategory.title))

    assert result.scalar_one() == "Telegram-боты"
