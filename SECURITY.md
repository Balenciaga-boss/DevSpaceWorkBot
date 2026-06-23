# Security

## Public Repository Safety

This repository is safe to publish only when real runtime secrets are kept out of Git.

Never commit:

- `.env`
- Telegram bot tokens
- admin chat IDs
- production database passwords
- local SQLite databases
- logs
- virtual environments

Before pushing, run:

```bash
python scripts/public_push_check.py
```

If a real Telegram bot token was ever committed or shared, revoke it in BotFather and create a new token before running the bot in production.

## Runtime Secrets

Use `.env.example` or `.env.beget.example` as templates only. Copy one of them to `.env` on the server and fill real values there.

## Data Storage

Production Docker deployment uses MySQL with a named Docker volume. Local SQLite files are ignored and must not be published.

