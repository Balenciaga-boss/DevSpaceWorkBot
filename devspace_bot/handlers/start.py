from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from devspace_bot.keyboards import main_menu_keyboard

router = Router()


WELCOME_TEXT = (
    "DEVSPACE\n\n"
    "Разрабатываем Telegram-ботов, сайты, CRM, парсеры, Mini Apps и автоматизации.\n"
    "Выберите действие:"
)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "menu:start")
async def show_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_keyboard())
    await callback.answer()
