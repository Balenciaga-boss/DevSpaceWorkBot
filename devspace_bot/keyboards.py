from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from devspace_bot.constants import MAIN_MENU

HOME_BUTTON_TEXT = "⬅️ На главную"
BACK_BUTTON_TEXT = "↩️ Отмена"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MAIN_MENU["estimate"], callback_data="menu:estimate")],
            [InlineKeyboardButton(text=MAIN_MENU["portfolio"], callback_data="menu:portfolio")],
            [InlineKeyboardButton(text=MAIN_MENU["contacts"], callback_data="menu:contacts")],
        ]
    )


def inline_options_keyboard(options: list[str], prefix: str, with_back: bool = True) -> InlineKeyboardMarkup:
    navigation = []
    if with_back:
        navigation.append([InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="form:back")])
    navigation.append([InlineKeyboardButton(text=HOME_BUTTON_TEXT, callback_data="menu:start")])

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=option, callback_data=f"{prefix}:{index}")]
            for index, option in enumerate(options)
        ]
        + navigation
    )


def portfolio_keyboard(categories: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=category, callback_data=f"portfolio:{index}")]
            for index, category in enumerate(categories)
        ]
        + [[InlineKeyboardButton(text=HOME_BUTTON_TEXT, callback_data="menu:start")]]
    )


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=HOME_BUTTON_TEXT, callback_data="menu:start")]
        ]
    )


def form_navigation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="form:back")],
            [InlineKeyboardButton(text=HOME_BUTTON_TEXT, callback_data="menu:start")],
        ]
    )
