import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box, Typography, Stack, Chip, Grid, Paper, Divider,
  LinearProgress, Alert, Button, Table, TableBody,
  TableRow, TableCell,
} from '@mui/material';
import { ArrowBack, Star } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { fetchStockDetail } from '../services/api';
import type { StockData } from '../utils/types';

const Row: React.FC<{ label: string; value: any; highlight?: boolean }> = ({ label, value, highlight }) => (
  <TableRow>
    <TableCell sx={{ color: 'text.secondary', fontSize: 13, border: 0, py: 0.5 }}>{label}</TableCell>
    <TableCell sx={{ fontWeight: highlight ? 700 : 400, fontSize: 13, border: 0, py: 0.5 }}>
      {value ?? '—'}
    </TableCell>
  </TableRow>
);

export default function StockDetailPage() {
  const { symbol } = useParams<{ symbol: string }>();
  const navigate   = useNavigate();

  const { data: stock, isLoading, error } = useQuery<StockData>({
    queryKey: ['stock', symbol],
    queryFn: () => fetchStockDetail(symbol!),
    enabled: !!symbol,
  });

  if (isLoading) return <Box sx={{ p: 3 }}><LinearProgress /></Box>;
  if (error)     return <Box sx={{ p: 3 }}><Alert severity="error">{(error as Error).message}</Alert></Box>;
  if (!stock)    return null;

  const signalColor: Record<string, any> = {
    'STRONG BUY': 'success', 'BUY': 'success', 'WATCH': 'info',
    'HOLD': 'warning', 'SELL': 'error', 'STRONG SELL': 'error',
  };

  return (
    <Box sx={{ p: 3 }}>
      <Button startIcon={<ArrowBack />} size="small" onClick={() => navigate(-1)} sx={{ mb: 2 }}>
        Back
      </Button>

      {/* Header */}
      <Stack direction="row" spacing={2} alignItems="flex-start" mb={3} flexWrap="wrap">
        <Box>
          <Typography variant="h4" fontWeight={700}>{stock.symbol}</Typography>
          <Typography variant="subtitle1" color="text.secondary">{stock.name} • {stock.sector}</Typography>
        </Box>
        <Box flex={1} />
        <Stack spacing={1} alignItems="flex-end">
          <Typography variant="h4" fontWeight={700}>
            ₹{stock.current_price?.toFixed(2)}
          </Typography>
          <Typography
            variant="body1"
            color={(stock.change_pct ?? 0) >= 0 ? 'success.main' : 'error.main'}
            fontWeight={600}>
            {(stock.change_pct ?? 0) >= 0 ? '+' : ''}{stock.change_pct?.toFixed(2)}%
          </Typography>
        </Stack>
        {stock.signal && (
          <Chip label={stock.signal} size="medium" color={signalColor[stock.signal] || 'default'}
            sx={{ fontWeight: 700, fontSize: 14 }} />
        )}
      </Stack>

      {/* Score bar */}
      <Paper sx={{ p: 2, mb: 3 }} elevation={2}>
        <Stack direction="row" spacing={2} alignItems="center" mb={1}>
          <Typography variant="subtitle1" fontWeight={700}>AI Buy Score</Typography>
          <Typography variant="h5" fontWeight={800} color={
            (stock.buy_score || 0) >= 76 ? 'success.main' :
            (stock.buy_score || 0) >= 61 ? 'info.main' : 'warning.main'
          }>
            {stock.buy_score?.toFixed(0)} / 100
          </Typography>
          <Chip label={stock.recommendation || '—'} size="small"
            color={signalColor[stock.signal || ''] || 'default'} />
          {stock.star_rating ? <Typography color="warning.main">{'★'.repeat(stock.star_rating)}</Typography> : null}
        </Stack>
        <LinearProgress variant="determinate" value={stock.buy_score || 0}
          sx={{ height: 8, borderRadius: 4,
                '& .MuiLinearProgress-bar': {
                  bgcolor: (stock.buy_score || 0) >= 76 ? 'success.main' : 'info.main',
                } }} />
      </Paper>

      <Grid container spacing={2}>
        {/* Price data */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }} elevation={2}>
            <Typography variant="subtitle2" fontWeight={700} mb={1}>Price Data</Typography>
            <Table size="small">
              <TableBody>
                <Row label="Open"        value={stock.open ? `₹${stock.open.toFixed(2)}` : undefined} />
                <Row label="High"        value={stock.high ? `₹${stock.high.toFixed(2)}` : undefined} />
                <Row label="Low"         value={stock.low  ? `₹${stock.low.toFixed(2)}`  : undefined} />
                <Row label="Close"       value={stock.close? `₹${stock.close.toFixed(2)}`: undefined} />
                <Row label="Prev Close"  value={stock.prev_close ? `₹${stock.prev_close.toFixed(2)}` : undefined} />
                <Row label="52W High"    value={stock.week52_high ? `₹${stock.week52_high.toFixed(0)}` : undefined} />
                <Row label="52W Low"     value={stock.week52_low  ? `₹${stock.week52_low.toFixed(0)}`  : undefined} />
                <Row label="52W High %"  value={stock.week52_high_pct != null ? `${stock.week52_high_pct.toFixed(1)}%` : undefined} />
              </TableBody>
            </Table>
          </Paper>
        </Grid>

        {/* Indicators */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }} elevation={2}>
            <Typography variant="subtitle2" fontWeight={700} mb={1}>Indicators</Typography>
            <Table size="small">
              <TableBody>
                <Row label="EMA 20"       value={stock.ema20   ? `₹${stock.ema20.toFixed(0)}`   : undefined} />
                <Row label="EMA 50"       value={stock.ema50   ? `₹${stock.ema50.toFixed(0)}`   : undefined} />
                <Row label="EMA 200"      value={stock.ema200  ? `₹${stock.ema200.toFixed(0)}`  : undefined} />
                <Row label="VWAP"         value={stock.vwap    ? `₹${stock.vwap.toFixed(0)}`    : undefined} />
                <Row label="RSI"          value={stock.rsi     ? stock.rsi.toFixed(1)            : undefined} highlight />
                <Row label="MACD"         value={stock.macd    ? stock.macd.toFixed(4)           : undefined} />
                <Row label="ADX"          value={stock.adx     ? stock.adx.toFixed(1)            : undefined} highlight />
                <Row label="Supertrend"   value={stock.supertrend_signal?.toUpperCase()} highlight />
                <Row label="BB Upper"     value={stock.bb_upper  ? `₹${stock.bb_upper.toFixed(0)}`  : undefined} />
                <Row label="BB Lower"     value={stock.bb_lower  ? `₹${stock.bb_lower.toFixed(0)}`  : undefined} />
              </TableBody>
            </Table>
          </Paper>
        </Grid>

        {/* Trade info */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }} elevation={2}>
            <Typography variant="subtitle2" fontWeight={700} mb={1}>Trade Levels</Typography>
            <Table size="small">
              <TableBody>
                <Row label="Entry"        value={stock.entry_price  ? `₹${stock.entry_price.toFixed(2)}`  : undefined} highlight />
                <Row label="Target"       value={stock.target_price ? `₹${stock.target_price.toFixed(2)}` : undefined} highlight />
                <Row label="Stop Loss"    value={stock.stop_loss    ? `₹${stock.stop_loss.toFixed(2)}`    : undefined} highlight />
                <Row label="R:R Ratio"    value={stock.risk_reward_ratio ? `1:${stock.risk_reward_ratio.toFixed(1)}` : undefined} />
                <Row label="Exp Return"   value={stock.expected_return_pct ? `${stock.expected_return_pct.toFixed(1)}%` : undefined} />
                <Row label="Success Prob" value={stock.success_probability ? `${stock.success_probability.toFixed(0)}%` : undefined} />
                <Row label="Support"      value={stock.support    ? `₹${stock.support.toFixed(0)}`    : undefined} />
                <Row label="Resistance"   value={stock.resistance ? `₹${stock.resistance.toFixed(0)}` : undefined} />
                <Row label="Trend"        value={stock.trend}  highlight />
                <Row label="Momentum"     value={stock.momentum} highlight />
                <Row label="Breakout"     value={stock.breakout_type} />
              </TableBody>
            </Table>
          </Paper>
        </Grid>

        {/* Reasons */}
        {stock.reasons && stock.reasons.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }} elevation={2}>
              <Typography variant="subtitle2" fontWeight={700} mb={1} color="success.main">
                ✅ Bullish Reasons ({stock.reasons.length})
              </Typography>
              <Stack spacing={0.5}>
                {stock.reasons.map((r, i) => (
                  <Typography key={i} variant="body2">• {r}</Typography>
                ))}
              </Stack>
            </Paper>
          </Grid>
        )}

        {stock.reject_reasons && stock.reject_reasons.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 2 }} elevation={2}>
              <Typography variant="subtitle2" fontWeight={700} mb={1} color="error.main">
                ⚠️ Risk Factors ({stock.reject_reasons.length})
              </Typography>
              <Stack spacing={0.5}>
                {stock.reject_reasons.map((r, i) => (
                  <Typography key={i} variant="body2" color="error.main">• {r}</Typography>
                ))}
              </Stack>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
}
