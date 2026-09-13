"""Application entry point for the refactored trading bot.

The legacy execution engine is intentionally not wired here. This module is
an application boundary for the new architecture and keeps live execution
disabled until market universe, pricing, risk and fill handling are complete.
"""

from __future__ import annotations

import argparse
import logging

from .api.finam import FinamClient
from .execution.executor import ExecutionDisabledError, Executor
from .risk.limits import RiskLimits

logger = logging.getLogger(__name__)


class ArbitrageApp:
    """Application facade for the refactored architecture."""

    def __init__(
        self,
        token: str | None = None,
        account_id: str | None = None,
        paper: bool = False,
    ) -> None:
        self.paper = paper
        self.client = FinamClient(token=token, account_id=account_id)
        self.risk = RiskLimits()
        self.executor = Executor()

    def check(self) -> None:
        """Validate local application components without connecting to Finam."""
        self.risk.validate()
        logger.info("Новая архитектура приложения загружена")
        logger.info("Live execution отключено")

    def run(self) -> None:
        """Run the application in its current safe migration state."""
        self.check()
        raise ExecutionDisabledError(
            "Торговый запуск отключен: новый execution engine еще не реализован"
        )

    def close(self) -> None:
        self.client.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Finam arbitrage application")
    parser.add_argument("--token", help="Finam API token")
    parser.add_argument("--account-id", help="Finam account id")
    parser.add_argument(
        "--paper",
        action="store_true",
        help="Зарезервировано для будущего paper mode",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Проверить загрузку новой архитектуры без подключения к Finam",
    )
    args = parser.parse_args()

    app = ArbitrageApp(
        token=args.token,
        account_id=args.account_id,
        paper=args.paper,
    )
    try:
        if args.check:
            app.check()
            return 0
        app.run()
    except ExecutionDisabledError as exc:
        logger.error("%s", exc)
        return 2
    finally:
        app.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
