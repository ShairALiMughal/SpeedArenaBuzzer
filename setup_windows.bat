@echo off
:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...
    :: Download Python installer (modify link for the version you want)
    curl -o python_installer.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    echo Python has been installed.
) else (
    echo Python is already installed.
)

:: Install required packages from requirements.txt
pip install -r requirements.txt

:: Run the Python application
python app.py

pause
