"""
Main Scanner Engine – scans all NSE F&O stocks and returns results
for every screener type: top-buy, swing, weekly, breakout, momentum,
long-buildup, short-covering, volume-shockers, EMA screener, OI analysis.
"""
import logging
import time
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple

import pandas as pd
import numpy as np
import pytz

from app.scanner.config import scanner_settings
from app.scanner.schemas import (
    ScanResult, ScanResponse, ScoreBreakdown, MarketOverview,
    HeatmapItem, HeatmapResponse,
)
from app.scanner.universe import get_full_universe, get_by_index, StockInfo
from app.scanner.market_data import (
    fetch_daily, fetch_nifty_daily, fetch_banknifty_daily, fetch_vix,
    fetch_snapshot, batch_fetch_daily, clear_scanner_cache, estimate_oi_pattern,
)
from app.scanner.indicators import compute_all, compute_relative_strength
from app.scanner.scoring import score_stock, compute_levels, get_signal, get_recommendation

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

# ── Cache ─────────────────────────────────────────────────────────────────
_scan_cache: Optional[List[ScanResult]] = None
_scan_cache_time: float = 0
_scan_running: bool = False   # prevents duplicate concurrent scans
SCAN_TTL = 300   # 5 min


def _now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _ist_now() -> datetime:
    return datetime.now(IST)


def is_market_open() -> bool:
    now = _ist_now()
    if now.weekday() >= 5:
        return False
    t = now.hour * 60 + now.minute
    return (9 * 60 + 15) <= t <= (15 * 60 + 30)


# ── Market overview ────────────────────────────────────────────────────────

def get_market_overview() -> MarketOverview:
    nifty_df     = fetch_nifty_daily()
    banknifty_df = fetch_banknifty_daily()
    vix          = fetch_vix()
    snap         = fetch_snapshot("^NSEI")
    bn_snap      = fetch_snapshot("^NSEBANK")

    price    = snap["price"]    if snap else None
    chg_pct  = snap["change_pct"] if snap else None
    bn_price = bn_snap["price"]   if bn_snap else None
    bn_chg   = bn_snap["change_pct"] if bn_snap else None

    # Determine data freshness
    from app.scanner.market_data import _last_known
    if price is not None:
        data_source = "live"
    elif "^NSEI" in _last_known:
        data_source = "last_known"
    else:
        data_source = "unavailable"

    ema20 = ema50 = ema200 = vwap_val = None
    above_ema20 = above_ema50 = above_ema200 = above_vwap = False

    if nifty_df is not None and len(nifty_df) >= 50:
        ind = compute_all(nifty_df)
        ema20  = ind.get("ema20");  ema50  = ind.get("ema50")
        ema200 = ind.get("ema200"); vwap_val = ind.get("vwap")
        if price:
            above_ema20  = bool(ema20  and price > ema20)
            above_ema50  = bool(ema50  and price > ema50)
            above_ema200 = bool(ema200 and price > ema200)
            above_vwap   = bool(vwap_val and price > vwap_val)

    vix_safe = vix is None or vix < (scanner_settings.VIX_THRESHOLD if hasattr(scanner_settings, 'VIX_THRESHOLD') else 18)
    market_bullish = above_ema200 and above_vwap and vix_safe

    if market_bullish and above_ema50:
        trend = "bullish"
    elif not above_ema200 or (vix and vix > 25):
        trend = "bearish"
    else:
        trend = "sideways"

    return MarketOverview(
        nifty_price=price,
        nifty_change_pct=chg_pct,
        nifty_ema20=ema20,
        nifty_ema50=ema50,
        nifty_ema200=ema200,
        nifty_above_ema20=above_ema20,
        nifty_above_ema50=above_ema50,
        nifty_above_ema200=above_ema200,
        nifty_vwap=vwap_val,
        nifty_above_vwap=above_vwap,
        banknifty_price=bn_price,
        banknifty_change_pct=bn_chg,
        vix=vix,
        vix_safe=vix_safe,
        market_trend=trend,
        data_source=data_source,
        timestamp=_now_str(),
    )


# ── Sector rankings ────────────────────────────────────────────────────────

def _compute_sector_ranks(
    stocks: List[StockInfo],
    data_map: Dict[str, pd.DataFrame],
) -> Dict[str, float]:
    sector_returns: Dict[str, List[float]] = {}
    for stock in stocks:
        df = data_map.get(stock.ticker)
        if df is None or len(df) < 6:
            continue
        c  = df["close"]
        r5 = float(((c.iloc[-1] - c.iloc[-6]) / c.iloc[-6]) * 100)
        sector_returns.setdefault(stock.sector, []).append(r5)

    sector_avg = {s: float(np.mean(v)) for s, v in sector_returns.items()}
    if not sector_avg:
        return {}
    vals = list(sector_avg.values())
    mn, mx = min(vals), max(vals)
    rng = mx - mn if mx != mn else 1
    return {s: round((v - mn) / rng, 3) for s, v in sector_avg.items()}


# ── Build ScanResult from indicators ──────────────────────────────────────

def _build_result(
    stock: StockInfo,
    df: pd.DataFrame,
    ind: Dict[str, Any],
    oi: Dict[str, Any],
    market_bullish: bool,
    sector_rank: float,
    nifty_5d: float,
    stock_5d: float,
) -> Optional[ScanResult]:
    price = ind.get("price")
    if not price:
        return None

    bd, reasons, rejects, qualified = score_stock(
        ind=ind,
        price=price,
        market_bullish=market_bullish,
        sector_rank=sector_rank,
        nifty_return_5d=nifty_5d,
        stock_return_5d=stock_5d,
        oi_data=oi,
    )

    levels = compute_levels(price=price, atr=ind.get("atr"), ind=ind)
    signal = get_signal(bd.total)
    rec    = get_recommendation(bd.total)

    # Merge OI data into ind
    ind.update(oi)

    # Consecutive green → star rating
    green = ind.get("consecutive_green") or 0
    stars = min(5, green) if green >= 2 else 0

    return ScanResult(
        symbol=stock.symbol,
        name=stock.name,
        sector=stock.sector,
        industry=getattr(stock, "industry", None),
        index=getattr(stock, "index", "NIFTY50"),
        market_cap=getattr(stock, "market_cap", None),

        current_price=price,
        future_price=round(price * 1.001, 2),     # approx future premium
        premium_discount=round(price * 0.001, 2),
        open=ind.get("open"),
        high=ind.get("high"),
        low=ind.get("low"),
        close=ind.get("close"),
        prev_close=ind.get("prev_close"),
        change=ind.get("change"),
        change_pct=ind.get("change_pct"),

        volume=ind.get("volume"),
        avg_volume_20d=int(ind.get("avg_volume_20d") or 0) or None,
        volume_ratio=ind.get("vol_ratio"),
        delivery_pct=ind.get("delivery_pct"),

        oi=oi.get("oi"),
        oi_change_pct=oi.get("oi_change_pct"),
        pcr=oi.get("pcr"),

        vwap=ind.get("vwap"),
        ema20=ind.get("ema20"),
        ema50=ind.get("ema50"),
        ema100=ind.get("ema100"),
        ema200=ind.get("ema200"),
        ema9=ind.get("ema9"),
        rsi=ind.get("rsi"),
        macd=ind.get("macd"),
        macd_signal_line=ind.get("macd_signal_line"),
        macd_histogram=ind.get("macd_hist"),
        adx=ind.get("adx"),
        atr=ind.get("atr"),
        supertrend=ind.get("supertrend"),
        supertrend_signal=ind.get("supertrend_dir"),
        bb_upper=ind.get("bb_upper"),
        bb_middle=ind.get("bb_middle"),
        bb_lower=ind.get("bb_lower"),

        week52_high=ind.get("week52_high"),
        week52_low=ind.get("week52_low"),
        week52_high_pct=ind.get("week52_high_pct"),
        week52_low_pct=ind.get("week52_low_pct"),

        trend=ind.get("trend"),
        momentum=ind.get("momentum"),
        breakout_type=_detect_breakout_type(ind),
        consecutive_green=green,
        star_rating=stars,

        support=ind.get("support"),
        resistance=ind.get("resistance"),

        long_buildup=oi.get("long_buildup"),
        short_covering=oi.get("short_covering"),
        short_buildup=oi.get("short_buildup"),
        long_unwinding=oi.get("long_unwinding"),

        entry_price=levels["entry_price"],
        target_price=levels["target_price"],
        stop_loss=levels["stop_loss"],
        risk_reward_ratio=levels["risk_reward_ratio"],
        expected_return_pct=levels["expected_return_pct"],
        success_probability=levels["success_probability"],

        confidence_score=bd.total,
        buy_score=bd.total,
        signal=signal,
        recommendation=rec,
        score_breakdown=bd,
        reasons=reasons,
        reject_reasons=rejects,
        macd_signal=ind.get("macd_cross"),
        scanned_at=_now_str(),
    )


def _detect_breakout_type(ind: Dict[str, Any]) -> Optional[str]:
    if ind.get("week52_high_pct") is not None and ind["week52_high_pct"] >= -1:
        return "52 Week Breakout"
    if ind.get("breakout_20d"):
        return "20 Day Breakout"
    if ind.get("breakout_50d"):
        return "50 Day Breakout"
    if ind.get("breakout_100d"):
        return "100 Day Breakout"
    if ind.get("breakout_200d"):
        return "200 Day Breakout"
    return None


# ── Main full scan ─────────────────────────────────────────────────────────

def run_full_scan(force: bool = False) -> List[ScanResult]:
    """Run full scan of all F&O stocks. Cached for 5 minutes."""
    global _scan_cache, _scan_cache_time, _scan_running

    # Return cached results if still fresh
    if not force and _scan_cache and (time.time() - _scan_cache_time) < SCAN_TTL:
        return _scan_cache

    # If another scan is already running, return stale cache or empty list
    if _scan_running:
        logger.info("Scan already in progress – returning cached results")
        return _scan_cache or []

    _scan_running = True
    t0 = time.time()
    logger.info("Starting full F&O scan…")

    try:
        market    = get_market_overview()
        bullish   = market.market_trend == "bullish"
        universe  = get_full_universe()
        tickers   = [s.ticker for s in universe]

        nifty_df  = fetch_nifty_daily()
        nifty_5d  = _calc_5d_return(nifty_df)

        data_map  = batch_fetch_daily(tickers, period="200d")
        sec_ranks = _compute_sector_ranks(universe, data_map)

        results: List[ScanResult] = []
        for stock in universe:
            df = data_map.get(stock.ticker)
            if df is None or len(df) < 50:
                continue
            try:
                ind      = compute_all(df)
                oi       = estimate_oi_pattern(df, stock.ticker)
                stock_5d = _calc_5d_return(df)
                sr       = sec_ranks.get(stock.sector, 0.5)
                result   = _build_result(stock, df, ind, oi, bullish, sr, nifty_5d, stock_5d)
                if result:
                    results.append(result)
            except Exception as e:
                logger.debug("Scan error %s: %s", stock.symbol, e)

        results.sort(key=lambda r: r.buy_score, reverse=True)
        _scan_cache      = results
        _scan_cache_time = time.time()
        logger.info("Scan done: %d stocks | %.1fs", len(results), time.time() - t0)
        return results

    except Exception as e:
        logger.error("run_full_scan failed: %s", e)
        return _scan_cache or []

    finally:
        _scan_running = False


def _calc_5d_return(df: Optional[pd.DataFrame]) -> float:
    if df is None or len(df) < 6:
        return 0.0
    c = df["close"]
    return float(((c.iloc[-1] - c.iloc[-6]) / c.iloc[-6]) * 100)


# ── Screener filters ───────────────────────────────────────────────────────

def get_top_buy(results: List[ScanResult], limit: int = 20) -> List[ScanResult]:
    return [r for r in results if r.buy_score >= 76][:limit]


def get_swing_buy(results: List[ScanResult], limit: int = 20) -> List[ScanResult]:
    return [r for r in results
            if r.buy_score >= 65
            and r.trend in ("Uptrend", "Strong Uptrend")
            and (r.rsi or 0) > 50
            and (r.volume_ratio or 0) > 1.2][:limit]


def get_weekly_buy(results: List[ScanResult], limit: int = 20) -> List[ScanResult]:
    return [r for r in results
            if r.buy_score >= 70
            and r.supertrend_signal == "buy"
            and (r.adx or 0) > 20][:limit]


def get_breakout_stocks(results: List[ScanResult], limit: int = 20) -> List[ScanResult]:
    return [r for r in results
            if r.breakout_type is not None
            and (r.volume_ratio or 0) > 1.5][:limit]


def get_momentum_stocks(results: List[ScanResult], limit: int = 20) -> List[ScanResult]:
    return [r for r in results
            if r.momentum in ("Strong", "Increasing")
            and (r.rsi or 0) > 55
            and (r.adx or 0) > 20][:limit]


def get_long_buildup(results: List[ScanResult], limit: int = 20) -> List[ScanResult]:
    return [r for r in results if r.long_buildup][:limit]


def get_short_covering(results: List[ScanResult], limit: int = 20) -> List[ScanResult]:
    return [r for r in results if r.short_covering][:limit]


def get_volume_shockers(results: List[ScanResult], limit: int = 20) -> List[ScanResult]:
    return sorted(
        [r for r in results if (r.volume_ratio or 0) >= 2.0],
        key=lambda r: r.volume_ratio or 0,
        reverse=True,
    )[:limit]


def get_ema_screener(results: List[ScanResult], limit: int = 30) -> List[ScanResult]:
    """Stocks in ideal EMA alignment."""
    return [r for r in results
            if r.ema20 and r.ema50 and r.ema200
            and (r.current_price or 0) > r.ema20 > r.ema50 > r.ema200][:limit]


def get_oi_analysis(results: List[ScanResult], limit: int = 30) -> List[ScanResult]:
    return sorted(
        [r for r in results if r.oi_change_pct is not None],
        key=lambda r: abs(r.oi_change_pct or 0),
        reverse=True,
    )[:limit]


# ── Heatmap ───────────────────────────────────────────────────────────────

def build_heatmap(results: List[ScanResult]) -> HeatmapResponse:
    items: List[HeatmapItem] = []
    for r in results:
        score = r.buy_score
        if score >= 76:
            color = "dark_green"
        elif score >= 61:
            color = "green"
        elif score >= 41:
            color = "yellow"
        elif score >= 21:
            color = "orange"
        else:
            color = "red"

        items.append(HeatmapItem(
            symbol=r.symbol,
            name=r.name,
            sector=r.sector,
            price=r.current_price,
            change_pct=r.change_pct or 0.0,
            buy_score=r.buy_score,
            signal=r.signal or "WATCH",
            volume=r.volume,
            oi_change_pct=r.oi_change_pct,
            market_cap=r.market_cap,
            trend=r.trend,
            color=color,
        ))
    return HeatmapResponse(items=items, total=len(items), timestamp=_now_str())


# ── Wrap full scan as ScanResponse ────────────────────────────────────────

def run_scan(
    index_filter: str = "ALL",
    min_score: float = 60.0,
    force: bool = False,
) -> ScanResponse:
    market  = get_market_overview()
    results = run_full_scan(force=force)
    filtered = [r for r in results if r.buy_score >= min_score]

    now_ist = _ist_now()
    monday  = now_ist - pd.Timedelta(days=now_ist.weekday())
    friday  = now_ist + pd.Timedelta(days=(4 - now_ist.weekday()) % 7)

    return ScanResponse(
        scan_date=now_ist.strftime("%Y-%m-%d"),
        market_status=market.market_trend,
        nifty_price=market.nifty_price,
        vix_level=market.vix,
        market_trend=market.market_trend,
        buy_window=f"{monday.strftime('%d %b %Y')} 09:30 – 11:00 IST",
        sell_window=f"{friday.strftime('%d %b %Y')} 14:30 – 15:20 IST",
        total_scanned=len(results),
        qualified=len(filtered),
        results=filtered,
        scan_duration_seconds=0.0,
        timestamp=_now_str(),
    )
