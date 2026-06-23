from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dockerfile_runs_bot_module():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "FROM python:3.11-slim" in dockerfile
    assert 'CMD ["python", "-m", "devspace_bot"]' in dockerfile


def test_compose_uses_bot_and_mysql_services():
    compose = (ROOT / "compose.yaml").read_text(encoding="utf-8")

    assert "devspace-bot:" in compose
    assert "mysql:" in compose
    assert "env_file:" in compose
    assert "restart: unless-stopped" in compose
    assert "mysql_data:" in compose


def test_dockerignore_excludes_local_secrets_and_runtime_files():
    dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")

    assert ".env" in dockerignore
    assert ".venv" in dockerignore
    assert "logs" in dockerignore
    assert "devspace_bot.db" in dockerignore
