@echo off
REM Переходим в корень проекта
cd /d "%~dp0.."

poetry run python app\auto_report.py

pause 