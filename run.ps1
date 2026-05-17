# Activate virtual environment and run the Flask application
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment script not found!" -ForegroundColor Red
    Exit 1
}

Write-Host "Starting Flask development server..." -ForegroundColor Green
python app.py
