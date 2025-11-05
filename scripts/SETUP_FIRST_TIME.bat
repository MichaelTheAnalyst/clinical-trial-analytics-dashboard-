@echo off
echo ================================================================================
echo  BNT113 Dashboard - First Time Setup
echo ================================================================================
echo.
echo This script will:
echo   1. Check if Python is installed
echo   2. Install all required dependencies
echo   3. Verify the installation
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

:: Change to the dashboard directory
cd /d "%~dp0"

echo.
echo ================================================================================
echo STEP 1: Checking Python Installation
echo ================================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher:
    echo   1. Download from: https://www.python.org/downloads/
    echo   2. Run the installer
    echo   3. ✅ Check "Add Python to PATH" during installation
    echo   4. Re-run this script after installation
    echo.
    echo Press any key to open the Python download page...
    pause >nul
    start "" "https://www.python.org/downloads/"
    exit /b 1
)

echo ✅ Python is installed!
python --version
echo.

echo ================================================================================
echo STEP 2: Installing Dependencies
echo ================================================================================
echo.
echo Installing required packages from requirements.txt...
echo This may take a few minutes...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to install dependencies!
    echo.
    echo Troubleshooting:
    echo   1. Check your internet connection
    echo   2. Try running: pip install --upgrade pip
    echo   3. Then run this script again
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo.
echo ✅ All dependencies installed successfully!
echo.

echo ================================================================================
echo STEP 3: Verifying Installation
echo ================================================================================
echo.

echo Checking installed packages...
python -c "import streamlit; import pandas; import plotly; print('✅ Core packages verified!')" 2>&1
if errorlevel 1 (
    echo ❌ WARNING: Some packages may not have installed correctly
    echo Try reinstalling: pip install -r requirements.txt --force-reinstall
)

echo.
echo ================================================================================
echo STEP 4: Setup Complete!
echo ================================================================================
echo.
echo ✅ Setup completed successfully!
echo.
echo Next steps:
echo   1. Place your Excel data files in the "data" folder
echo      (or upload them through the dashboard later)
echo.
echo   2. Double-click "START_DASHBOARD.bat" to launch the dashboard
echo.
echo   3. The dashboard will open at: http://localhost:8501
echo.
echo   4. Login with default credentials:
echo      Username: admin
echo      Password: sctu2024
echo      (⚠️ Change the password after first login!)
echo.
echo ================================================================================
echo.
echo Would you like to start the dashboard now? (Y/N)
set /p choice="> "

if /i "%choice%"=="Y" (
    echo.
    echo Starting dashboard...
    echo.
    echo Note: Using 'python -m streamlit' to ensure compatibility
    echo.
    timeout /t 2 /nobreak >nul
    call START_DASHBOARD.bat
) else (
    echo.
    echo Setup complete! Run START_DASHBOARD.bat when ready.
    echo.
    timeout /t 3 /nobreak >nul
)

