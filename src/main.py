"""Точка входа: CLI-приложение для визуализации зависимостей Maven."""
from __future__ import annotations

import sys

from .config import ConfigError, parse_args, print_config
from .maven import MavenError, get_direct_dependencies


def main() -> None:
    """Точка входа."""
    try:
        config = parse_args()
    except ConfigError as exc:
        print(f"Ошибка конфигурации: {exc}", file=sys.stderr)
        sys.exit(1)

    print_config(config)

    if config.test_mode:
        print(f"\nТестовый режим: файл {config.test_repo_path}")
        print("Прямые зависимости будут прочитаны из этого файла на Этапе 3.")
        return

    print(f"\nЗапрашиваем зависимости для {config.package_name}...")
    try:
        dependencies = get_direct_dependencies(
            config.repo_url,
            config.package_name,
        )
    except MavenError as exc:
        print(f"Ошибка Maven: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\nПрямые зависимости ({len(dependencies)}):")
    if not dependencies:
        print("  (нет)")
    else:
        for dep in dependencies:
            print(f"  {dep.full_name()}")


if __name__ == "__main__":
    main()