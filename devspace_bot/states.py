from aiogram.fsm.state import State, StatesGroup


class EstimateForm(StatesGroup):
    project_type = State()
    has_spec = State()
    description = State()
    budget = State()
    deadline = State()
    contact = State()

