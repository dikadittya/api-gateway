# KrakenD Configuration Builder for PowerShell
# Merge multiple endpoint files into single krakend.json

Write-Host "Building KrakenD configuration..." -ForegroundColor Cyan

# Check if Python is available
if (Get-Command python -ErrorAction SilentlyContinue) {
    python build-config.py
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    python3 build-config.py
} else {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3 to use this script" -ForegroundColor Yellow
    exit 1
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✨ Configuration built successfully!" -ForegroundColor Green
    Write-Host "You can now restart the API Gateway:" -ForegroundColor Yellow
    Write-Host "   cd .." -ForegroundColor Gray
    Write-Host "   docker-compose restart" -ForegroundColor Gray
} else {
    Write-Host "`n❌ Configuration build failed!" -ForegroundColor Red
    exit 1
}
