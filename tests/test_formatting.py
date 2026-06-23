from datetime import datetime
from zoneinfo import ZoneInfo

from devspace_bot.services.formatting import ApplicationPayload, format_admin_application


def test_format_admin_application_contains_devspace_request_details():
    payload = ApplicationPayload(
        project_type="Telegram-бот",
        has_spec="Да",
        description="Нужен бот для приема заявок",
        budget="$300-700",
        deadline="1-4 недели",
        contact="@client",
        created_at=datetime(2026, 6, 23, 12, 30, tzinfo=ZoneInfo("Europe/Bucharest")),
    )

    text = format_admin_application(payload)

    assert "🚀 Новая заявка DEVSPACE" in text
    assert "Тип проекта:\nTelegram-бот" in text
    assert "Есть ТЗ:\nДа" in text
    assert "Описание:\nНужен бот для приема заявок" in text
    assert "Бюджет:\n$300-700" in text
    assert "Сроки:\n1-4 недели" in text
    assert "Контакт:\n@client" in text
    assert "Дата:\n23.06.2026 12:30" in text

