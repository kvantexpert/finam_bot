"""Risk limits used by the application layer."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskLimits:
    """Explicit limits; no live execution is implied by this model."""

    max_open_triangles: int = 0
    max_order_notional: float = 0.0
    max_daily_loss: float = 0.0

    def validate(self) -> None:
        if self.max_open_triangles < 0:
            raise ValueError("max_open_triangles не может быть отрицательным")
        if self.max_order_notional < 0 or self.max_daily_loss < 0:
            raise ValueError("Денежные лимиты не могут быть отрицательными")
