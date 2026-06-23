from devspace_bot.services.antispam import CooldownGuard


def test_cooldown_guard_allows_first_action():
    guard = CooldownGuard(cooldown_seconds=3)

    assert guard.can_start(user_id=10, now=1000.0) is True


def test_cooldown_guard_blocks_repeated_action_inside_window():
    guard = CooldownGuard(cooldown_seconds=3)

    guard.mark_started(user_id=10, now=1000.0)

    assert guard.can_start(user_id=10, now=1002.0) is False


def test_cooldown_guard_allows_after_window_expires():
    guard = CooldownGuard(cooldown_seconds=3)

    guard.mark_started(user_id=10, now=1000.0)

    assert guard.can_start(user_id=10, now=1003.1) is True
