import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, Chip, Box, Typography, IconButton, Tooltip, TableSortLabel,
  LinearProgress, Stack,
} from '@mui/material';
import { Info, Star, TrendingUp, TrendingDown } from '@mui/icons-material';
import type { StockData } from '../utils/types';

interface Column {
  id: keyof StockData | 'action';
  label: string;
  minWidth?: number;
  align?: 'left' | 'center' | 'right';
  format?: (value: any, row: StockData) => React.ReactNode;
}

interface Props {
  data: StockData[];
  loading?: boolean;
  compact?: boolean;
}

const defaultColumns: Column[] = [
  {
    id: 'symbol',
    label: 'Symbol',
    minWidth: 100,
    format: (val, row) => (
      <Box>
        <Typography variant="body2" fontWeight={700}>{val}</Typography>
        <Typography variant="caption" color="text.secondary">{row.name}</Typography>
      </Box>
    ),
  },
  {
    id: 'current_price',
    label: 'Price',
    minWidth: 80,
    align: 'right',
    format: (val) => val != null ? `₹${val.toFixed(2)}` : '—',
  },
  {
    id: 'change_pct',
    label: 'Change %',
    minWidth: 80,
    align: 'right',
    format: (val) => val != null ? (
      <Typography variant="body2" color={val >= 0 ? 'success.main' : 'error.main'} fontWeight={600}>
        {val >= 0 ? '+' : ''}{val.toFixed(2)}%
      </Typography>
    ) : '—',
  },
  {
    id: 'buy_score',
    label: 'Buy Score',
    minWidth: 100,
    align: 'center',
    format: (val) => (
      <Box sx={{ display: 'inline-block', minWidth: 60 }}>
        <Typography variant="body2" fontWeight={700} mb={0.2}>
          {val != null ? val.toFixed(0) : '—'} / 100
        </Typography>
        {val != null && (
          <LinearProgress variant="determinate" value={val}
            sx={{ height: 4, borderRadius: 1,
                  '& .MuiLinearProgress-bar': {
                    bgcolor: val >= 76 ? 'success.main' : val >= 61 ? 'info.main' : 'warning.main',
                  } }} />
        )}
      </Box>
    ),
  },
  {
    id: 'signal',
    label: 'Signal',
    minWidth: 110,
    align: 'center',
    format: (val) => {
      const colors: Record<string, any> = {
        'STRONG BUY': 'success',
        'BUY':        'success',
        'WATCH':      'info',
        'HOLD':       'warning',
        'SELL':       'error',
        'STRONG SELL':'error',
      };
      return val ? <Chip label={val} size="small" color={colors[val] || 'default'} /> : '—';
    },
  },
  {
    id: 'trend',
    label: 'Trend',
    minWidth: 130,
    format: (val) => {
      const icon = val?.includes('Uptrend') ? <TrendingUp fontSize="inherit" /> : <TrendingDown fontSize="inherit" />;
      return val ? <Stack direction="row" spacing={0.5} alignItems="center"><>{icon}</> <Typography variant="caption">{val}</Typography></Stack> : '—';
    },
  },
  {
    id: 'rsi',
    label: 'RSI',
    minWidth: 50,
    align: 'right',
    format: (val) => val != null ? val.toFixed(1) : '—',
  },
  {
    id: 'volume_ratio',
    label: 'Vol Ratio',
    minWidth: 70,
    align: 'right',
    format: (val) => val != null ? `${val.toFixed(2)}x` : '—',
  },
  {
    id: 'consecutive_green',
    label: 'Streak',
    minWidth: 60,
    align: 'center',
    format: (val) => {
      const stars = val && val >= 2 ? '★'.repeat(Math.min(val, 5)) : '';
      return stars ? <Tooltip title={`${val} consecutive green candles`}><Typography variant="caption" color="warning.main">{stars}</Typography></Tooltip> : '—';
    },
  },
  {
    id: 'action',
    label: 'Details',
    minWidth: 60,
    align: 'center',
    format: (_, row) => (
      <IconButton size="small" sx={{ color: 'primary.main' }}>
        <Info fontSize="small" />
      </IconButton>
    ),
  },
];

export const StockTable: React.FC<Props> = ({ data, loading, compact }) => {
  const navigate = useNavigate();
  const [orderBy, setOrderBy] = useState<keyof StockData>('buy_score');
  const [order, setOrder] = useState<'asc' | 'desc'>('desc');

  const handleSort = (col: keyof StockData) => {
    if (col === orderBy) {
      setOrder(order === 'asc' ? 'desc' : 'asc');
    } else {
      setOrderBy(col);
      setOrder('desc');
    }
  };

  const sorted = [...data].sort((a, b) => {
    const aVal = a[orderBy] ?? 0;
    const bVal = b[orderBy] ?? 0;
    const cmp = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
    return order === 'asc' ? cmp : -cmp;
  });

  const columns = compact ? defaultColumns.filter(c => ['symbol', 'current_price', 'change_pct', 'buy_score', 'signal', 'action'].includes(c.id)) : defaultColumns;

  return (
    <Paper elevation={2} sx={{ overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: 600 }}>
        <Table stickyHeader size="small">
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell key={col.id} align={col.align || 'left'} sx={{ minWidth: col.minWidth, fontWeight: 700, bgcolor: 'background.default' }}>
                  {col.id === 'action' ? (
                    col.label
                  ) : (
                    <TableSortLabel
                      active={orderBy === col.id}
                      direction={orderBy === col.id ? order : 'asc'}
                      onClick={() => col.id !== 'action' && handleSort(col.id as keyof StockData)}>
                      {col.label}
                    </TableSortLabel>
                  )}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {loading && (
              <TableRow>
                <TableCell colSpan={columns.length} align="center" sx={{ py: 4 }}>
                  <Typography variant="body2" color="text.secondary">Loading...</Typography>
                </TableCell>
              </TableRow>
            )}
            {!loading && sorted.length === 0 && (
              <TableRow>
                <TableCell colSpan={columns.length} align="center" sx={{ py: 4 }}>
                  <Typography variant="body2" color="text.secondary">No stocks found</Typography>
                </TableCell>
              </TableRow>
            )}
            {!loading && sorted.map((row) => (
              <TableRow hover key={row.symbol}
                onClick={() => navigate(`/stock/${row.symbol}`)}
                sx={{ cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}>
                {columns.map((col) => (
                  <TableCell key={col.id} align={col.align || 'left'}>
                    {col.format ? col.format(row[col.id as keyof StockData], row) : (row[col.id as keyof StockData] as any) || '—'}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};
