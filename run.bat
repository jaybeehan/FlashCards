@echo off
cd /d "%~dp0"
set PY=
py -3 --version >nul 2>nul && set PY=py -3
if not defined PY (
    python --version >nul 2>nul && set PY=python
)
if not defined PY (
    echo Python 3 is not installed. Get it from https://www.python.org/downloads/
    pause
    exit /b 1
)
rem Keep the virtual environment on the local disk (venvs break on network drives).
set VENV=%LOCALAPPDATA%\AlbertaFlashCards\venv
if not exist "%VENV%\Scripts\python.exe" %PY% -m venv "%VENV%"
"%VENV%\Scripts\python" -c "import reportlab" >nul 2>nul
if errorlevel 1 (
    echo Installing reportlab...
    "%VENV%\Scripts\python" -m pip install -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo.
        echo Install failed - see the message above.
        pause
        exit /b 1
    )
)
"%VENV%\Scripts\python" flashcards.py
pause
