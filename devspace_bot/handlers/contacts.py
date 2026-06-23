from aiogram import F, Router
from aiogram.types import CallbackQuery

from devspace_bot.keyboards import back_to_menu_keyboard

router = Router()


@router.callback_query(F.data == "menu:contacts")
async def show_contacts(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "📞 Контакты DEVSPACE\n\n"
        "👤 @tonaryy\n"
        "👤 @cryvento",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()

