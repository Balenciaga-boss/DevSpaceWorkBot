import time
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from devspace_bot.config import Settings
from devspace_bot.constants import BUDGET_OPTIONS, DEADLINE_OPTIONS, PROJECT_TYPES, TECH_SPEC_OPTIONS
from devspace_bot.database import session_scope
from devspace_bot.keyboards import form_navigation_keyboard, inline_options_keyboard, main_menu_keyboard
from devspace_bot.messages import APPLICATION_SUCCESS_TEXT
from devspace_bot.repositories import create_application, upsert_user
from devspace_bot.services.antispam import CooldownGuard
from devspace_bot.services.formatting import ApplicationPayload, format_admin_application
from devspace_bot.states import EstimateForm

router = Router()


@router.callback_query(F.data == "menu:estimate")
async def start_estimate(
    callback: CallbackQuery,
    state: FSMContext,
    spam_guard: CooldownGuard,
) -> None:
    now = time.monotonic()
    if not spam_guard.can_start(callback.from_user.id, now):
        await callback.answer("Подождите немного перед новой заявкой.", show_alert=True)
        return

    spam_guard.mark_started(callback.from_user.id, now)
    await state.set_state(EstimateForm.project_type)
    await callback.message.edit_text(
        "⚡ Получить оценку проекта\n\nЧто необходимо разработать?",
        reply_markup=inline_options_keyboard(PROJECT_TYPES, "project_type", with_back=False),
    )
    await callback.answer()


@router.callback_query(EstimateForm.project_type, F.data.startswith("project_type:"))
async def set_project_type(callback: CallbackQuery, state: FSMContext) -> None:
    await save_option(callback, state, PROJECT_TYPES, "project_type")
    await state.set_state(EstimateForm.has_spec)
    await callback.message.edit_text(
        "Есть ли техническое задание?",
        reply_markup=inline_options_keyboard(TECH_SPEC_OPTIONS, "has_spec"),
    )
    await callback.answer()


@router.callback_query(EstimateForm.has_spec, F.data.startswith("has_spec:"))
async def set_has_spec(callback: CallbackQuery, state: FSMContext) -> None:
    await save_option(callback, state, TECH_SPEC_OPTIONS, "has_spec")
    await state.set_state(EstimateForm.description)
    await callback.message.edit_text(
        "Опишите проект своими словами.",
        reply_markup=form_navigation_keyboard(),
    )
    await callback.answer()


@router.message(EstimateForm.description)
async def set_description(message: Message, state: FSMContext) -> None:
    description = message.text.strip() if message.text else ""
    if len(description) < 10:
        await message.answer("Опишите проект чуть подробнее, минимум 10 символов.")
        return

    await state.update_data(description=description)
    await state.set_state(EstimateForm.budget)
    await message.answer(
        "Укажите примерный бюджет.",
        reply_markup=inline_options_keyboard(BUDGET_OPTIONS, "budget"),
    )


@router.callback_query(EstimateForm.budget, F.data.startswith("budget:"))
async def set_budget(callback: CallbackQuery, state: FSMContext) -> None:
    await save_option(callback, state, BUDGET_OPTIONS, "budget")
    await state.set_state(EstimateForm.deadline)
    await callback.message.edit_text(
        "Какие сроки реализации?",
        reply_markup=inline_options_keyboard(DEADLINE_OPTIONS, "deadline"),
    )
    await callback.answer()


@router.callback_query(EstimateForm.deadline, F.data.startswith("deadline:"))
async def set_deadline(callback: CallbackQuery, state: FSMContext) -> None:
    await save_option(callback, state, DEADLINE_OPTIONS, "deadline")
    await state.set_state(EstimateForm.contact)
    await callback.message.edit_text(
        "Укажите Telegram для обратной связи.",
        reply_markup=form_navigation_keyboard(),
    )
    await callback.answer()


@router.message(EstimateForm.contact)
async def finish_estimate(
    message: Message,
    state: FSMContext,
    session_factory: async_sessionmaker,
    settings: Settings,
) -> None:
    contact = message.text.strip() if message.text else ""
    if not contact:
        await message.answer("Отправьте Telegram username или ссылку для связи.")
        return

    await state.update_data(contact=contact)
    data = await state.get_data()
    created_at = datetime.now(ZoneInfo(settings.timezone))

    async for session in session_scope(session_factory):
        user = await upsert_user(session, message.from_user)
        await create_application(session, user, data)

    application_text = format_admin_application(
        ApplicationPayload(
            project_type=data["project_type"],
            has_spec=data["has_spec"],
            description=data["description"],
            budget=data["budget"],
            deadline=data["deadline"],
            contact=contact,
            created_at=created_at,
        )
    )
    await message.bot.send_message(settings.admin_chat_id, application_text)
    await state.clear()
    await message.answer(
        APPLICATION_SUCCESS_TEXT,
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(EstimateForm.has_spec, F.data == "form:back")
async def back_to_project_type(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EstimateForm.project_type)
    await callback.message.edit_text(
        "⚡ Получить оценку проекта\n\nЧто необходимо разработать?",
        reply_markup=inline_options_keyboard(PROJECT_TYPES, "project_type", with_back=False),
    )
    await callback.answer()


@router.callback_query(EstimateForm.description, F.data == "form:back")
async def back_to_has_spec(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EstimateForm.has_spec)
    await callback.message.edit_text(
        "Есть ли техническое задание?",
        reply_markup=inline_options_keyboard(TECH_SPEC_OPTIONS, "has_spec"),
    )
    await callback.answer()


@router.callback_query(EstimateForm.budget, F.data == "form:back")
async def back_to_description(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EstimateForm.description)
    await callback.message.edit_text(
        "Опишите проект своими словами.",
        reply_markup=form_navigation_keyboard(),
    )
    await callback.answer()


@router.callback_query(EstimateForm.deadline, F.data == "form:back")
async def back_to_budget(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EstimateForm.budget)
    await callback.message.edit_text(
        "Укажите примерный бюджет.",
        reply_markup=inline_options_keyboard(BUDGET_OPTIONS, "budget"),
    )
    await callback.answer()


@router.callback_query(EstimateForm.contact, F.data == "form:back")
async def back_to_deadline(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EstimateForm.deadline)
    await callback.message.edit_text(
        "Какие сроки реализации?",
        reply_markup=inline_options_keyboard(DEADLINE_OPTIONS, "deadline"),
    )
    await callback.answer()


@router.callback_query(EstimateForm.project_type, F.data == "form:back")
async def back_from_first_step(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "DEVSPACE\n\n"
        "Разрабатываем Telegram-ботов, сайты, CRM, парсеры, Mini Apps и автоматизации.\n"
        "Выберите действие:",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


async def save_option(
    callback: CallbackQuery,
    state: FSMContext,
    options: list[str],
    key: str,
) -> None:
    index = int(callback.data.split(":", 1)[1])
    if index >= len(options):
        await callback.answer("Выберите вариант из списка.", show_alert=True)
        return
    await state.update_data(**{key: options[index]})
