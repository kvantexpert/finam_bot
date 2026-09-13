"""Market data models.

These models are intentionally independent from the current legacy
arbitrage implementation. Trading semantics will be migrated separately.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Quote:
    """A single bid/ask quote."""

    symbol: str
    bid: float
    ask: float
    last: float = 0.0
    volume: int = 0
    timestamp: Optional[datetime] = None

    @property
    def spread(self) -> float:
        return max(0.0, self.ask - self.bid)

    @property
    def is_valid(self) -> bool:
        return self.bid > 0 and self.ask > 0 and self.ask >= self.bid
