@echo off
REM Переходим в корень проекта
cd /d "%~dp0.."
set "PYTHON_PATH=.venv\Scripts\python.exe"
if not exist "%PYTHON_PATH%" (
    echo Не найден python в виртуальном окружении, пробую системный python...
    set "PYTHON_PATH=python"
)
"%PYTHON_PATH%" app\auto_report.py 