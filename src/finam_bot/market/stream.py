"""Finam quote-stream adapter.

The adapter keeps FinamPy subscription details outside the domain model.
"""

from __future__ import annotations

import logging
import threading
from datetime import datetime
from typing import Callable, Dict, Optional

from .models import Quote

logger = logging.getLogger(__name__)


class QuoteStream:
    """Translate FinamPy quote events into application-owned Quote objects."""

    def __init__(self, client, symbols: list[str]):
        self.client = client
        self.symbols = list(symbols)
        self.quotes: Dict[str, Quote] = {}
        self.callbacks: list[Callable[[Quote], None]] = []
        self.running = False
        self.updates = 0
        self.started_at: Optional[datetime] = None

    def add_callback(self, callback: Callable[[Quote], None]) -> None:
        self.callbacks.append(callback)

    @staticmethod
    def _value(field) -> float:
        return float(field.value) if field and field.value else 0.0

    def _handle(self, response) -> None:
        for item in response.quote:
            quote = Quote(
                symbol=item.symbol,
                bid=self._value(item.bid),
                ask=self._value(item.ask),
                last=self._value(item.last),
                volume=int(self._value(item.volume)),
                timestamp=datetime.now(),
            )
            self.quotes[quote.symbol] = quote
            self.updates += 1
            for callback in self.callbacks:
                try:
                    callback(quote)
                except Exception:
                    logger.exception("Ошибка callback котировки %s", quote.symbol)

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.started_at = datetime.now()
        self.client.on_quote.subscribe(self._handle)
        thread = threading.Thread(
            target=self.client.subscribe_quote_thread,
            args=(tuple(self.symbols),),
            daemon=True,
        )
        thread.start()

    def stop(self) -> None:
        self.running = False

    def get(self, symbol: str) -> Optional[Quote]:
        return self.quotes.get(symbol)
