"""Currency monitoring models, independent from terminal presentation."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, Optional


@dataclass
class CurrencyData:
    code: str
    name: str
    symbol: str
    bid: float = 0.0
    ask: float = 0.0
    last: float = 0.0
    change: float = 0.0
    change_percent: float = 0.0
    volume: int = 0
    timestamp: Optional[datetime] = None
    history: Deque[dict] = field(default_factory=lambda: deque(maxlen=100))

    def update(
        self,
        bid: float,
        ask: float,
        last: float,
        volume: int,
        timestamp: datetime,
    ) -> None:
        old_last = self.last
        self.bid, self.ask, self.last = bid, ask, last
        self.volume = volume
        self.timestamp = timestamp
        if old_last > 0:
            self.change = last - old_last
            self.change_percent = self.change / old_last * 100
        self.history.append(
            {"timestamp": timestamp, "last": last, "bid": bid, "ask": ask}
        )

    @property
    def spread(self) -> float:
        if self.bid > 0 and self.ask > 0:
            return self.ask - self.bid
        return 0.0


class AlertSystem:
    """Stateful alert throttling without terminal/network side effects."""

    def __init__(self, threshold_percent: float = 0.5, cooldown_seconds: int = 60):
        self.threshold = threshold_percent
        self.cooldown_seconds = cooldown_seconds
        self.last_alert: dict[str, datetime] = {}

    def should_alert(self, code: str, currency: CurrencyData, now: Optional[datetime] = None) -> bool:
        if abs(currency.change_percent) < self.threshold:
            return False
        now = now or datetime.now()
        previous = self.last_alert.get(code)
        if previous and (now - previous).total_seconds() <= self.cooldown_seconds:
            return False
        self.last_alert[code] = now
        return True
