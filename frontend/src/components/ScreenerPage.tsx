import React from 'react';
import {
  Box, Typography, Stack, Chip, Alert, LinearProgress,
  IconButton, Tooltip, Button,
} from '@mui/material';
import { Refresh, Download } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { StockTable } from './StockTable';
import { exportCSV } from '../services/api';
import type { StockData, StocksResponse } from '../utils/types';

interface Props {
  title: string;
  subtitle?: string;
  icon?: string;
  queryKey: string;
  fetcher: () => Promise<StocksResponse>;
  refetchInterval?: number;
  columns?: string[];
}

export const ScreenerPage: React.FC<Props> = ({
  title, subtitle, icon, queryKey, fetcher, refetchInterval = 300_000,
}) => {
  const { data, isLoading, error, refetch, isFetching } = useQuery<StocksResponse>({
    queryKey: [queryKey],
    queryFn: fetcher,
    refetchInterval,
  });

  const stocks: StockData[] = data?.stocks ?? [];

  return (
    <Box sx={{ p: 3 }}>
      <Stack direction="row" spacing={1} alignItems="center" mb={2} flexWrap="wrap">
        <Typography variant="h5" fontWeight={700}>
          {icon} {title}
        </Typography>
        {data && <Chip label={`${stocks.length} stocks`} size="small" color="primary" />}
        {(isLoading || isFetching) && <LinearProgress sx={{ width: 80, ml: 1 }} />}
        <Box flex={1} />
        <Tooltip title="Refresh">
          <IconButton size="small" onClick={() => refetch()}><Refresh /></IconButton>
        </Tooltip>
        <Tooltip title="Export CSV">
          <IconButton size="small" onClick={() => exportCSV()}><Download /></IconButton>
        </Tooltip>
      </Stack>

      {subtitle && (
        <Typography variant="body2" color="text.secondary" mb={2}>{subtitle}</Typography>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {(error as Error).message}
        </Alert>
      )}

      {!isLoading && stocks.length === 0 && !error && (
        <Alert severity="info">No stocks match this criteria right now.</Alert>
      )}

      <StockTable data={stocks} loading={isLoading} />

      <Typography variant="caption" color="text.secondary" mt={1} display="block">
        Last updated: {data?.timestamp ?? '—'} • Refreshes every 5 min
      </Typography>
    </Box>
  );
};
