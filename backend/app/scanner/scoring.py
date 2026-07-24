"""
AI Buy Score Engine – Full 100-point transparent scoring system.
Scores each Nifty F&O stock out of 100 across 8 dimensions.

Score bands:
  0–40   = Avoid
  41–60  = Watch
  61–75  = Good
  76–90  = Strong Buy
  91–100 = Excellent Buy
"""
from typing import Dict, Any, List, Optional, Tuple
from app.scanner.schemas import ScoreBreakdown


# ─── Signal labels ────────────────────────────────────────────────────────

def get_signal(score: float) -> str:
    if score >= 91: return "STRONG BUY"
    if score >= 76: return "BUY"
    if score >= 61: return "WATCH"
    if score >= 41: return "HOLD"
    if score >= 21: return "SELL"
    return "STRONG SELL"


def get_recommendation(score: float) -> str:
    if score >= 91: return "Excellent Buy"
    if score >= 76: return "Strong Buy"
    if score >= 61: return "Good"
    if score >= 41: return "Watch"
    return "Avoid"


# ─── Main scoring function ────────────────────────────────────────────────

def score_stock(
    ind: Dict[str, Any],
    price: float,
    market_bullish: bool,
    sector_rank: float = 0.5,       # 0–1
    nifty_return_5d: float = 0.0,
    stock_return_5d: float = 0.0,
    oi_data: Optional[Dict] = None,
) -> Tuple[ScoreBreakdown, List[str], List[str], bool]:
    """
    Returns (ScoreBreakdown, reasons, reject_reasons, is_qualified).
    Total possible raw points exceed 100; we cap at 100.
    """
    bd = ScoreBreakdown()
    reasons: List[str] = []
    rejects: List[str] = []

    def v(key): return ind.get(key)

    # ── 1. TREND  (max 35 pts) ──────────────────────────────────────────
    ema20  = v("ema20");  ema50  = v("ema50")
    ema100 = v("ema100"); ema200 = v("ema200")
    trend_pts = 0.0

    # EMA stack alignment
    if ema20 and ema50 and ema200 and ema20 > ema50 > ema200:
        trend_pts += 10
        reasons.append("EMA20 > EMA50 > EMA200 – perfect bullish stack")
    if price and ema20 and price > ema20:
        trend_pts += 5
        reasons.append(f"Price above EMA20 ({price:.0f} > {ema20:.0f})")
    elif price and ema20:
        rejects.append("Price below EMA20")
    if price and ema50 and price > ema50:
        trend_pts += 5
        reasons.append("Price above EMA50")
    if price and ema200 and price > ema200:
        trend_pts += 5
        reasons.append("Price above EMA200")

    # Golden / Death Cross
    if v("golden_cross"):
        trend_pts += 10
        reasons.append("Golden Cross (EMA50 crossed above EMA200)")
    if v("death_cross"):
        trend_pts -= 15
        rejects.append("Death Cross (EMA50 crossed below EMA200) – strong bearish")

    bd.ema_trend = max(0.0, min(35.0, round(trend_pts, 1)))

    # ── 2. MOMENTUM  (max 26 pts) ──────────────────────────────────────
    mom_pts = 0.0
    rsi = v("rsi")
    if rsi is not None:
        if 55 <= rsi <= 70:
            mom_pts += 8
            reasons.append(f"RSI in ideal zone ({rsi:.1f})")
        elif 70 < rsi <= 80:
            mom_pts += 5
            reasons.append(f"RSI strong momentum ({rsi:.1f})")
        elif rsi < 40:
            mom_pts -= 8
            rejects.append(f"RSI oversold/weak ({rsi:.1f} < 40)")
    bd.rsi = max(0.0, min(10.0, round(mom_pts if rsi is not None else 0, 1)))

    macd_pts = 0.0
    macd_cross = v("macd_cross"); macd_hist = v("macd_hist") or 0
    if macd_cross == "bullish":
        macd_pts += 8
        reasons.append(f"MACD bullish crossover (hist={macd_hist:.4f})")
    elif macd_cross == "bearish":
        rejects.append("MACD bearish crossover")
    if macd_hist > 0:
        macd_pts += 5
        if macd_cross != "bullish":
            reasons.append("MACD histogram positive")
    bd.macd = max(0.0, min(13.0, round(macd_pts, 1)))

    adx_pts = 0.0
    adx = v("adx"); adx_plus = v("adx_plus"); adx_minus = v("adx_minus")
    if adx is not None:
        if adx > 35 and adx_plus and adx_minus and adx_plus > adx_minus:
            adx_pts = 10
            reasons.append(f"Very strong trend ADX={adx:.1f}")
        elif adx > 25 and adx_plus and adx_minus and adx_plus > adx_minus:
            adx_pts = 8
            reasons.append(f"Strong trend ADX={adx:.1f}")
        elif adx > 20:
            adx_pts = 4
        else:
            rejects.append(f"Weak trend ADX={adx:.1f}")
    bd.adx = max(0.0, min(10.0, round(adx_pts, 1)))

    # ── 3. VOLUME  (max 23 pts) ─────────────────────────────────────────
    vol_pts = 0.0
    vol_ratio = v("vol_ratio")
    if vol_ratio is not None:
        if vol_ratio >= 2.0:
            vol_pts += 10
            reasons.append(f"Volume surge {vol_ratio:.1f}x 20-day avg")
        elif vol_ratio >= 1.5:
            vol_pts += 7
            reasons.append(f"High volume {vol_ratio:.1f}x avg")
        elif vol_ratio >= 1.2:
            vol_pts += 4
        elif vol_ratio < 0.7:
            rejects.append(f"Low volume {vol_ratio:.2f}x avg")
    if v("volume_increasing_3d"):
        vol_pts += 8
        reasons.append("Volume increasing 3 consecutive days")
    bd.volume = max(0.0, min(18.0, round(vol_pts, 1)))

    # Delivery
    del_pts = 0.0
    delivery_pct = v("delivery_pct") or 0
    if delivery_pct > 50:
        del_pts += 5
        reasons.append(f"Strong delivery {delivery_pct:.0f}%")
    if v("delivery_increasing"):
        del_pts += 5
    bd.delivery = max(0.0, min(10.0, round(del_pts, 1)))

    # ── 4. PRICE ACTION  (max 29 pts) ────────────────────────────────────
    pa_pts = 0.0
    green = v("consecutive_green") or 0
    if green >= 5:
        pa_pts += 10
        reasons.append(f"{green} consecutive green candles ({'★' * min(green, 5)})")
    elif green >= 3:
        pa_pts += 8
        reasons.append(f"{green} consecutive green candles")
    elif green >= 2:
        pa_pts += 4

    if v("higher_highs") and v("higher_lows"):
        pa_pts += 5
        reasons.append("Higher Highs + Higher Lows confirmed")
    elif v("higher_highs"):
        pa_pts += 3

    if v("bullish_engulfing"):
        pa_pts += 5
        reasons.append("Bullish Engulfing pattern")

    gap_pct = v("gap_up_pct") or 0
    if 0 < gap_pct <= 2:
        pa_pts += 3
        reasons.append(f"Gap up +{gap_pct:.1f}%")
    elif gap_pct > 5:
        rejects.append(f"Gap up too large ({gap_pct:.1f}%) – chasing risk")
        pa_pts -= 3

    bd.price_action = max(0.0, min(15.0, round(pa_pts, 1)))

    # Breakout
    brk_pts = 0.0
    if v("breakout_20d"):
        brk_pts += 10; reasons.append("20-day Breakout")
    if v("breakout_50d"):
        brk_pts += 5
    if v("breakout_200d"):
        brk_pts += 5

    week52_high_pct = v("week52_high_pct") or -99
    if week52_high_pct >= -1:
        brk_pts += 10
        reasons.append("52-Week Breakout / Near 52-Week High")
    elif week52_high_pct >= -5:
        brk_pts += 5
        reasons.append("Near 52-week high")

    bd.breakout = max(0.0, min(14.0, round(brk_pts, 1)))

    # ── 5. OPEN INTEREST  (max 21 pts) ───────────────────────────────────
    oi_pts = 0.0
    long_buildup   = v("long_buildup")   or (oi_data or {}).get("long_buildup", False)
    short_covering = v("short_covering") or (oi_data or {}).get("short_covering", False)
    oi_increasing  = v("oi_increasing")  or (oi_data or {}).get("oi_increasing", False)
    price_up_oi_up = price and ind.get("change_pct", 0) > 0 and oi_increasing

    if long_buildup:
        oi_pts += 10
        reasons.append("Long Build-up (Price ↑ + OI ↑)")
    if short_covering:
        oi_pts += 8
        reasons.append("Short Covering (Price ↑ + OI ↓)")
    if oi_increasing and not long_buildup:
        oi_pts += 5
        reasons.append("Open Interest increasing")
    if price_up_oi_up and not long_buildup:
        oi_pts += 8

    change_pct = ind.get("change_pct", 0) or 0
    if change_pct < 0 and oi_increasing:
        oi_pts -= 8
        rejects.append("Short Build-up (Price ↓ + OI ↑) – bearish")
    elif change_pct > 0 and not oi_increasing and oi_increasing is not None:
        oi_pts += 3  # Price rising OI falling = short covering
    bd.open_interest = max(0.0, min(21.0, round(oi_pts, 1)))

    # ── 6. TREND CONFIRMATION  (max 18 pts) ─────────────────────────────
    tc_pts = 0.0
    st_dir = v("supertrend_dir")
    if st_dir == "buy":
        tc_pts += 8
        reasons.append("Supertrend BUY signal")
    elif st_dir == "sell":
        rejects.append("Supertrend SELL – bearish")

    vwap = v("vwap")
    if vwap and price:
        if price > vwap:
            tc_pts += 5
            reasons.append(f"Price above VWAP ({price:.0f} > {vwap:.0f})")
        else:
            rejects.append("Price below VWAP")
        # VWAP BUY (additional)
        if price > vwap * 1.001:
            tc_pts += 5
    bd.supertrend = max(0.0, min(10.0, round(tc_pts, 1)))
    bd.vwap       = max(0.0, min(8.0,  round(max(0, tc_pts - 8.0), 1)))

    # ── 7. RELATIVE STRENGTH  (max 18 pts) ──────────────────────────────
    rs_pts = 0.0
    rs = stock_return_5d - nifty_return_5d
    if rs > 2:
        rs_pts += 8
        reasons.append(f"Outperforming Nifty by {rs:.1f}% (5d)")
    elif rs > 0:
        rs_pts += 5
        reasons.append(f"Beating Nifty by {rs:.1f}%")
    else:
        rejects.append(f"Underperforming Nifty ({rs:.1f}%)")
    bd.relative_strength = max(0.0, min(8.0, round(rs_pts, 1)))

    if sector_rank >= 0.7:
        bd.sector_strength = 10.0
        reasons.append(f"Strong sector (rank {sector_rank:.0%})")
    elif sector_rank >= 0.5:
        bd.sector_strength = 6.0
    elif sector_rank < 0.3:
        bd.sector_strength = 0.0
        rejects.append("Weak sector performance")
    else:
        bd.sector_strength = 3.0

    rs_line_rising = v("rs_line_rising")
    if rs_line_rising:
        rs_pts += 5

    # ── 8. MARKET CONFIRMATION  (max 16 pts) ────────────────────────────
    mkt_pts = 0.0
    if market_bullish:
        mkt_pts += 10
        reasons.append("Market trend bullish")
    else:
        rejects.append("Market trend not bullish")

    # Bonus market indicators (from ind if available)
    if v("nifty_above_ema20"):
        mkt_pts += 3
    if v("nifty_above_ema50"):
        mkt_pts += 3
    bd.market_trend = max(0.0, min(16.0, round(mkt_pts, 1)))

    # ── Risk deductions ──────────────────────────────────────────────────
    risk_deduct = 0.0
    atr = v("atr")
    if atr and price:
        atr_pct = (atr / price) * 100
        if atr_pct > 5:
            risk_deduct += 5
            rejects.append(f"High volatility ATR={atr_pct:.1f}%")
    pcr = v("pcr") or 0
    if pcr > 1.5:
        risk_deduct += 3
    week52_low_pct = v("week52_low_pct") or 100
    if week52_low_pct < 5:
        risk_deduct += 5
        rejects.append("Near 52-week low – weak")
    bd.risk = -round(min(15.0, risk_deduct), 1)

    # ── Total (cap at 100) ───────────────────────────────────────────────
    raw_total = (
        bd.ema_trend + bd.rsi + bd.macd + bd.adx +
        bd.volume + bd.delivery +
        bd.price_action + bd.breakout +
        bd.open_interest +
        bd.supertrend + bd.vwap +
        bd.relative_strength + bd.sector_strength +
        bd.market_trend + bd.risk
    )
    bd.total = round(max(0.0, min(100.0, raw_total)), 1)

    # ── Qualification check ──────────────────────────────────────────────
    hard_fails = [r for r in rejects if any(kw in r.lower() for kw in [
        "death cross", "short build-up", "price below ema20",
        "supertrend sell", "market trend not bullish"
    ])]
    is_qualified = (
        bd.total >= 60 and
        len(hard_fails) == 0 and
        (rsi is None or 40 <= rsi <= 85) and
        (gap_pct or 0) <= 5
    )

    return bd, reasons, rejects, is_qualified


def compute_levels(
    price: float,
    atr: Optional[float],
    ind: Dict[str, Any],
    capital: float = 100_000.0,
    max_risk_pct: float = 1.0,
) -> Dict[str, Any]:
    """Entry / Target / Stop-loss / Position sizing."""
    entry = round(price, 2)

    sl_candidates = [price * 0.97]
    ema20 = ind.get("ema20"); st = ind.get("supertrend")
    if atr:
        sl_candidates.append(price - 1.5 * atr)
    if ema20 and ema20 < price:
        sl_candidates.append(ema20 * 0.995)
    if st and st < price:
        sl_candidates.append(st * 0.998)

    stop_loss = round(max(sl_candidates), 2)
    risk_per_share = max(entry - stop_loss, entry * 0.01)

    rsi       = ind.get("rsi") or 50
    macd_hist = ind.get("macd_hist") or 0
    target_pct = 3.0 if (macd_hist > 0 and rsi < 70) else 2.0
    target     = round(entry + target_pct * risk_per_share, 2)
    rr         = round((target - entry) / risk_per_share, 2)
    exp_ret    = round(((target - entry) / entry) * 100, 2)

    max_loss  = capital * (max_risk_pct / 100)
    qty       = max(1, int(max_loss / risk_per_share))
    pos_size  = round(qty * entry, 2)
    prob      = min(95, max(40, 50 + (rsi - 50) * 0.3 + macd_hist * 100))

    return {
        "entry_price":          entry,
        "target_price":         target,
        "stop_loss":            stop_loss,
        "risk_reward_ratio":    rr,
        "expected_return_pct":  exp_ret,
        "success_probability":  round(prob, 1),
        "qty":                  qty,
        "position_size":        pos_size,
    }
