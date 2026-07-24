@echo off
title Nifty F&O AI Analyzer

echo ================================================
echo  Nifty F&O AI Analyzer v2.0
echo  Starting Backend and Frontend...
echo ================================================

:: Start Backend
echo.
echo [1/2] Starting FastAPI Backend on port 8000...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: Wait a bit
timeout /t 3 /nobreak > nul

:: Start Frontend
echo [2/2] Starting React Frontend on port 5173...
start "Frontend - Vite" cmd /k "cd /d %~dp0frontend && npm install && npm run dev"

echo.
echo ================================================
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo  Frontend: http://localhost:5173
echo ================================================
echo.
pause
