import React, { useState } from 'react';
import {
  Box, Typography, Stack, Chip, Paper, Button, Grid,
  TextField, MenuItem, Select, FormControl, InputLabel,
  Slider, Switch, FormControlLabel, Collapse, CircularProgress,
  Alert, IconButton, Tooltip, LinearProgress,
} from '@mui/material';
import {
  FilterList, Refresh, Download, ExpandMore, ExpandLess, Clear,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { fetchFutureStocks, exportCSV } from '../services/api';
import { StockTable } from '../components/StockTable';
import type { StockData } from '../utils/types';

const SECTORS = [
  'All', 'Banking', 'IT', 'Energy', 'Auto', 'FMCG', 'Pharma',
  'Finance', 'Metal', 'Infrastructure', 'Telecom', 'Consumer',
];
const SIGNALS  = ['All', 'STRONG BUY', 'BUY', 'WATCH', 'HOLD', 'SELL', 'STRONG SELL'];
const TRENDS   = ['All', 'Strong Uptrend', 'Uptrend', 'Sideways', 'Weak Downtrend', 'Strong Downtrend'];

export default function FutureStocksPage() {
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [sector,    setSector]    = useState('All');
  const [signal,    setSignal]    = useState('All');
  const [trend,     setTrend]     = useState('All');
  const [minScore,  setMinScore]  = useState(0);
  const [minVol,    setMinVol]    = useState(0);

  const { data, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ['future-stocks', sector, signal, trend, minScore],
    queryFn: () =>
      fetchFutureStocks({
        sector:    sector !== 'All' ? sector : undefined,
        signal:    signal !== 'All' ? signal : undefined,
        trend:     trend  !== 'All' ? trend  : undefined,
        min_score: minScore > 0 ? minScore : undefined,
        limit: 200,
      }),
    refetchInterval: 300_000,
  });

  const stocks: StockData[] = data?.stocks ?? [];

  const filtered = minVol > 0
    ? stocks.filter(s => (s.volume_ratio ?? 0) >= minVol)
    : stocks;

  const handleReset = () => {
    setSector('All'); setSignal('All'); setTrend('All');
    setMinScore(0);   setMinVol(0);
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Stack direction="row" spacing={1} alignItems="center" mb={2} flexWrap="wrap">
        <Typography variant="h5" fontWeight={700}>Nifty F&O Stocks</Typography>
        <Chip label={`${filtered.length} stocks`} size="small" color="primary" />
        {isFetching && <CircularProgress size={16} />}
        <Box flex={1} />
        <Tooltip title="Refresh">
          <IconButton size="small" onClick={() => refetch()}><Refresh /></IconButton>
        </Tooltip>
        <Tooltip title="Export CSV">
          <IconButton size="small" onClick={() => exportCSV(minScore)}><Download /></IconButton>
        </Tooltip>
        <Button
          size="small"
          variant="outlined"
          startIcon={<FilterList />}
          endIcon={filtersOpen ? <ExpandLess /> : <ExpandMore />}
          onClick={() => setFiltersOpen(!filtersOpen)}>
          Filters
        </Button>
      </Stack>

      {/* Filters panel */}
      <Collapse in={filtersOpen}>
        <Paper sx={{ p: 2, mb: 2 }} elevation={1}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={3}>
              <FormControl size="small" fullWidth>
                <InputLabel>Sector</InputLabel>
                <Select value={sector} label="Sector" onChange={e => setSector(e.target.value)}>
                  {SECTORS.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <FormControl size="small" fullWidth>
                <InputLabel>Signal</InputLabel>
                <Select value={signal} label="Signal" onChange={e => setSignal(e.target.value)}>
                  {SIGNALS.map(s => <MenuItem key={s} value={s}>{s}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <FormControl size="small" fullWidth>
                <InputLabel>Trend</InputLabel>
                <Select value={trend} label="Trend" onChange={e => setTrend(e.target.value)}>
                  {TRENDS.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="caption" color="text.secondary">
                Min Buy Score: <strong>{minScore}</strong>
              </Typography>
              <Slider value={minScore} min={0} max={100} step={5}
                onChange={(_, v) => setMinScore(v as number)} size="small" />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="caption" color="text.secondary">
                Min Vol Ratio: <strong>{minVol > 0 ? `${minVol}x` : 'All'}</strong>
              </Typography>
              <Slider value={minVol} min={0} max={5} step={0.5}
                onChange={(_, v) => setMinVol(v as number)} size="small" />
            </Grid>
            <Grid item xs="auto">
              <Button size="small" startIcon={<Clear />} onClick={handleReset}>
                Reset
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </Collapse>

      {/* Summary chips */}
      <Stack direction="row" spacing={1} mb={2} flexWrap="wrap">
        {['STRONG BUY', 'BUY', 'WATCH'].map(sig => {
          const count = stocks.filter(s => s.signal === sig).length;
          const colorMap: Record<string, any> = { 'STRONG BUY': 'success', 'BUY': 'success', 'WATCH': 'info' };
          return count > 0 ? (
            <Chip key={sig} label={`${sig}: ${count}`} size="small" color={colorMap[sig]} />
          ) : null;
        })}
      </Stack>

      {/* Error */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to load stocks. {(error as Error).message}
        </Alert>
      )}

      {/* Loading */}
      {isLoading && <LinearProgress sx={{ mb: 1 }} />}

      {/* Table */}
      <StockTable data={filtered} loading={isLoading} />

      {/* Footer */}
      <Typography variant="caption" color="text.secondary" mt={1} display="block">
        Data refreshes every 5 minutes. Last update: {data?.timestamp ?? '—'}
      </Typography>
    </Box>
  );
}
