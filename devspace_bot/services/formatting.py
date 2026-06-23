from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ApplicationPayload:
    project_type: str
    has_spec: str
    description: str
    budget: str
    deadline: str
    contact: str
    created_at: datetime


def format_admin_application(payload: ApplicationPayload) -> str:
    created_at = payload.created_at.strftime("%d.%m.%Y %H:%M")
    return (
        "🚀 Новая заявка DEVSPACE\n\n"
        f"Тип проекта:\n{payload.project_type}\n\n"
        f"Есть ТЗ:\n{payload.has_spec}\n\n"
        f"Описание:\n{payload.description}\n\n"
        f"Бюджет:\n{payload.budget}\n\n"
        f"Сроки:\n{payload.deadline}\n\n"
        f"Контакт:\n{payload.contact}\n\n"
        f"Дата:\n{created_at}"
    )

