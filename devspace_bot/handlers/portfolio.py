from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker

from devspace_bot.database import session_scope
from devspace_bot.keyboards import back_to_menu_keyboard, portfolio_keyboard
from devspace_bot.repositories import list_portfolio_cases, list_portfolio_categories

router = Router()


@router.callback_query(F.data == "menu:portfolio")
async def show_portfolio(callback: CallbackQuery, session_factory: async_sessionmaker) -> None:
    async for session in session_scope(session_factory):
        categories = await list_portfolio_categories(session)

    titles = [category.title for category in categories]
    await callback.message.edit_text(
        "📂 Портфолио DEVSPACE\n\nВыберите категорию:",
        reply_markup=portfolio_keyboard(titles),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("portfolio:"))
async def show_portfolio_category(callback: CallbackQuery, session_factory: async_sessionmaker) -> None:
    index = int(callback.data.split(":", 1)[1])

    async for session in session_scope(session_factory):
        categories = await list_portfolio_categories(session)
        if index >= len(categories):
            await callback.answer("Категория не найдена", show_alert=True)
            return

        category = categories[index]
        cases = await list_portfolio_cases(session, category.id)

    if not cases:
        text = (
            f"📂 {category.title}\n\n"
            "Кейсы для этой категории скоро появятся."
        )
    else:
        lines = [f"📂 {category.title}"]
        for case in cases:
            line = f"\n<b>{case.title}</b>\n{case.description}"
            if case.url:
                line += f"\n{case.url}"
            lines.append(line)
        text = "\n".join(lines)

    await callback.message.edit_text(text, reply_markup=back_to_menu_keyboard(), disable_web_page_preview=True)
    await callback.answer()
