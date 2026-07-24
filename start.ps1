#!/usr/bin/env pwsh
# Nifty Future Analyzer + Weekly Scanner – PowerShell start script
# Single backend (port 8000) + Single frontend (port 5173)

$ROOT = $PSScriptRoot

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "  Nifty Analyzer + Weekly Scanner" -ForegroundColor Cyan
Write-Host "  Unified Quick Start" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# ── Backend ──────────────────────────────────────────
Write-Host "`n[1/3] Setting up Python backend..." -ForegroundColor Yellow
Set-Location "$ROOT\backend"

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
}

Write-Host "Installing requirements..." -ForegroundColor Gray
& ".\venv\Scripts\pip.exe" install -r requirements.txt --quiet

Write-Host "Starting unified backend on http://localhost:8000..." -ForegroundColor Green
Start-Process "pwsh" -ArgumentList "-NoExit", "-Command", "Set-Location '$ROOT\backend'; .\venv\Scripts\activate; python -m uvicorn app.main:app --reload --port 8000"

Start-Sleep -Seconds 4

# ── Frontend ─────────────────────────────────────────
Write-Host "`n[2/3] Setting up React frontend..." -ForegroundColor Yellow
Set-Location "$ROOT\frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing npm packages (this may take a minute)..." -ForegroundColor Gray
    npm install
}

Write-Host "Starting unified frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process "pwsh" -ArgumentList "-NoExit", "-Command", "Set-Location '$ROOT\frontend'; npm run dev"

Write-Host "`n===========================================" -ForegroundColor Cyan
Write-Host "  All services started!" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "  NIFTY FUTURE ANALYZER" -ForegroundColor White
Write-Host "  Frontend:       http://localhost:5173" -ForegroundColor White
Write-Host "  Backend API:    http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "  WEEKLY SCANNER  (sub-module, same app)" -ForegroundColor Yellow
Write-Host "  Scanner UI:     http://localhost:5173/scanner" -ForegroundColor White
Write-Host "  Backtest UI:    http://localhost:5173/backtest" -ForegroundColor White
Write-Host "  Universe UI:    http://localhost:5173/universe" -ForegroundColor White
Write-Host "  Scanner API:    http://localhost:8000/api/scanner/scan" -ForegroundColor White
Write-Host "===========================================" -ForegroundColor Cyan

Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"
