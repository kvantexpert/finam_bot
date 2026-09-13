"""Arbitrage triangle domain types.

This module defines structure only. It deliberately does not reproduce the
legacy triangle formulas until the real Finam instrument universe is verified.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Triangle:
    """A three-leg conversion cycle."""

    symbols: Tuple[str, str, str]

    def __post_init__(self) -> None:
        if len(self.symbols) != 3:
            raise ValueError("Треугольник должен содержать ровно 3 инструмента")
