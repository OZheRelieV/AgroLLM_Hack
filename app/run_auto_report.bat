@echo off
REM Переходим в корень проекта
cd /d "%~dp0.."

REM 1. Пробуем python из poetry
for /f "delims=" %%i in ('poetry env info --path 2^>nul') do set VENV_PATH=%%i
if exist "%VENV_PATH%\Scripts\python.exe" (
    set "PYTHON_PATH=%VENV_PATH%\Scripts\python.exe"
    echo Использую python из poetry: %PYTHON_PATH%
) else (
    set "PYTHON_PATH="
)

REM 2. Пробуем python из .venv
if not defined PYTHON_PATH if exist ".venv\Scripts\python.exe" (
    set "PYTHON_PATH=.venv\Scripts\python.exe"
    echo Использую python из .venv: %PYTHON_PATH%
)

REM 3. Пробуем системный python
if not defined PYTHON_PATH (
    where python >nul 2>nul && set "PYTHON_PATH=python" && echo Использую системный python
)

if not defined PYTHON_PATH (
    echo Не удалось найти подходящий python!
    pause
    exit /b
)

REM Запускаем и логируем вывод
"%PYTHON_PATH%" app\auto_report.py > app\run_auto_report.bat.log 2>&1 