# 🚀 Nifty F&O AI Analyzer v2.0

Professional AI-Powered NSE Futures & Options Stock Screener with 100-point transparent Buy Score engine.

---

## Features

- **Real-time scanning** of all NSE F&O stocks via Yahoo Finance
- **100-point AI Buy Score** with fully transparent breakdown
- **18 screener types**: Top Buy, Swing, Weekly, Breakout, Momentum, EMA, Volume Shockers, Long Build-up, Short Covering, OI Analysis
- **TradingView-style Heatmap** with sector grouping
- **Formula & Education page** explaining all 18 indicators
- **Watchlist & Portfolio tracking**
- **CSV Export**
- **Dark/Light theme**

---

## Quick Start

### One-click start (Windows)
```bat
start.bat
```

### Manual start

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
## Terminate Backend
-----------------------
taskkill /IM python.exe /F

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| GET /api/future-stocks | All F&O stocks with full indicators |
| GET /api/heatmap | Heatmap data |
| GET /api/top-buy | Top buy stocks (score ≥ 76) |
| GET /api/swing-buy | Swing trade setups |
| GET /api/weekly-buy | Weekly trade setups |
| GET /api/breakout | Breakout stocks |
| GET /api/momentum | Momentum stocks |
| GET /api/long-build-up | Long build-up stocks |
| GET /api/short-covering | Short covering stocks |
| GET /api/volume-shockers | High-volume stocks |
| GET /api/ema-screener | EMA alignment screener |
| GET /api/oi-analysis | OI analysis |
| GET /api/stock/{symbol} | Single stock detail |
| GET /api/market-overview | Market condition |
| GET /api/formula | All indicator formulas |
| GET /api/watchlist | Watchlist CRUD |
| GET /api/notifications | Alerts and notifications |
| GET /api/export/csv | Export CSV |

---

## Buy Score Guide

| Score | Signal | Action |
|-------|--------|--------|
| 91–100 | STRONG BUY | Excellent setup |
| 76–90 | BUY | Strong buy |
| 61–75 | WATCH | Good candidate |
| 41–60 | HOLD | Wait for better setup |
| 0–40 | AVOID | Skip |

---

## Tech Stack

- **Backend**: Python FastAPI + Pandas + yfinance + pandas_ta
- **Frontend**: React 19 + TypeScript + MUI v6 + Redux Toolkit + React Query
- **Data**: Yahoo Finance (free, real-time)

---

## Disclaimer

This tool is for educational and research purposes only. Not financial advice.
Always do your own research before trading.
