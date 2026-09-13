# Структура репозитория Finam Bot

## Принцип

Репозиторий разделён на четыре зоны:

1. **`src/finam_bot/`** — новый собственный код;
2. **`docs/`** — контекст, решения и план;
3. **legacy** — старый код, который временно поддерживается и постепенно удаляется;
4. **внешние/служебные компоненты** — `FinamPy`, examples и runtime-инфраструктура.

Новые возможности должны появляться в `src/finam_bot/`, а не в legacy-каталогах.

## Текущая структура

```text
finam_bot/
│
├── src/
│   └── finam_bot/
│       ├── __init__.py
│       ├── app.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── finam.py
│       ├── market/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── quotes.py
│       │   └── stream.py
│       ├── strategy/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── pricing.py
│       │   └── triangles.py
│       ├── risk/
│       │   ├── __init__.py
│       │   └── limits.py
│       ├── execution/
│       │   ├── __init__.py
│       │   └── executor.py
│       └── monitoring/
│           ├── __init__.py
│           ├── currency.py
│           └── quotes.py
│
├── tests/                  # тесты; постепенно расширяются
├── examples/               # безопасные reference-примеры
├── docs/
│   ├── PROJECT.md          # что это за проект
│   ├── STATUS.md           # где мы сейчас
│   ├── STRUCTURE.md        # как устроен репозиторий
│   ├── ROADMAP.md          # что делать дальше
│   └── DECISIONS.md        # почему приняты ключевые решения
│
├── core/                   # LEGACY, заморожен
├── config/                 # LEGACY-конфигурация, мигрируется отдельно
├── diagnostics/            # LEGACY-диагностика
├── FinamPy/                # vendored SDK; не domain-код приложения
├── Examples/               # старые примеры SDK
├── arbitrage_trader.py     # LEGACY entrypoint
├── arbitrage_finder.py     # LEGACY entrypoint
├── currency_monitor_cli.py # LEGACY entrypoint
├── run_arbitrage.py        # compatibility wrapper
├── requirements.txt
└── README.md
```

## Целевая структура

После завершения миграции структура должна быть ближе к:

```text
finam_bot/
├── src/
│   └── finam_bot/
│       ├── api/
│       ├── market/
│       ├── strategy/
│       ├── risk/
│       ├── execution/
│       ├── monitoring/
│       ├── config.py
│       └── app.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fakes/
├── examples/
├── docs/
├── pyproject.toml
└── README.md
```

## Ответственность каталогов

### `api/`

Единственная граница с Finam API. Здесь допустимы protobuf и детали SDK.

### `market/`

Нормализованные рыночные данные приложения: инструменты, котировки, freshness и stream.

### `strategy/`

Сигналы и математическая модель стратегии. Strategy не должна сама отправлять заявки.

### `risk/`

Проверка допустимости операции до execution.

### `execution/`

Order plan, отправка заявок, состояния заявок, fills, partial fills и unwind.

### `monitoring/`

Наблюдение за состоянием рынка и приложения. Monitoring не должен незаметно инициировать торговлю.

### `app.py`

Собирает application components и определяет точку запуска.

## Правила миграции

1. Сначала найти все зависимости старого файла.
2. Перенести ответственность в новый слой.
3. Добавить smoke/unit-тесты.
4. Оставить compatibility wrapper, если он нужен.
5. Проверить, что новый код не импортирует `core.*`.
6. Только после этого удалять legacy-файл.

## Что нельзя переносить механически

Не копировать в новую архитектуру без проверки:

- `POINT = 0.0001`;
- magic coefficients для лотов;
- автоматический выбор первого счёта;
- старую модель cross-triangles;
- `CancelOrder` как закрытие позиции;
- последовательные market orders без контроля fills;
- live execution без reconciliation.

## Runtime-файлы

Следующие данные не являются частью исходного проекта и не должны попадать в Git:

- `.venv/`, `venv/`;
- `__pycache__/`;
- `build/`, `dist/`, `*.egg-info/`;
- `*.log`;
- runtime data;
- `.env` и секреты;
- локальные generated reports.
