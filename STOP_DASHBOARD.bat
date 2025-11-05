@echo off
echo ========================================
echo  Stopping BNT113 Dashboard
echo ========================================
echo.

:: Kill all Streamlit processes
taskkill /F /IM streamlit.exe >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq *streamlit*" >nul 2>&1

:: Kill Python processes running Streamlit
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%a" get CommandLine /format:list | findstr /I "streamlit" >nul 2>&1
    if not errorlevel 1 (
        taskkill /F /PID %%a >nul 2>&1
    )
)

echo Dashboard stopped successfully!
echo.
timeout /t 2 /nobreak >nul

