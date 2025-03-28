@echo off
setlocal

cd /d "%~dp0"

if "%VIRTUAL_ENV%"=="" (
    if not exist "venv" (
        echo Creating virtual environment...
        python -m venv venv
    )

    echo Checking dependencies...
    call venv\Scripts\pip install -r requirements.txt

    echo Running game...
    call venv\Scripts\python src\main.py
) else (
    echo Checking dependencies...
    pip install -r requirements.txt

    echo Running game...
    python src\main.py
)

endlocal
