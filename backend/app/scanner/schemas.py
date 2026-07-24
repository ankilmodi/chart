"""
Pydantic schemas for the Nifty Future Analyzer scanner module.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


# ── Stock Info (universe entry) ───────────────────────────────────────────

class StockInfo(BaseModel):
    symbol: str
    name: str
    sector: str
    index: str = "NIFTY50"
    ticker: str
    industry: Optional[str] = None


# ── Criteria Pass/Fail ────────────────────────────────────────────────────

class CriteriaStatus(BaseModel):
    """Each criterion tracked individually for transparent display."""
    buy_score_85:            bool = False
    confidence_85:           bool = False
    bullish_days_3:          bool = False
    volume_growth_5d:        bool = False
    ema_stack:               bool = False
    price_above_vwap:        bool = False
    macd_bullish:            bool = False
    rsi_ideal:               bool = False
    adx_25:                  bool = False
    long_buildup:            bool = False
    oi_increasing:           bool = False
    delivery_50:             bool = False
    breakout_confirmed:      bool = False
    rs_positive:             bool = False
    sector_strong:           bool = False
    supertrend_buy:          bool = False
    no_bearish_pattern:      bool = False
    market_bullish:          bool = False
    banknifty_bullish:       bool = False


# ── Score Breakdown ───────────────────────────────────────────────────────

class ScoreBreakdown(BaseModel):
    # Trend (max 35)
    ema_trend:      float = 0.0
    golden_cross:   float = 0.0
    price_vs_ema:   float = 0.0

    # Momentum (max 26)
    rsi:   float = 0.0
    macd:  float = 0.0
    adx:   float = 0.0

    # Volume (max 23)
    volume:   float = 0.0
    delivery: float = 0.0

    # Price Action (max 29)
    price_action:  float = 0.0
    breakout:      float = 0.0
    candle_pattern: float = 0.0

    # Open Interest (max 21)
    open_interest: float = 0.0

    # Trend Confirmation (max 18)
    supertrend: float = 0.0
    vwap:       float = 0.0

    # Relative Strength (max 18)
    relative_strength: float = 0.0
    sector_strength:   float = 0.0

    # Market Confirmation (max 16)
    market_trend: float = 0.0

    # Advanced criteria (additive)
    multi_day_strength:    float = 0.0
    continuous_vol_growth: float = 0.0
    above_avg_volume:      float = 0.0
    smart_money:           float = 0.0
    price_above_levels:    float = 0.0
    candle_quality:        float = 0.0
    breakout_confirmation: float = 0.0
    oi_pattern:            float = 0.0
    trend_quality:         float = 0.0

    # Risk Deductions
    risk: float = 0.0

    total: float = 0.0

    class Config:
        json_encoders = {float: lambda v: round(v, 2)}


# ── Single stock scan result ──────────────────────────────────────────────

class ScanResult(BaseModel):
    symbol: str
    name:   str
    sector: str
    industry:   Optional[str] = None
    index:      str           = "NIFTY50"
    market_cap: Optional[float] = None

    # Price data
    current_price:      float
    future_price:       Optional[float] = None
    premium_discount:   Optional[float] = None
    open:               Optional[float] = None
    high:               Optional[float] = None
    low:                Optional[float] = None
    close:              Optional[float] = None
    prev_close:         Optional[float] = None
    change:             Optional[float] = None
    change_pct:         Optional[float] = None
    future_change_pct:  Optional[float] = None

    # Volume
    volume:         Optional[int]   = None
    avg_volume_20d: Optional[int]   = None
    volume_ratio:   Optional[float] = None
    delivery_pct:   Optional[float] = None
    volume_trend:   Optional[str]   = None   # Increasing / Flat / Decreasing
    vol_vs_5d:      Optional[float] = None
    vol_vs_10d:     Optional[float] = None
    vol_vs_20d:     Optional[float] = None
    vol_vs_50d:     Optional[float] = None
    is_highest_volume_20d: Optional[bool] = None
    continuous_volume_growth: Optional[int] = None

    # Open Interest
    oi:             Optional[float] = None
    oi_change:      Optional[float] = None
    oi_change_pct:  Optional[float] = None
    pcr:            Optional[float] = None

    # Technical Indicators
    vwap:             Optional[float] = None
    ema9:             Optional[float] = None
    ema20:            Optional[float] = None
    ema50:            Optional[float] = None
    ema100:           Optional[float] = None
    ema200:           Optional[float] = None
    ema20_slope:      Optional[float] = None
    ema50_slope:      Optional[float] = None
    ema200_slope:     Optional[float] = None
    rsi:              Optional[float] = None
    macd:             Optional[float] = None
    macd_signal_line: Optional[float] = None
    macd_histogram:   Optional[float] = None
    adx:              Optional[float] = None
    atr:              Optional[float] = None
    supertrend:       Optional[float] = None
    supertrend_signal: Optional[str]  = None
    bb_upper:         Optional[float] = None
    bb_middle:        Optional[float] = None
    bb_lower:         Optional[float] = None
    relative_strength: Optional[float] = None

    # 52-week data
    week52_high:     Optional[float] = None
    week52_low:      Optional[float] = None
    week52_high_pct: Optional[float] = None
    week52_low_pct:  Optional[float] = None

    # Weekly indicators
    weekly_rsi:       Optional[float] = None
    weekly_macd:      Optional[float] = None
    weekly_macd_hist: Optional[float] = None
    weekly_ema9:      Optional[float] = None
    weekly_ema20:     Optional[float] = None
    weekly_breakout:  Optional[bool]  = None
    weekly_vol_ratio: Optional[float] = None

    # Smart money
    smart_money: Optional[str] = None   # Strong / Moderate / Weak

    # Classification
    trend:            Optional[str] = None
    trend_quality:    Optional[str] = None   # Excellent / Strong / Moderate / Weak
    momentum:         Optional[str] = None
    breakout_type:    Optional[str] = None
    breakout_valid:   Optional[bool] = None
    fake_breakout:    Optional[bool] = None
    consecutive_green: Optional[int] = None
    multi_day_strength: Optional[int] = None
    star_rating:       Optional[int] = None
    bullish_days_label: Optional[str] = None  # 🔥 3-Day Bullish etc.

    # Candle patterns
    bullish_patterns:      Optional[List[str]] = None
    three_white_soldiers:  Optional[bool] = None
    morning_star:          Optional[bool] = None
    marubozu:              Optional[bool] = None
    hammer:                Optional[bool] = None
    bullish_engulfing:     Optional[bool] = None

    # Support / Resistance / Key levels
    support:    Optional[float] = None
    resistance: Optional[float] = None
    prev_day_high: Optional[float] = None
    levels_above_count: Optional[int] = None

    # OI patterns
    long_buildup:   Optional[bool] = None
    short_covering: Optional[bool] = None
    short_buildup:  Optional[bool] = None
    long_unwinding: Optional[bool] = None

    # Trade levels (3 targets)
    entry_price:         Optional[float] = None
    target1:             Optional[float] = None
    target2:             Optional[float] = None
    target3:             Optional[float] = None
    target_price:        Optional[float] = None   # alias for target1
    stop_loss:           Optional[float] = None
    risk_reward_ratio:   Optional[float] = None
    expected_return_pct: Optional[float] = None
    success_probability: Optional[float] = None
    holding_period:      Optional[str]   = None   # Intraday / Swing / Positional
    risk_level:          Optional[str]   = None   # Low / Medium / High

    # Scores
    buy_score:        float = 0.0
    confidence_score: float = 0.0
    swing_score:      float = 0.0
    weekly_score:     float = 0.0
    trend_score:      float = 0.0
    signal:           Optional[str] = None
    star_signal:      Optional[str] = None   # ⭐⭐⭐⭐⭐ STRONG BUY etc.
    recommendation:   Optional[str] = None

    # Criteria checklist
    criteria: Optional[CriteriaStatus] = None
    score_breakdown: Optional[ScoreBreakdown] = None
    reasons:        List[str] = []
    reject_reasons: List[str] = []
    macd_signal:    Optional[str] = None
    scanned_at:     Optional[str] = None
    confidence_score: float = 0.0


# ── Market overview ───────────────────────────────────────────────────────

class MarketOverview(BaseModel):
    nifty_price:        Optional[float] = None
    nifty_change_pct:   Optional[float] = None
    nifty_ema20:        Optional[float] = None
    nifty_ema50:        Optional[float] = None
    nifty_ema200:       Optional[float] = None
    nifty_above_ema20:  bool = False
    nifty_above_ema50:  bool = False
    nifty_above_ema200: bool = False
    nifty_vwap:         Optional[float] = None
    nifty_above_vwap:   bool = False
    banknifty_price:    Optional[float] = None
    banknifty_change_pct: Optional[float] = None
    banknifty_bullish:  bool = False
    vix:                Optional[float] = None
    vix_safe:           bool = True
    market_trend:       str  = "sideways"
    advance_decline:    Optional[float] = None
    data_source:        str  = "live"   # "live" | "last_known" | "unavailable"
    timestamp:          str  = ""


# ── Scan response ─────────────────────────────────────────────────────────

class ScanResponse(BaseModel):
    scan_date:            str
    market_status:        str
    nifty_price:          Optional[float] = None
    vix_level:            Optional[float] = None
    market_trend:         str  = "sideways"
    buy_window:           str  = ""
    sell_window:          str  = ""
    total_scanned:        int  = 0
    qualified:            int  = 0
    results:              List[ScanResult] = []
    scan_duration_seconds: float = 0.0
    timestamp:            str  = ""


# ── Heatmap ───────────────────────────────────────────────────────────────

class HeatmapItem(BaseModel):
    symbol:       str
    name:         str
    sector:       str
    price:        float
    change_pct:   float
    buy_score:    float
    signal:       str
    volume:       Optional[int]   = None
    oi_change_pct: Optional[float] = None
    market_cap:   Optional[float] = None
    trend:        Optional[str]   = None
    color:        str = "yellow"


class HeatmapResponse(BaseModel):
    items:     List[HeatmapItem] = []
    total:     int  = 0
    timestamp: str  = ""


# ── Watchlist ─────────────────────────────────────────────────────────────

class WatchlistItem(BaseModel):
    symbol:    str
    name:      str
    sector:    str
    added_at:  str
    notes:     Optional[str]   = None
    target:    Optional[float] = None
    stop_loss: Optional[float] = None


class WatchlistResponse(BaseModel):
    items: List[WatchlistItem] = []
    total: int = 0


# ── Formula ───────────────────────────────────────────────────────────────

class FormulaEntry(BaseModel):
    name:              str
    category:          str
    formula:           str
    calculation:       str
    interpretation:    str
    bullish_condition: str
    bearish_condition: str
    example:           str
    parameters:        Optional[Dict[str, Any]] = None


class FormulaResponse(BaseModel):
    formulas: List[FormulaEntry] = []
    total:    int = 0


# ── Notification ──────────────────────────────────────────────────────────

class Notification(BaseModel):
    id:        str
    type:      str
    symbol:    str
    message:   str
    score:     Optional[float] = None
    timestamp: str
    read:      bool = False


class NotificationResponse(BaseModel):
    notifications: List[Notification] = []
    unread_count:  int = 0
    total:         int = 0
