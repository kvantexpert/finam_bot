"""Execution boundary.

Live order execution is intentionally not implemented during the structural
migration. Keeping this boundary explicit prevents legacy order logic from
being mistaken for a safe execution engine.
"""


class ExecutionDisabledError(RuntimeError):
    """Raised when live execution is requested before the engine is ready."""


class Executor:
    """Placeholder for a future fill-aware execution engine."""

    def place_order(self, *args, **kwargs):
        raise ExecutionDisabledError(
            "Live execution отключено до реализации risk/fill/reconciliation"
        )
