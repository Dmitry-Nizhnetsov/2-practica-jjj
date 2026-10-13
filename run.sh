#!/bin/bash
# Пример запуска с тестовым репозиторием
cd "$(dirname "$0")"
python3 -m src.main \
    --package A \
    --test-repo data/test_repo.txt \
    --test-mode \
    --ascii-tree