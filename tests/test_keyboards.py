from devspace_bot.constants import BUDGET_OPTIONS, MAIN_MENU, PORTFOLIO_CATEGORIES, PROJECT_TYPES
from devspace_bot.keyboards import inline_options_keyboard, main_menu_keyboard, portfolio_keyboard


def test_main_menu_keyboard_has_required_buttons():
    keyboard = main_menu_keyboard()
    labels = [button.text for row in keyboard.inline_keyboard for button in row]

    assert labels == list(MAIN_MENU.values())


def test_inline_options_keyboard_uses_all_options_as_buttons():
    keyboard = inline_options_keyboard(PROJECT_TYPES, prefix="project", with_back=False)
    labels = [button.text for row in keyboard.inline_keyboard for button in row]
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert labels == [*PROJECT_TYPES, "⬅️ На главную"]
    assert callbacks[0] == "project:0"
    assert callbacks[-1] == "menu:start"


def test_budget_keyboard_keeps_every_budget_clickable():
    keyboard = inline_options_keyboard(BUDGET_OPTIONS, prefix="budget")
    labels = [button.text for row in keyboard.inline_keyboard for button in row]
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert labels == [*BUDGET_OPTIONS, "↩️ Отмена", "⬅️ На главную"]
    assert callbacks[-2] == "form:back"


def test_portfolio_keyboard_has_categories_from_database_seed():
    keyboard = portfolio_keyboard(PORTFOLIO_CATEGORIES)
    labels = [button.text for row in keyboard.inline_keyboard for button in row]

    assert labels == [*PORTFOLIO_CATEGORIES, "⬅️ На главную"]
