import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box, Grid, Card, CardContent, Typography, Chip,
  LinearProgress, Stack, Divider, Button, CircularProgress,
  Alert, Paper,
} from '@mui/material';
import {
  TrendingUp, TrendingDown, Star, Bolt, ShowChart,
  Refresh, ArrowForward, VolumeUp,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { fetchMarketOverview, fetchTopBuy, fetchBreakout, fetchMomentum } from '../services/api';
import { StockTable } from '../components/StockTable';
import type { StockData } from '../utils/types';

const MetricCard: React.FC<{
  title: string; value: string | number; sub?: string;
  color?: string; icon?: React.ReactNode;
}> = ({ title, value, sub, color, icon }) => (
  <Card elevation={2}>
    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
      <Stack direction="row" spacing={1} alignItems="center" mb={0.5}>
        {icon && <Box sx={{ color: color || 'primary.main' }}>{icon}</Box>}
        <Typography variant="caption" color="text.secondary">{title}</Typography>
      </Stack>
      <Typography variant="h6" fontWeight={700} color={color}>{value}</Typography>
      {sub && <Typography variant="caption" color="text.secondary">{sub}</Typography>}
    </CardContent>
  </Card>
);

const SignalBadge: React.FC<{ signal: string }> = ({ signal }) => {
  const colorMap: Record<string, any> = {
    'STRONG BUY': 'success', 'BUY': 'success', 'WATCH': 'info',
    'HOLD': 'warning', 'SELL': 'error', 'STRONG SELL': 'error',
  };
  return <Chip label={signal} size="small" color={colorMap[signal] || 'default'} />;
};

export default function DashboardPage() {
  const navigate  = useNavigate();

  const { data: market, isLoading: mktLoading } = useQuery({
    queryKey: ['market-overview'],
    queryFn: fetchMarketOverview,
    refetchInterval: 60_000,
  });

  const { data: topBuy, isLoading: tbLoading } = useQuery({
    queryKey: ['top-buy'],
    queryFn: () => fetchTopBuy(5),
    refetchInterval: 300_000,
  });

  const { data: breakout, isLoading: brLoading } = useQuery({
    queryKey: ['breakout'],
    queryFn: () => fetchBreakout(5),
    refetchInterval: 300_000,
  });

  const { data: momentum } = useQuery({
    queryKey: ['momentum'],
    queryFn: () => fetchMomentum(5),
    refetchInterval: 300_000,
  });

  const topStocks: StockData[] = topBuy?.stocks || [];
  const breakoutStocks: StockData[] = breakout?.stocks || [];

  return (
    <Box sx={{ p: 3 }}>
      <Stack direction="row" spacing={1} alignItems="center" mb={3}>
        <Typography variant="h5" fontWeight={700}>Dashboard</Typography>
        <Chip label="NSE F&O Only" size="small" variant="outlined" />
        {mktLoading && <CircularProgress size={16} />}
      </Stack>

      {/* Data source warning */}
      {market && market.data_source !== 'live' && (
        <Alert severity={market.data_source === 'last_known' ? 'warning' : 'error'} sx={{ mb: 2 }}>
          {market.data_source === 'last_known'
            ? '⚠️ Showing last known prices – Yahoo Finance temporarily unavailable. Data may be delayed.'
            : '❌ Market data unavailable. Yahoo Finance is not responding.'}
        </Alert>
      )}

      {/* Market Overview */}
      {market && (
        <Grid container spacing={2} mb={3}>
          <Grid item xs={6} sm={3}>
            <MetricCard
              title="NIFTY 50"
              value={`₹${market.nifty_price?.toLocaleString('en-IN', { maximumFractionDigits: 0 }) ?? '—'}`}
              sub={market.nifty_change_pct != null ? `${market.nifty_change_pct >= 0 ? '+' : ''}${market.nifty_change_pct?.toFixed(2)}%` : ''}
              color={market.nifty_change_pct != null && market.nifty_change_pct >= 0 ? '#4caf50' : '#f44336'}
              icon={<TrendingUp />}
            />
          </Grid>
          <Grid item xs={6} sm={3}>
            <MetricCard
              title="BANKNIFTY"
              value={`₹${market.banknifty_price?.toLocaleString('en-IN', { maximumFractionDigits: 0 }) ?? '—'}`}
              sub={market.banknifty_change_pct != null ? `${market.banknifty_change_pct >= 0 ? '+' : ''}${market.banknifty_change_pct?.toFixed(2)}%` : ''}
              icon={<ShowChart />}
            />
          </Grid>
          <Grid item xs={6} sm={3}>
            <MetricCard
              title="India VIX"
              value={market.vix?.toFixed(2) ?? '—'}
              sub={market.vix_safe ? '✅ Safe Zone' : '⚠️ Elevated'}
              color={market.vix_safe ? '#4caf50' : '#f44336'}
            />
          </Grid>
          <Grid item xs={6} sm={3}>
            <MetricCard
              title="Market Trend"
              value={market.market_trend?.toUpperCase() ?? '—'}
              color={market.market_trend === 'bullish' ? '#4caf50' : market.market_trend === 'bearish' ? '#f44336' : '#ff9800'}
              icon={market.market_trend === 'bullish' ? <TrendingUp /> : <TrendingDown />}
            />
          </Grid>
        </Grid>
      )}

      {/* Market condition chips */}
      {market && (
        <Paper sx={{ p: 2, mb: 3 }} elevation={1}>
          <Typography variant="subtitle2" fontWeight={600} mb={1}>Market Conditions</Typography>
          <Stack direction="row" flexWrap="wrap" gap={1}>
            {[
              { label: 'NIFTY > EMA20',  ok: market.nifty_above_ema20  },
              { label: 'NIFTY > EMA50',  ok: market.nifty_above_ema50  },
              { label: 'NIFTY > EMA200', ok: market.nifty_above_ema200 },
              { label: 'Above VWAP',     ok: market.nifty_above_vwap   },
              { label: 'VIX Safe',       ok: market.vix_safe           },
            ].map(c => (
              <Chip key={c.label} label={c.label} size="small"
                color={c.ok ? 'success' : 'error'} variant={c.ok ? 'filled' : 'outlined'} />
            ))}
          </Stack>
        </Paper>
      )}

      {/* Screener Summary Cards */}
      <Grid container spacing={2} mb={3}>
        {[
          { title: '🔥 Top Buy Today',     count: topBuy?.total,     path: '/top-buy',        color: '#4caf50' },
          { title: '📈 Breakout Stocks',   count: breakout?.total,   path: '/breakout',       color: '#2196f3' },
          { title: '⚡ Momentum Stocks',   count: momentum?.total,   path: '/momentum',       color: '#ff9800' },
          { title: '🏃 Swing Buy',         count: undefined,          path: '/swing-buy',      color: '#9c27b0' },
        ].map(item => (
          <Grid item xs={6} sm={3} key={item.title}>
            <Card elevation={2} sx={{ cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
              onClick={() => navigate(item.path)}>
              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                <Typography variant="body2" mb={0.5}>{item.title}</Typography>
                <Typography variant="h5" fontWeight={700} color={item.color}>
                  {item.count ?? <CircularProgress size={16} />}
                </Typography>
                <Typography variant="caption" color="text.secondary">stocks qualified</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Top Buy Table */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Box mb={1} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="subtitle1" fontWeight={700}>
              <Star sx={{ fontSize: 16, mr: 0.5, color: 'warning.main', verticalAlign: 'middle' }} />
              Top Buy Today
            </Typography>
            <Button size="small" endIcon={<ArrowForward />} onClick={() => navigate('/top-buy')}>
              View All
            </Button>
          </Box>
          {tbLoading ? <LinearProgress /> :
            topStocks.length > 0 ? (
              <StockTable data={topStocks} compact />
            ) : (
              <Alert severity="info">No strong buy signals right now.</Alert>
            )
          }
        </Grid>

        <Grid item xs={12} md={6}>
          <Box mb={1} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="subtitle1" fontWeight={700}>
              <Bolt sx={{ fontSize: 16, mr: 0.5, color: 'info.main', verticalAlign: 'middle' }} />
              Breakout Stocks
            </Typography>
            <Button size="small" endIcon={<ArrowForward />} onClick={() => navigate('/breakout')}>
              View All
            </Button>
          </Box>
          {brLoading ? <LinearProgress /> :
            breakoutStocks.length > 0 ? (
              <StockTable data={breakoutStocks} compact />
            ) : (
              <Alert severity="info">No breakouts detected.</Alert>
            )
          }
        </Grid>
      </Grid>

      {/* Score Guide */}
      <Paper sx={{ p: 2, mt: 3 }} elevation={1}>
        <Typography variant="subtitle2" fontWeight={600} mb={1.5}>Buy Score Guide</Typography>
        <Stack direction="row" flexWrap="wrap" gap={1}>
          {[
            { range: '91–100', label: 'Excellent Buy', color: '#1b5e20' },
            { range: '76–90',  label: 'Strong Buy',    color: '#2e7d32' },
            { range: '61–75',  label: 'Good',          color: '#1976d2' },
            { range: '41–60',  label: 'Watch',         color: '#f57c00' },
            { range: '0–40',   label: 'Avoid',         color: '#c62828' },
          ].map(b => (
            <Chip key={b.range}
              label={`${b.range}: ${b.label}`}
              size="small"
              sx={{ bgcolor: b.color, color: '#fff', fontWeight: 600 }}
            />
          ))}
        </Stack>
      </Paper>
    </Box>
  );
}
