from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class Config:


    package_name: str
    repo_url: str | None
    test_repo_path: str | None
    test_mode: bool
    ascii_tree: bool


class ConfigError(Exception):
    """Ошибка конфигурации."""


def parse_args(argv: list[str] | None = None) -> Config:

    parser = argparse.ArgumentParser(
        description="Визуализатор графа зависимостей Maven-пакетов"
    )
    parser.add_argument(
        "--package", "-p",
        type=str,
        required=True,
        help="Имя анализируемого пакета (например: org.example:library)",
    )
    parser.add_argument(
        "--repo", "-r",
        type=str,
        default=None,
        help="URL-адрес Maven-репозитория",
    )
    parser.add_argument(
        "--test-repo",
        type=str,
        default=None,
        help="Путь к файлу описания тестового репозитория",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Режим работы с тестовым репозиторием",
    )
    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Выводить зависимости в формате ASCII-дерева",
    )

    args = parser.parse_args(argv)

    # Валидация
    if args.test_mode:
        if not args.test_repo:
            raise ConfigError(
                "В режиме --test-mode обязателен параметр --test-repo"
            )
    else:
        if not args.repo:
            raise ConfigError(
                "Для работы с реальным репозиторием укажите --repo "
                "или включите --test-mode"
            )
        if args.test_repo:
            raise ConfigError(
                "Параметр --test-repo используется только с --test-mode"
            )

    return Config(
        package_name=args.package,
        repo_url=args.repo,
        test_repo_path=args.test_repo,
        test_mode=args.test_mode,
        ascii_tree=args.ascii_tree,
    )


def print_config(config: Config) -> None:

    print("=" * 40)
    print("Параметры запуска:")
    print(f"  package_name:   {config.package_name}")
    print(f"  repo_url:       {config.repo_url}")
    print(f"  test_repo_path: {config.test_repo_path}")
    print(f"  test_mode:      {config.test_mode}")
    print(f"  ascii_tree:     {config.ascii_tree}")
    print("=" * 40)