@echo off
REM Универсальный запуск Streamlit-приложения с логированием
cd /d "%~dp0"
set LOGFILE=start.bat.log
if exist %LOGFILE% del %LOGFILE%

REM 1. Пробуем poetry run
poetry run streamlit run app/streamlit_app.py > %LOGFILE% 2>&1
if %errorlevel% equ 0 goto showlog

echo Не удалось запустить через poetry run, пробую python из poetry env info --path... >> %LOGFILE%
for /f "delims=" %%i in ('poetry env info --path 2^>nul') do set VENV_PATH=%%i
if exist "%VENV_PATH%\Scripts\python.exe" (
    set "PYTHON_PATH=%VENV_PATH%\Scripts\python.exe"
    echo Использую python из poetry: %PYTHON_PATH% >> %LOGFILE%
    "%PYTHON_PATH%" -m streamlit run app/streamlit_app.py >> %LOGFILE% 2>&1
    if %errorlevel% equ 0 goto showlog
)

REM 2. Пробуем python из .venv
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_PATH=.venv\Scripts\python.exe"
    echo Использую python из .venv: %PYTHON_PATH% >> %LOGFILE%
    "%PYTHON_PATH%" -m streamlit run app/streamlit_app.py >> %LOGFILE% 2>&1
    if %errorlevel% equ 0 goto showlog
)

REM 3. Пробуем системный python
where python >nul 2>nul && set "PYTHON_PATH=python" && echo Использую системный python >> %LOGFILE% && %PYTHON_PATH% -m streamlit run app/streamlit_app.py >> %LOGFILE% 2>&1
if %errorlevel% equ 0 goto showlog

echo Не удалось найти подходящий python или запустить Streamlit! >> %LOGFILE%

:showlog
REM Показываем последние 40 строк лога (если есть powershell)
where powershell >nul 2>nul && powershell -Command "Get-Content -Path '%LOGFILE%' -Tail 40" || type %LOGFILE%
pause 