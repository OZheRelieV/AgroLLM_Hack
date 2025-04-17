@echo off
REM Запуск Streamlit-приложения через poetry run
cd /d "%~dp0"

poetry run streamlit run app/streamlit_app.py

pause 