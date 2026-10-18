from __future__ import annotations

import sys

from .config import ConfigError, parse_args, print_config


def main() -> None:

    try:
        config = parse_args()
    except ConfigError as exc:
        print(f"Ошибка конфигурации: {exc}", file=sys.stderr)
        sys.exit(1)

    print_config(config)


if __name__ == "__main__":
    main()