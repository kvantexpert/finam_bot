"""Pricing primitives for strategy signals.

Legacy fixed-point and magic lot formulas are intentionally not migrated here.
Instrument metadata must define price precision and quantity steps first.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..market.models import Quote


@dataclass(frozen=True)
class Deviation:
    """Raw price deviation before costs and risk adjustments."""

    value: float
    unit: str = "price"


def validate_quotes(quotes: Sequence[Quote]) -> None:
    if len(quotes) != 3:
        raise ValueError("Для треугольной стратегии нужны ровно 3 котировки")
    if not all(quote.is_valid for quote in quotes):
        raise ValueError("Все котировки должны быть валидными")
