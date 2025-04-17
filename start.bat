@echo off
REM Запуск Streamlit-приложения
REM Убедитесь, что Poetry установлен и активен
poetry run streamlit run app/streamlit_app.py
if %errorlevel% neq 0 (
    echo Ошибка при запуске Streamlit!
    pause
    exit /b
)
pause 