"""Quote conversion and storage."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from .models import Quote


class QuoteStore:
    """In-memory latest-quote store, independent from FinamPy protobufs."""

    def __init__(self) -> None:
        self._quotes: Dict[str, Quote] = {}

    def update(self, quote: Quote) -> None:
        self._quotes[quote.symbol] = quote

    def get(self, symbol: str) -> Optional[Quote]:
        return self._quotes.get(symbol)

    def all(self) -> Dict[str, Quote]:
        return dict(self._quotes)

    def is_fresh(self, symbol: str, max_age_seconds: float) -> bool:
        quote = self.get(symbol)
        if quote is None or quote.timestamp is None:
            return False
        age = (datetime.now() - quote.timestamp).total_seconds()
        return age <= max_age_seconds
