@echo off
echo ========================================
echo  BNT113 Dashboard - Network Access Mode
echo ========================================
echo.
echo This will start the dashboard with NETWORK ACCESS enabled.
echo.
echo Dashboard will be accessible from other computers at:
echo   http://SRV04750.soton.ac.uk:8501
echo.
echo ⚠️ WARNING: Only use on secure networks!
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

:: Change to the dashboard directory
cd /d "%~dp0"

echo.
echo Starting dashboard with network access...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please run SETUP_FIRST_TIME.bat first.
    echo.
    pause
    exit /b 1
)

:: Wait a moment before starting
timeout /t 2 /nobreak >nul

:: Start browser
echo Opening dashboard...
start "" "http://localhost:8501"

:: Start Streamlit with network access
echo.
echo Dashboard is now accessible from:
echo   - Local: http://localhost:8501
echo   - Network: http://SRV04750.soton.ac.uk:8501
echo.
echo Press Ctrl+C to stop the dashboard.
echo.
python -m streamlit run streamlit_dashboard_bnt113_real_data.py --server.port 8501 --server.address 0.0.0.0 --server.headless true

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start dashboard!
    echo.
    pause
)

