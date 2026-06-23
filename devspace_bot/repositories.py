from aiogram.types import User as TelegramUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from devspace_bot.constants import PORTFOLIO_CATEGORIES
from devspace_bot.models import Application, PortfolioCase, PortfolioCategory, User


async def upsert_user(session: AsyncSession, telegram_user: TelegramUser) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_user.id))
    user = result.scalar_one_or_none()
    full_name = " ".join(filter(None, [telegram_user.first_name, telegram_user.last_name]))

    if user is None:
        user = User(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            full_name=full_name or None,
        )
        session.add(user)
        await session.flush()
        return user

    user.username = telegram_user.username
    user.full_name = full_name or None
    await session.flush()
    return user


async def create_application(
    session: AsyncSession,
    user: User,
    data: dict[str, str],
) -> Application:
    application = Application(
        user_id=user.id,
        project_type=data["project_type"],
        has_spec=data["has_spec"],
        description=data["description"],
        budget=data["budget"],
        deadline=data["deadline"],
        contact=data["contact"],
    )
    session.add(application)
    await session.flush()
    return application


async def seed_portfolio_categories(session: AsyncSession) -> None:
    for index, title in enumerate(PORTFOLIO_CATEGORIES):
        slug = f"category-{index}"
        result = await session.execute(select(PortfolioCategory).where(PortfolioCategory.title == title))
        if result.scalar_one_or_none() is None:
            session.add(PortfolioCategory(title=title, slug=slug))
    await session.flush()


async def list_portfolio_categories(session: AsyncSession) -> list[PortfolioCategory]:
    result = await session.execute(select(PortfolioCategory).order_by(PortfolioCategory.id))
    return list(result.scalars().all())


async def list_portfolio_cases(session: AsyncSession, category_id: int) -> list[PortfolioCase]:
    result = await session.execute(
        select(PortfolioCase).where(PortfolioCase.category_id == category_id).order_by(PortfolioCase.id.desc())
    )
    return list(result.scalars().all())

