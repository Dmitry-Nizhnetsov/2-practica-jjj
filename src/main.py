from __future__ import annotations

import sys

from .config import ConfigError, parse_args, print_config


def main() -> None:

    try:
        config = parse_args()
    except ConfigError as exc:
        print(f"Ошибка конфигурации: {exc}", file=sys.stderr)
        sys.exit(1)

    # Этап 1: вывести все параметры в формате ключ-значение
    print_config(config)

    # Здесь будут следующие этапы:
    # - Этап 2: сбор данных о зависимостях
    # - Этап 3: построение графа
    # - Этап 4: обратные зависимости
    # - Этап 5: визуализация


if __name__ == "__main__":
    main()