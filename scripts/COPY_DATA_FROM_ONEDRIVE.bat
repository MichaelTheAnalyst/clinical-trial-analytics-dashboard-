@echo off
echo ========================================
echo  Copy Data Files from OneDrive
echo ========================================
echo.
echo This script will help you copy Excel data files from OneDrive to the dashboard data folder.
echo.

:: Change to the dashboard directory
cd /d "%~dp0"

:: Define source and destination paths
set "ONEDRIVE_SOURCE=F:\projects\OneDrive_2025-10-21\bnt122 progress report dashboard\BNT113 real data"
set "DASHBOARD_DATA=%~dp0data"

echo Source folder:
echo %ONEDRIVE_SOURCE%
echo.
echo Destination folder:
echo %DASHBOARD_DATA%
echo.

:: Check if source folder exists
if not exist "%ONEDRIVE_SOURCE%" (
    echo ❌ ERROR: OneDrive source folder not found!
    echo.
    echo Please verify the OneDrive folder path:
    echo   %ONEDRIVE_SOURCE%
    echo.
    echo If your OneDrive is in a different location:
    echo   1. Open this file in a text editor
    echo   2. Update the ONEDRIVE_SOURCE path
    echo   3. Save and run again
    echo.
    pause
    exit /b 1
)

:: Check if destination folder exists
if not exist "%DASHBOARD_DATA%" (
    echo Creating data folder...
    mkdir "%DASHBOARD_DATA%"
)

echo Found OneDrive folder! ✓
echo.
echo Files available to copy:
echo.
dir /b "%ONEDRIVE_SOURCE%\*.xlsx" 2>nul
echo.

echo.
echo What would you like to copy?
echo.
echo   1 - Copy all Excel files
echo   2 - Copy only Master Tracker
echo   3 - Copy only Screening Logs
echo   4 - Select files manually
echo   5 - Cancel
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Copying all Excel files...
    copy "%ONEDRIVE_SOURCE%\*.xlsx" "%DASHBOARD_DATA%\" /Y
    if errorlevel 1 (
        echo ❌ Error copying files!
    ) else (
        echo ✓ All files copied successfully!
    )
    goto :done
)

if "%choice%"=="2" (
    echo.
    echo Copying Master Tracker...
    copy "%ONEDRIVE_SOURCE%\BNT113-01 Master Tracker*.xlsx" "%DASHBOARD_DATA%\" /Y
    if errorlevel 1 (
        echo ❌ Error copying file!
    ) else (
        echo ✓ Master Tracker copied successfully!
    )
    goto :done
)

if "%choice%"=="3" (
    echo.
    echo Copying Screening Logs...
    copy "%ONEDRIVE_SOURCE%\BNT113-01 Screening Logs*.xlsx" "%DASHBOARD_DATA%\" /Y
    if errorlevel 1 (
        echo ❌ Error copying file!
    ) else (
        echo ✓ Screening Logs copied successfully!
    )
    goto :done
)

if "%choice%"=="4" (
    echo.
    echo Opening OneDrive folder...
    echo Please manually copy the files you need to:
    echo %DASHBOARD_DATA%
    echo.
    start "" explorer "%ONEDRIVE_SOURCE%"
    start "" explorer "%DASHBOARD_DATA%"
    goto :done
)

if "%choice%"=="5" (
    echo.
    echo Cancelled.
    goto :done
)

echo.
echo Invalid choice!
pause
exit /b 1

:done
echo.
echo ========================================
echo.
echo Data files location:
echo %DASHBOARD_DATA%
echo.
dir /b "%DASHBOARD_DATA%\*.xlsx" 2>nul
echo.
echo ========================================
echo.
echo Next step: Double-click START_DASHBOARD.bat to launch the dashboard
echo.
pause

