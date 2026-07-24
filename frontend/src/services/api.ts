/**
 * API service layer – all backend calls go through here.
 */
import axios, { AxiosError } from 'axios';
import type {
  MarketData, IndicatorValues, SignalResponse, HistoryResponse,
  StocksResponse, HeatmapResponse, WatchlistItem,
  NotificationResponse, MarketOverview,
} from '../utils/types';

const BASE_URL = import.meta.env.VITE_API_URL || '/api';

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// Separate instance for slow scanner endpoints (full scan can take 30–60s first time)
export const apiSlow = axios.create({
  baseURL: BASE_URL,
  timeout: 90000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.response.use(
  (res) => res,
  (error: AxiosError) => {
    if (error.code === 'ECONNABORTED') throw new Error('Request timeout');
    if (!error.response) throw new Error('Network error – check your connection');
    const status = error.response.status;
    if (status === 503) throw new Error('Data unavailable – market may be closed');
    if (status === 429) throw new Error('Rate limit exceeded – please wait');
    throw new Error((error.response.data as any)?.detail || 'API error');
  }
);

apiSlow.interceptors.response.use(
  (res) => res,
  (error: AxiosError) => {
    if (error.code === 'ECONNABORTED') throw new Error('Scan timeout – try again in a moment');
    if (!error.response) throw new Error('Network error – check your connection');
    const status = error.response.status;
    if (status === 503) throw new Error('Data unavailable – market may be closed');
    throw new Error((error.response.data as any)?.detail || 'API error');
  }
);

// ── Market ─────────────────────────────────────────────────────────────────
export const fetchMarket       = async (): Promise<MarketData>     => (await api.get('/market')).data;
export const fetchMarketOverview = async (): Promise<MarketOverview> => (await api.get('/market-overview')).data;
export const fetchIndicators   = async (): Promise<IndicatorValues> => (await api.get('/indicators')).data;
export const fetchSignal       = async (): Promise<SignalResponse>  => (await api.get('/signal')).data;
export const fetchHistory      = async (limit = 100): Promise<HistoryResponse> =>
  (await api.get(`/history?limit=${limit}`)).data;
export const clearCache        = async (): Promise<void> => { await api.post('/cache/clear'); };

// ── Screeners ──────────────────────────────────────────────────────────────
export const fetchFutureStocks = async (params?: {
  force?: boolean; min_score?: number; sector?: string;
  signal?: string; trend?: string; limit?: number;
}): Promise<StocksResponse> => {
  const q = new URLSearchParams();
  if (params?.force)     q.set('force',     String(params.force));
  if (params?.min_score) q.set('min_score', String(params.min_score));
  if (params?.sector)    q.set('sector',    params.sector);
  if (params?.signal)    q.set('signal',    params.signal);
  if (params?.trend)     q.set('trend',     params.trend);
  if (params?.limit)     q.set('limit',     String(params.limit));
  return (await apiSlow.get(`/future-stocks?${q}`)).data;
};

export const fetchHeatmap        = async (force = false): Promise<HeatmapResponse> =>
  (await apiSlow.get(`/heatmap?force=${force}`)).data;

export const fetchTopBuy         = async (limit = 20): Promise<StocksResponse> =>
  (await apiSlow.get(`/top-buy?limit=${limit}`)).data;

export const fetchSwingBuy       = async (limit = 20): Promise<StocksResponse> =>
  (await apiSlow.get(`/swing-buy?limit=${limit}`)).data;

export const fetchWeeklyBuy      = async (limit = 20): Promise<StocksResponse> =>
  (await apiSlow.get(`/weekly-buy?limit=${limit}`)).data;

export const fetchBreakout       = async (limit = 20): Promise<StocksResponse> =>
  (await apiSlow.get(`/breakout?limit=${limit}`)).data;

export const fetchMomentum       = async (limit = 20): Promise<StocksResponse> =>
  (await apiSlow.get(`/momentum?limit=${limit}`)).data;

export const fetchLongBuildup    = async (limit = 20): Promise<StocksResponse> =>
  (await apiSlow.get(`/long-build-up?limit=${limit}`)).data;

export const fetchShortCovering  = async (limit = 20): Promise<StocksResponse> =>
  (await apiSlow.get(`/short-covering?limit=${limit}`)).data;

export const fetchVolumeShockers = async (limit = 20): Promise<StocksResponse> =>
  (await apiSlow.get(`/volume-shockers?limit=${limit}`)).data;

export const fetchEmaScreener    = async (limit = 30): Promise<StocksResponse> =>
  (await apiSlow.get(`/ema-screener?limit=${limit}`)).data;

export const fetchOiAnalysis     = async (limit = 30): Promise<StocksResponse> =>
  (await apiSlow.get(`/oi-analysis?limit=${limit}`)).data;

export const fetchStockDetail    = async (symbol: string) =>
  (await apiSlow.get(`/stock/${symbol}`)).data;

export const fetchScanner        = async (minScore = 60, force = false): Promise<StocksResponse> =>
  (await apiSlow.get(`/scanner?min_score=${minScore}&force=${force}`)).data;

// ── Formula ────────────────────────────────────────────────────────────────
export const fetchFormulas = async () => (await api.get('/formula')).data;

// ── Watchlist ──────────────────────────────────────────────────────────────
export const fetchWatchlist  = async () => (await api.get('/watchlist')).data;
export const addToWatchlist  = async (item: WatchlistItem) => (await api.post('/watchlist', item)).data;
export const removeWatchlist = async (symbol: string) => (await api.delete(`/watchlist/${symbol}`)).data;

// ── Notifications ──────────────────────────────────────────────────────────
export const fetchNotifications     = async (): Promise<NotificationResponse> =>
  (await api.get('/notifications')).data;
export const markNotifRead          = async (id: string) =>
  (await api.post(`/notifications/read/${id}`)).data;
export const generateNotifications  = async () =>
  (await api.post('/notifications/generate')).data;

// ── Export ─────────────────────────────────────────────────────────────────
export const exportCSV = (minScore = 0) => {
  window.open(`${BASE_URL}/export/csv?min_score=${minScore}`, '_blank');
};
