"""Application-level quote monitoring."""

from datetime import datetime

from ..market.models import Quote
from ..market.quotes import QuoteStore


class QuoteMonitor:
    """Small monitor facade over the market quote store."""

    def __init__(self, store: QuoteStore | None = None) -> None:
        self.store = store or QuoteStore()
        self.started_at: datetime | None = None

    def start(self) -> None:
        self.started_at = datetime.now()

    def update(self, quote: Quote) -> None:
        self.store.update(quote)

    def get(self, symbol: str) -> Quote | None:
        return self.store.get(symbol)
