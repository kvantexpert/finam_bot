"""Strategy-domain models migrated from the legacy arbitrage core."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ..market.models import Quote


@dataclass
class TriangleState:
    """Runtime state of a strategy triangle.

    This is a state container only. It does not define how positions are
    opened or closed.
    """

    triangle_type: int = -1
    direction: int = 0
    order_ids: List[str] = field(default_factory=lambda: ["", "", ""])
    entry_prices: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    quantities: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    deviation: float = 0.0
    current_profit: float = 0.0
    open_time: Optional[datetime] = None
    active: bool = False
    compensation: bool = False
    parent_index: int = -1
    symbols: List[str] = field(default_factory=list)

    def side_for_leg(self, index: int) -> str:
        if not 0 <= index < 3:
            raise IndexError("Индекс ноги должен быть от 0 до 2")
        if self.direction == 1:
            return "BUY" if index < 2 else "SELL"
        return "SELL" if index < 2 else "BUY"


@dataclass(frozen=True)
class Opportunity:
    """Strategy signal. Profitability must be decided by pricing/risk."""

    triangle_type: int
    direction: int
    deviation: float
    quotes: List[Quote]
    signal_type: str
    description: str
