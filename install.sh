#!/bin/bash
set -e

# Проверка Python
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python не найден. Установите Python 3 вручную."
  exit 1
fi

# Проверка Poetry
if ! command -v poetry >/dev/null 2>&1; then
  echo "Poetry не найден. Устанавливаю Poetry..."
  curl -sSL https://install.python-poetry.org | python3 -
  export PATH="$HOME/.local/bin:$PATH"
fi

# Установка зависимостей
poetry install --no-root

# Активируем окружение Poetry (создаём, если не было)
poetry env use python3
VENV_PATH=$(poetry env info --path 2>/dev/null)
if [ -x "$VENV_PATH/bin/python" ]; then
  echo "Poetry-окружение успешно создано: $VENV_PATH"
  echo "Для запуска используйте ./start.sh"
else
  echo "Не удалось создать poetry-окружение! Проверьте установку Python и Poetry."
fi

echo "Установка завершена!" 