import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from devspace_bot.config import get_settings
from devspace_bot.database import build_session_factory, init_db, session_scope
from devspace_bot.handlers import build_router
from devspace_bot.repositories import seed_portfolio_categories
from devspace_bot.services.antispam import CooldownGuard


async def run_bot() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()
    session_factory = build_session_factory(settings.database_url)
    await init_db(session_factory)

    async for session in session_scope(session_factory):
        await seed_portfolio_categories(session)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(build_router())
    dispatcher["settings"] = settings
    dispatcher["session_factory"] = session_factory
    dispatcher["spam_guard"] = CooldownGuard(settings.spam_cooldown_seconds)

    await dispatcher.start_polling(bot)


def main() -> None:
    asyncio.run(run_bot())

