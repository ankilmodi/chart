"""
All new API endpoints for the Nifty Future Analyzer.
GET /future-stocks, /heatmap, /top-buy, /weekly-buy, /swing-buy,
    /breakout, /momentum, /long-build-up, /short-covering,
    /volume-shockers, /ema-screener, /oi-analysis,
    /watchlist, /formula, /notifications, /stock/{symbol}
"""
import json
import logging
import os
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query, Body
from fastapi.responses import StreamingResponse
import io

from app.scanner.scanner import (
    run_full_scan, get_market_overview, build_heatmap,
    get_top_buy, get_swing_buy, get_weekly_buy,
    get_breakout_stocks, get_momentum_stocks,
    get_long_buildup, get_short_covering,
    get_volume_shockers, get_ema_screener, get_oi_analysis,
)
from app.scanner.schemas import (
    ScanResult, HeatmapResponse, WatchlistItem, WatchlistResponse,
    FormulaEntry, FormulaResponse, Notification, NotificationResponse,
)
from app.scanner.market_data import clear_scanner_cache

logger = logging.getLogger(__name__)
router = APIRouter()

WATCHLIST_FILE = os.path.join(os.path.dirname(__file__), "watchlist_store.json")
NOTIF_FILE     = os.path.join(os.path.dirname(__file__), "notifications_store.json")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


# ── Helpers ────────────────────────────────────────────────────────────────

def _load_json(path: str) -> list:
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save_json(path: str, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ── GET /future-stocks ─────────────────────────────────────────────────────

@router.get("/future-stocks", tags=["screener"])
async def get_future_stocks(
    force:     bool  = Query(False),
    min_score: float = Query(0),
    sector:    Optional[str] = Query(None),
    signal:    Optional[str] = Query(None),
    trend:     Optional[str] = Query(None),
    limit:     int   = Query(200),
):
    """Full Nifty F&O stock table with all indicators and buy scores."""
    results = run_full_scan(force=force)
    if min_score > 0:
        results = [r for r in results if r.buy_score >= min_score]
    if sector:
        results = [r for r in results if r.sector.lower() == sector.lower()]
    if signal:
        results = [r for r in results if (r.signal or "").upper() == signal.upper()]
    if trend:
        results = [r for r in results if (r.trend or "").lower() == trend.lower()]
    return {
        "stocks": [r.dict() for r in results[:limit]],
        "total":  len(results),
        "timestamp": _now(),
    }


# ── GET /heatmap ───────────────────────────────────────────────────────────

@router.get("/heatmap", tags=["screener"])
async def get_heatmap(force: bool = Query(False)):
    """TradingView-style heatmap data by sector and buy score."""
    results  = run_full_scan(force=force)
    heatmap  = build_heatmap(results)
    return heatmap.dict()


# ── GET /top-buy ───────────────────────────────────────────────────────────

@router.get("/top-buy", tags=["screener"])
async def get_top_buy_endpoint(
    limit: int = Query(20),
    force: bool = Query(False),
):
    """Top Buy stocks today (score ≥ 76)."""
    results = run_full_scan(force=force)
    top     = get_top_buy(results, limit=limit)
    return {"stocks": [r.dict() for r in top], "total": len(top), "timestamp": _now()}


# ── GET /swing-buy ─────────────────────────────────────────────────────────

@router.get("/swing-buy", tags=["screener"])
async def get_swing_buy_endpoint(
    limit: int = Query(20),
    force: bool = Query(False),
):
    """Swing trading picks (2–5 day hold)."""
    results = run_full_scan(force=force)
    picks   = get_swing_buy(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /weekly-buy ────────────────────────────────────────────────────────

@router.get("/weekly-buy", tags=["screener"])
async def get_weekly_buy_endpoint(
    limit: int = Query(20),
    force: bool = Query(False),
):
    """Weekly trading picks (5–7 day hold)."""
    results = run_full_scan(force=force)
    picks   = get_weekly_buy(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /breakout ──────────────────────────────────────────────────────────

@router.get("/breakout", tags=["screener"])
async def get_breakout_endpoint(
    limit: int = Query(20),
    force: bool = Query(False),
):
    """Stocks breaking out of key levels."""
    results = run_full_scan(force=force)
    picks   = get_breakout_stocks(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /momentum ──────────────────────────────────────────────────────────

@router.get("/momentum", tags=["screener"])
async def get_momentum_endpoint(
    limit: int = Query(20),
    force: bool = Query(False),
):
    """High-momentum stocks."""
    results = run_full_scan(force=force)
    picks   = get_momentum_stocks(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /long-build-up ─────────────────────────────────────────────────────

@router.get("/long-build-up", tags=["screener"])
async def get_long_buildup_endpoint(
    limit: int = Query(20),
    force: bool = Query(False),
):
    """Long build-up stocks (Price ↑ + OI ↑)."""
    results = run_full_scan(force=force)
    picks   = get_long_buildup(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /short-covering ────────────────────────────────────────────────────

@router.get("/short-covering", tags=["screener"])
async def get_short_covering_endpoint(
    limit: int = Query(20),
    force: bool = Query(False),
):
    """Short covering stocks (Price ↑ + OI ↓)."""
    results = run_full_scan(force=force)
    picks   = get_short_covering(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /volume-shockers ───────────────────────────────────────────────────

@router.get("/volume-shockers", tags=["screener"])
async def get_volume_shockers_endpoint(
    limit: int = Query(20),
    force: bool = Query(False),
):
    """Stocks with 2x+ above average volume."""
    results = run_full_scan(force=force)
    picks   = get_volume_shockers(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /ema-screener ──────────────────────────────────────────────────────

@router.get("/ema-screener", tags=["screener"])
async def get_ema_screener_endpoint(
    limit: int = Query(30),
    force: bool = Query(False),
):
    """Stocks in perfect EMA bullish alignment."""
    results = run_full_scan(force=force)
    picks   = get_ema_screener(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /oi-analysis ───────────────────────────────────────────────────────

@router.get("/oi-analysis", tags=["screener"])
async def get_oi_analysis_endpoint(
    limit: int = Query(30),
    force: bool = Query(False),
):
    """Open Interest analysis for all F&O stocks."""
    results = run_full_scan(force=force)
    picks   = get_oi_analysis(results, limit=limit)
    return {"stocks": [r.dict() for r in picks], "total": len(picks), "timestamp": _now()}


# ── GET /stock/{symbol} ────────────────────────────────────────────────────

@router.get("/stock/{symbol}", tags=["stock"])
async def get_stock_detail(symbol: str):
    """Full detail for a single stock."""
    results = run_full_scan()
    match = next((r for r in results if r.symbol.upper() == symbol.upper()), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    return match.dict()


# ── GET /market-overview ───────────────────────────────────────────────────

@router.get("/market-overview", tags=["market"])
async def get_market():
    """Live Nifty / BankNifty / VIX market overview."""
    return get_market_overview().dict()


# ── GET /scanner ───────────────────────────────────────────────────────────

@router.get("/scanner", tags=["screener"])
async def run_scanner(
    min_score: float = Query(60),
    force:     bool  = Query(False),
):
    """Run full scanner, return results above min_score."""
    results  = run_full_scan(force=force)
    filtered = [r for r in results if r.buy_score >= min_score]
    return {
        "results":   [r.dict() for r in filtered],
        "total":     len(filtered),
        "scanned":   len(results),
        "timestamp": _now(),
    }


# ── GET /watchlist ─────────────────────────────────────────────────────────

@router.get("/watchlist", tags=["watchlist"])
async def get_watchlist():
    items_raw = _load_json(WATCHLIST_FILE)
    items = [WatchlistItem(**i) for i in items_raw]
    # Enrich with live prices
    if items:
        results = run_full_scan()
        price_map = {r.symbol: r for r in results}
        enriched = []
        for item in items:
            live = price_map.get(item.symbol)
            d = item.dict()
            if live:
                d["current_price"] = live.current_price
                d["change_pct"]    = live.change_pct
                d["buy_score"]     = live.buy_score
                d["signal"]        = live.signal
            enriched.append(d)
        return WatchlistResponse(items=enriched, total=len(enriched)).dict()
    return WatchlistResponse(items=items, total=len(items)).dict()


@router.post("/watchlist", tags=["watchlist"])
async def add_to_watchlist(item: WatchlistItem):
    items = _load_json(WATCHLIST_FILE)
    if any(i["symbol"] == item.symbol for i in items):
        raise HTTPException(status_code=400, detail=f"{item.symbol} already in watchlist")
    items.append(item.dict())
    _save_json(WATCHLIST_FILE, items)
    return {"message": f"{item.symbol} added to watchlist", "timestamp": _now()}


@router.delete("/watchlist/{symbol}", tags=["watchlist"])
async def remove_from_watchlist(symbol: str):
    items = _load_json(WATCHLIST_FILE)
    items = [i for i in items if i["symbol"] != symbol.upper()]
    _save_json(WATCHLIST_FILE, items)
    return {"message": f"{symbol} removed", "timestamp": _now()}


# ── GET /notifications ─────────────────────────────────────────────────────

@router.get("/notifications", tags=["notifications"])
async def get_notifications():
    raw   = _load_json(NOTIF_FILE)
    notifs = [Notification(**n) for n in raw]
    unread = sum(1 for n in notifs if not n.read)
    return NotificationResponse(
        notifications=notifs, unread_count=unread, total=len(notifs)
    ).dict()


@router.post("/notifications/read/{notif_id}", tags=["notifications"])
async def mark_notification_read(notif_id: str):
    raw = _load_json(NOTIF_FILE)
    for n in raw:
        if n["id"] == notif_id:
            n["read"] = True
    _save_json(NOTIF_FILE, raw)
    return {"message": "marked read"}


@router.post("/notifications/generate", tags=["notifications"])
async def generate_notifications():
    """Scan and generate alerts for strong buys, breakouts, volume spikes."""
    import uuid
    results = run_full_scan()
    raw     = _load_json(NOTIF_FILE)
    existing_symbols = {n["symbol"] for n in raw if not n.get("read", False)}
    new_notifs = []

    for r in results:
        if r.symbol in existing_symbols:
            continue
        if r.buy_score >= 91:
            new_notifs.append({
                "id": str(uuid.uuid4())[:8],
                "type": "strong_buy",
                "symbol": r.symbol,
                "message": f"🔥 {r.symbol} – Excellent Buy! Score: {r.buy_score:.0f}/100",
                "score": r.buy_score,
                "timestamp": _now(),
                "read": False,
            })
        elif r.breakout_type:
            new_notifs.append({
                "id": str(uuid.uuid4())[:8],
                "type": "breakout",
                "symbol": r.symbol,
                "message": f"📈 {r.symbol} – {r.breakout_type} detected",
                "score": r.buy_score,
                "timestamp": _now(),
                "read": False,
            })
        elif (r.volume_ratio or 0) >= 3.0:
            new_notifs.append({
                "id": str(uuid.uuid4())[:8],
                "type": "volume_spike",
                "symbol": r.symbol,
                "message": f"📊 {r.symbol} – Volume {r.volume_ratio:.1f}x avg",
                "score": r.buy_score,
                "timestamp": _now(),
                "read": False,
            })

    all_notifs = new_notifs + raw
    _save_json(NOTIF_FILE, all_notifs[:100])
    return {"generated": len(new_notifs), "timestamp": _now()}


# ── GET /export ────────────────────────────────────────────────────────────

@router.get("/export/csv", tags=["export"])
async def export_csv(min_score: float = Query(0)):
    results = run_full_scan()
    filtered = [r for r in results if r.buy_score >= min_score]
    import csv, io as _io
    output = _io.StringIO()
    if filtered:
        fields = [
            "symbol", "name", "sector", "current_price", "change_pct",
            "buy_score", "signal", "trend", "rsi", "macd", "adx",
            "ema20", "ema50", "ema200", "volume_ratio", "supertrend_signal",
            "breakout_type", "momentum", "long_buildup", "short_covering",
        ]
        writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for r in filtered:
            writer.writerow({f: getattr(r, f, None) for f in fields})
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=nifty_scan.csv"},
    )


# ── POST /cache/clear ──────────────────────────────────────────────────────

@router.post("/cache/clear", tags=["admin"])
async def clear_cache():
    clear_scanner_cache()
    return {"message": "Cache cleared", "timestamp": _now()}



# ── GET /formula ───────────────────────────────────────────────────────────

@router.get("/formula", tags=["education"])
async def get_formula():
    """All indicator formulas with explanations."""
    from app.scanner.formula_data import get_formula_response
    return get_formula_response().dict()
