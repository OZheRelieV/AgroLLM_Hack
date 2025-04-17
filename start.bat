@echo off
REM Универсальный запуск Streamlit-приложения
cd /d "%~dp0"

REM 1. Пробуем poetry run
poetry run streamlit run app/streamlit_app.py
if %errorlevel% equ 0 goto end

echo Не удалось запустить через poetry run, пробую python из poetry env info --path...
for /f "delims=" %%i in ('poetry env info --path 2^>nul') do set VENV_PATH=%%i
if exist "%VENV_PATH%\Scripts\python.exe" (
    set "PYTHON_PATH=%VENV_PATH%\Scripts\python.exe"
    echo Использую python из poetry: %PYTHON_PATH%
    "%PYTHON_PATH%" -m streamlit run app/streamlit_app.py
    if %errorlevel% equ 0 goto end
)

REM 2. Пробуем python из .venv
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_PATH=.venv\Scripts\python.exe"
    echo Использую python из .venv: %PYTHON_PATH%
    "%PYTHON_PATH%" -m streamlit run app/streamlit_app.py
    if %errorlevel% equ 0 goto end
)

REM 3. Пробуем системный python
where python >nul 2>nul && set "PYTHON_PATH=python" && echo Использую системный python && %PYTHON_PATH% -m streamlit run app/streamlit_app.py
if %errorlevel% equ 0 goto end

echo Не удалось найти подходящий python или запустить Streamlit!
pause
exit /b

:end
pause 