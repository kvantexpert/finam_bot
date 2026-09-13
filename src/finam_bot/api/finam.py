"""Finam API boundary.

The first migration step keeps the existing FinamPy SDK behind a small
application-owned interface. Trading logic must not depend on SDK details.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional

from FinamPy import FinamPy
from FinamPy.grpc.accounts.accounts_service_pb2 import GetAccountRequest
from FinamPy.grpc.assets.assets_service_pb2 import ClockRequest
from FinamPy.grpc.marketdata.marketdata_service_pb2 import QuoteRequest

logger = logging.getLogger(__name__)


class FinamClient:
    """Thin application boundary around the vendored FinamPy SDK."""

    def __init__(self, token: Optional[str] = None, account_id: Optional[str] = None):
        self.token = token
        self.account_id = account_id
        self._client: Optional[FinamPy] = None

    @property
    def connected(self) -> bool:
        return self._client is not None

    def connect(self) -> str:
        if self._client is not None:
            if not self.account_id:
                raise RuntimeError("Счет не выбран")
            return self.account_id

        self._client = FinamPy(self.token) if self.token else FinamPy()
        if not self._client.account_ids:
            self._client = None
            raise RuntimeError("Finam API не вернул доступных счетов")

        if not self.account_id:
            if len(self._client.account_ids) != 1:
                raise RuntimeError(
                    "Доступно несколько счетов; account_id должен быть указан явно"
                )
            self.account_id = self._client.account_ids[0]

        if self.account_id not in self._client.account_ids:
            self._client.close_channel()
            self._client = None
            raise ValueError("Указанный account_id недоступен")

        return self.account_id

    def server_time(self) -> Optional[datetime]:
        if not self._client:
            raise RuntimeError("FinamClient не подключен")
        try:
            response = self._client.call_function(
                self._client.assets_stub.Clock, ClockRequest()
            )
            if response:
                return datetime.fromtimestamp(response.timestamp.seconds)
        except Exception:
            logger.exception("Ошибка получения времени сервера")
        return None

    def account(self) -> Any:
        if not self._client or not self.account_id:
            raise RuntimeError("FinamClient не подключен или счет не выбран")
        return self._client.call_function(
            self._client.accounts_stub.GetAccount,
            GetAccountRequest(account_id=self.account_id),
        )

    def last_quote(self, symbol: str) -> Any:
        if not self._client:
            raise RuntimeError("FinamClient не подключен")
        return self._client.call_function(
            self._client.marketdata_stub.LastQuote,
            QuoteRequest(symbol=symbol),
        )

    def close(self) -> None:
        if self._client:
            self._client.close_channel()
            self._client = None
