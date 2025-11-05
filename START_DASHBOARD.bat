@echo off
echo ========================================
echo  BNT113 Trial Dashboard - VM Startup
echo ========================================
echo.
echo Starting on SRV04750.soton.ac.uk...
echo.

:: Change to the dashboard directory
cd /d "%~dp0"

echo Dashboard Location: %CD%
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo Python found!
python --version
echo.

:: Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Streamlit is not installed!
    echo Installing required packages...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        echo Please run: pip install -r requirements.txt
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
)

echo All dependencies are installed!
echo.

:: Wait a moment before starting
timeout /t 2 /nobreak >nul

:: Start Streamlit in the background and open browser
echo Opening dashboard in your default browser...
echo Dashboard URL: http://localhost:8501
echo.
start "" "http://localhost:8501"

:: Start Streamlit server
echo Starting Streamlit server...
echo Press Ctrl+C to stop the dashboard.
echo.
python -m streamlit run streamlit_dashboard_bnt113_real_data.py --server.port 8501 --server.address localhost --server.headless true

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Failed to start dashboard!
    echo ========================================
    echo.
    echo Common solutions:
    echo 1. Check if port 8501 is already in use
    echo 2. Verify Python and dependencies are installed
    echo 3. Check the data files are accessible
    echo.
    echo Press any key to close...
    pause >nul
)

