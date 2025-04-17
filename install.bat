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
    REM Добавляем путь к Poetry в PATH (универсально для всех версий Python)
    set "PATH=%USERPROFILE%\AppData\Roaming\Python\Python*\Scripts;%PATH%"
    REM Если не сработает, попросите перезапустить консоль или вручную добавить путь
)

REM Установка зависимостей
poetry install --no-root

if %errorlevel% neq 0 (
    echo Ошибка при установке зависимостей!
    pause
    exit /b
)

echo Установка завершена!
pause 