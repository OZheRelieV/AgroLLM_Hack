@echo off
REM Проверка Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python не найден. Откройте страницу загрузки и установите Python вручную.
    start https://www.python.org/downloads/
    pause
    exit /b
)

REM Проверка Poetry
where poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo Poetry не найден. Устанавливаю Poetry...
    python -m pip install --user poetry
    set PATH=%USERPROFILE%\AppData\Roaming\Python\Python39\Scripts;%PATH%
)

REM Установка зависимостей
poetry install --no-root

echo Установка завершена!
pause 