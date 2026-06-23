# DEVSPACE Telegram Bot

Telegram bot for collecting project estimate requests for DEVSPACE.

## Features

- Aiogram 3 FSM questionnaire.
- All options are inline buttons.
- MySQL storage for users, applications, portfolio categories, and cases.
- Admin chat notification for each new request.
- Simple anti-spam cooldown.
- VPS-ready `systemd` unit example.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_CHAT_ID=your_admin_chat_id
DATABASE_URL=mysql+asyncmy://user:password@127.0.0.1:3306/devspace_bot
```

Create database:

```sql
CREATE DATABASE devspace_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Run:

```powershell
.\.venv\Scripts\python.exe -m devspace_bot
```

## VPS systemd

Copy `deploy/devspace-bot.service` to `/etc/systemd/system/devspace-bot.service`, adjust paths, then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now devspace-bot
sudo journalctl -u devspace-bot -f
```

## Beget VPS with Docker Compose

Use `.env.beget.example` and `compose.yaml` for Docker deployment:

```bash
cp .env.beget.example .env
nano .env
docker compose up -d --build
docker compose logs -f devspace-bot
```

Full Beget notes are in `deploy/beget.md`.
