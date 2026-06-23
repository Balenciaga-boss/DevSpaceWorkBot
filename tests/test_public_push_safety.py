import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_push_check_passes():
    result = subprocess.run(
        [sys.executable, "scripts/public_push_check.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_env_examples_do_not_contain_real_secrets():
    for filename in [".env.example", ".env.beget.example"]:
        text = (ROOT / filename).read_text(encoding="utf-8")

        assert "replace_with_" in text
        assert ("change" + "_me") not in text
        assert "123456:" not in text
