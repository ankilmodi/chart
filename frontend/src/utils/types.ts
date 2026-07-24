// All TypeScript types for the Nifty Future Analyzer

export interface ScoreBreakdown {
  ema_trend: number;
  golden_cross: number;
  price_vs_ema: number;
  rsi: number;
  macd: number;
  adx: number;
  volume: number;
  delivery: number;
  price_action: number;
  breakout: number;
  candle_pattern: number;
  open_interest: number;
  supertrend: number;
  vwap: number;
  relative_strength: number;
  sector_strength: number;
  market_trend: number;
  risk: number;
  total: number;
}

export interface StockData {
  symbol: string;
  name: string;
  sector: string;
  industry?: string;
  index?: string;
  market_cap?: number;

  // Price
  current_price: number;
  future_price?: number;
  premium_discount?: number;
  open?: number;
  high?: number;
  low?: number;
  close?: number;
  prev_close?: number;
  change?: number;
  change_pct?: number;
  future_change_pct?: number;

  // Volume
  volume?: number;
  avg_volume_20d?: number;
  volume_ratio?: number;
  delivery_pct?: number;

  // OI
  oi?: number;
  oi_change_pct?: number;
  pcr?: number;

  // Indicators
  vwap?: number;
  ema9?: number;
  ema20?: number;
  ema50?: number;
  ema100?: number;
  ema200?: number;
  rsi?: number;
  macd?: number;
  macd_signal_line?: number;
  macd_histogram?: number;
  adx?: number;
  atr?: number;
  supertrend?: number;
  supertrend_signal?: string;
  bb_upper?: number;
  bb_middle?: number;
  bb_lower?: number;
  relative_strength?: number;

  // 52-week
  week52_high?: number;
  week52_low?: number;
  week52_high_pct?: number;
  week52_low_pct?: number;

  // Classification
  trend?: string;
  momentum?: string;
  breakout_type?: string;
  consecutive_green?: number;
  star_rating?: number;

  // Support/Resistance
  support?: number;
  resistance?: number;

  // OI patterns
  long_buildup?: boolean;
  short_covering?: boolean;
  short_buildup?: boolean;
  long_unwinding?: boolean;

  // Trade levels
  entry_price?: number;
  target_price?: number;
  stop_loss?: number;
  risk_reward_ratio?: number;
  expected_return_pct?: number;
  success_probability?: number;

  // Score
  confidence_score: number;
  buy_score: number;
  signal?: string;
  recommendation?: string;
  score_breakdown?: ScoreBreakdown;
  reasons?: string[];
  reject_reasons?: string[];
  macd_signal?: string;
  scanned_at?: string;
}

export interface MarketOverview {
  nifty_price?: number;
  nifty_change_pct?: number;
  nifty_ema20?: number;
  nifty_ema50?: number;
  nifty_ema200?: number;
  nifty_above_ema20: boolean;
  nifty_above_ema50: boolean;
  nifty_above_ema200: boolean;
  nifty_vwap?: number;
  nifty_above_vwap: boolean;
  banknifty_price?: number;
  banknifty_change_pct?: number;
  vix?: number;
  vix_safe: boolean;
  market_trend: 'bullish' | 'bearish' | 'sideways';
  data_source: 'live' | 'last_known' | 'unavailable';
  timestamp: string;
}

export interface HeatmapItem {
  symbol: string;
  name: string;
  sector: string;
  price: number;
  change_pct: number;
  buy_score: number;
  signal: string;
  volume?: number;
  oi_change_pct?: number;
  market_cap?: number;
  trend?: string;
  color: 'dark_green' | 'green' | 'yellow' | 'orange' | 'red';
}

export interface HeatmapResponse {
  items: HeatmapItem[];
  total: number;
  timestamp: string;
}

export interface StocksResponse {
  stocks: StockData[];
  total: number;
  timestamp: string;
}

export interface WatchlistItem {
  symbol: string;
  name: string;
  sector: string;
  added_at: string;
  notes?: string;
  target?: number;
  stop_loss?: number;
  current_price?: number;
  change_pct?: number;
  buy_score?: number;
  signal?: string;
}

export interface FormulaEntry {
  name: string;
  category: string;
  formula: string;
  calculation: string;
  interpretation: string;
  bullish_condition: string;
  bearish_condition: string;
  example: string;
}

export interface Notification {
  id: string;
  type: string;
  symbol: string;
  message: string;
  score?: number;
  timestamp: string;
  read: boolean;
}

export interface NotificationResponse {
  notifications: Notification[];
  unread_count: number;
  total: number;
}

// Legacy types kept for backward compat
export interface MarketData {
  price: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  change: number;
  change_pct: number;
  prev_close: number;
  timestamp: string;
}

export interface IndicatorValues {
  ema9?: number;
  ema20?: number;
  ema50?: number;
  ema200?: number;
  rsi?: number;
  macd?: number;
  macd_signal?: number;
  macd_histogram?: number;
  adx?: number;
  atr?: number;
  vwap?: number;
  bb_upper?: number;
  bb_middle?: number;
  bb_lower?: number;
  supertrend?: number;
  supertrend_direction?: string;
  volume_ratio?: number;
  timestamp: string;
}

export interface SignalResponse {
  signal: 'BUY' | 'SELL' | 'WAIT';
  confidence: number;
  reasons: string[];
  timestamp: string;
}

export interface HistoryResponse {
  symbol: string;
  interval: string;
  candles: Candle[];
  total: number;
}

export interface Candle {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface GapAnalysis {
  prev_close: number;
  open: number;
  gap_points: number;
  gap_pct: number;
  gap_type: string;
  timestamp: string;
}

export interface OrbAnalysis {
  orb_high: number;
  orb_low: number;
  current_price: number;
  status: string;
  timestamp: string;
}

export interface StocksQuotesResponse {
  quotes: any[];
  total: number;
  timestamp: string;
}

export type SignalType = 'STRONG BUY' | 'BUY' | 'WATCH' | 'HOLD' | 'SELL' | 'STRONG SELL';
export type TrendType = 'Strong Uptrend' | 'Uptrend' | 'Sideways' | 'Weak Downtrend' | 'Strong Downtrend';
export type MomentumType = 'Strong' | 'Increasing' | 'Weak' | 'Loss';
