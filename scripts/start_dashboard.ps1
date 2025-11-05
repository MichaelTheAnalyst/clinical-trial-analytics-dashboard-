# BNT113 Dashboard - PowerShell Launcher
# For advanced users who prefer PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " BNT113 Trial Dashboard - VM Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

Write-Host "Dashboard Location: $PWD" -ForegroundColor Yellow
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check Streamlit installation
Write-Host "Checking Streamlit installation..." -ForegroundColor Green
try {
    python -c "import streamlit" 2>$null
    Write-Host "✓ Streamlit is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Streamlit not found. Installing dependencies..." -ForegroundColor Yellow
    Write-Host ""
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install dependencies!" -ForegroundColor Red
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting dashboard..." -ForegroundColor Green
Write-Host "Dashboard URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the dashboard" -ForegroundColor Yellow
Write-Host ""

# Wait a moment
Start-Sleep -Seconds 2

# Open browser
Start-Process "http://localhost:8501"

# Start Streamlit
python -m streamlit run streamlit_dashboard_bnt113_real_data.py --server.port 8501 --server.address localhost --server.headless true

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host " ERROR: Failed to start dashboard!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "  1. Check if port 8501 is already in use" -ForegroundColor Yellow
    Write-Host "  2. Verify Python and dependencies are installed" -ForegroundColor Yellow
    Write-Host "  3. Check the data files are accessible" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
}

