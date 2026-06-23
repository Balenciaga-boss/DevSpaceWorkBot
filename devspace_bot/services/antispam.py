from dataclasses import dataclass, field


@dataclass
class CooldownGuard:
    cooldown_seconds: int
    _last_started_at: dict[int, float] = field(default_factory=dict)

    def can_start(self, user_id: int, now: float) -> bool:
        last_started_at = self._last_started_at.get(user_id)
        if last_started_at is None:
            return True
        return now - last_started_at >= self.cooldown_seconds

    def mark_started(self, user_id: int, now: float) -> None:
        self._last_started_at[user_id] = now

