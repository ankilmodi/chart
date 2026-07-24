import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box, Drawer, AppBar, Toolbar, Typography, IconButton,
  List, ListItemButton, ListItemIcon, ListItemText,
  Collapse, Divider, Badge, Chip, Tooltip, useTheme, useMediaQuery,
} from '@mui/material';
import {
  Menu as MenuIcon, Dashboard, ShowChart, GridView, Star,
  TrendingUp, DateRange, Bolt, Speed, Equalizer,
  VolumeUp, Addchart, SwapVert, BarChart, School,
  Bookmarks, AccountBalance, Settings, Notifications,
  WbSunny, DarkMode, ExpandLess, ExpandMore, Refresh,
  Analytics, FilterList,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { fetchMarketOverview, fetchNotifications } from '../services/api';
import { useAppSelector, useAppDispatch } from '../store/hooks';
import { markAllRead } from '../store';

const DRAWER_W = 240;

interface NavItem {
  label: string;
  path?: string;
  icon: React.ReactNode;
  children?: NavItem[];
  badge?: number;
}

interface LayoutProps {
  children: React.ReactNode;
  themeMode: 'dark' | 'light';
  onToggleTheme: () => void;
}

export const Layout: React.FC<LayoutProps> = ({ children, themeMode, onToggleTheme }) => {
  const theme    = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const [mobileOpen,   setMobileOpen]   = useState(false);
  const [openScreener, setOpenScreener] = useState(true);
  const [openOI,       setOpenOI]       = useState(false);

  const unread = useAppSelector(s => s.notifications.unread);

  const { data: market } = useQuery({
    queryKey: ['market-overview'],
    queryFn: fetchMarketOverview,
    refetchInterval: 60_000,
  });

  const nav = (path: string) => {
    navigate(path);
    if (isMobile) setMobileOpen(false);
  };

  const isActive = (path: string) => location.pathname === path;

  const itemSx = (path: string) => ({
    borderRadius: 1,
    mx: 0.5,
    mb: 0.3,
    bgcolor: isActive(path) ? 'primary.main' : 'transparent',
    color:   isActive(path) ? 'primary.contrastText' : 'inherit',
    '&:hover': { bgcolor: isActive(path) ? 'primary.dark' : 'action.hover' },
  });

  const DrawerContent = (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Logo */}
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
        <Analytics sx={{ color: 'primary.main', fontSize: 28 }} />
        <Box>
          <Typography variant="subtitle1" fontWeight={700} lineHeight={1.2}>
            Nifty F&O
          </Typography>
          <Typography variant="caption" color="text.secondary">
            AI Stock Analyzer
          </Typography>
        </Box>
      </Box>

      {/* Market status bar */}
      {market && (
        <Box sx={{ px: 2, pb: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="caption" color="text.secondary">NIFTY</Typography>
            <Chip
              label={market.market_trend?.toUpperCase()}
              size="small"
              color={market.market_trend === 'bullish' ? 'success' : market.market_trend === 'bearish' ? 'error' : 'warning'}
              sx={{ height: 18, fontSize: 10 }}
            />
          </Box>
          <Typography variant="body2" fontWeight={700}>
            {market.nifty_price?.toLocaleString('en-IN', { maximumFractionDigits: 0 }) ?? '—'}
            {market.nifty_change_pct != null && (
              <Typography component="span" variant="caption"
                color={market.nifty_change_pct >= 0 ? 'success.main' : 'error.main'} ml={0.5}>
                ({market.nifty_change_pct >= 0 ? '+' : ''}{market.nifty_change_pct?.toFixed(2)}%)
              </Typography>
            )}
          </Typography>
          {market.vix && (
            <Typography variant="caption" color={market.vix_safe ? 'success.main' : 'error.main'}>
              VIX: {market.vix?.toFixed(1)}
            </Typography>
          )}
        </Box>
      )}

      <Divider />

      <List dense sx={{ flex: 1, overflowY: 'auto', pt: 1 }}>
        {/* Main */}
        <ListItemButton sx={itemSx('/')} onClick={() => nav('/')}>
          <ListItemIcon sx={{ minWidth: 36, color: 'inherit' }}><Dashboard fontSize="small" /></ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItemButton>

        <ListItemButton sx={itemSx('/future-stocks')} onClick={() => nav('/future-stocks')}>
          <ListItemIcon sx={{ minWidth: 36, color: 'inherit' }}><GridView fontSize="small" /></ListItemIcon>
          <ListItemText primary="F&O Stocks Table" />
        </ListItemButton>

        <ListItemButton sx={itemSx('/heatmap')} onClick={() => nav('/heatmap')}>
          <ListItemIcon sx={{ minWidth: 36, color: 'inherit' }}><GridView fontSize="small" /></ListItemIcon>
          <ListItemText primary="Heat Map" />
        </ListItemButton>

        <Divider sx={{ my: 0.5 }} />

        {/* Screeners group */}
        <ListItemButton onClick={() => setOpenScreener(!openScreener)} sx={{ borderRadius: 1, mx: 0.5 }}>
          <ListItemIcon sx={{ minWidth: 36 }}><FilterList fontSize="small" /></ListItemIcon>
          <ListItemText primary="Screeners" primaryTypographyProps={{ fontWeight: 600, fontSize: 13 }} />
          {openScreener ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />}
        </ListItemButton>
        <Collapse in={openScreener} timeout="auto">
          <List dense disablePadding sx={{ pl: 1 }}>
            {[
              { label: 'Top Buy Today',   path: '/top-buy',        icon: <Star fontSize="small" /> },
              { label: 'Swing Buy',       path: '/swing-buy',      icon: <TrendingUp fontSize="small" /> },
              { label: 'Weekly Buy',      path: '/weekly-buy',     icon: <DateRange fontSize="small" /> },
              { label: 'Breakout Stocks', path: '/breakout',       icon: <Bolt fontSize="small" /> },
              { label: 'Momentum',        path: '/momentum',       icon: <Speed fontSize="small" /> },
              { label: 'EMA Screener',    path: '/ema-screener',   icon: <ShowChart fontSize="small" /> },
              { label: 'Volume Shockers', path: '/volume-shockers',icon: <VolumeUp fontSize="small" /> },
            ].map(item => (
              <ListItemButton key={item.path} sx={itemSx(item.path)} onClick={() => nav(item.path)}>
                <ListItemIcon sx={{ minWidth: 32, color: 'inherit' }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} primaryTypographyProps={{ fontSize: 13 }} />
              </ListItemButton>
            ))}
          </List>
        </Collapse>

        <Divider sx={{ my: 0.5 }} />

        {/* OI group */}
        <ListItemButton onClick={() => setOpenOI(!openOI)} sx={{ borderRadius: 1, mx: 0.5 }}>
          <ListItemIcon sx={{ minWidth: 36 }}><BarChart fontSize="small" /></ListItemIcon>
          <ListItemText primary="OI Analysis" primaryTypographyProps={{ fontWeight: 600, fontSize: 13 }} />
          {openOI ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />}
        </ListItemButton>
        <Collapse in={openOI} timeout="auto">
          <List dense disablePadding sx={{ pl: 1 }}>
            {[
              { label: 'Long Build-up',   path: '/long-buildup',   icon: <Addchart fontSize="small" /> },
              { label: 'Short Covering',  path: '/short-covering', icon: <SwapVert fontSize="small" /> },
              { label: 'OI Analysis',     path: '/oi-analysis',    icon: <Equalizer fontSize="small" /> },
            ].map(item => (
              <ListItemButton key={item.path} sx={itemSx(item.path)} onClick={() => nav(item.path)}>
                <ListItemIcon sx={{ minWidth: 32, color: 'inherit' }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} primaryTypographyProps={{ fontSize: 13 }} />
              </ListItemButton>
            ))}
          </List>
        </Collapse>

        <Divider sx={{ my: 0.5 }} />

        {/* Other pages */}
        {[
          { label: 'Formula & Calc',   path: '/formula',     icon: <School fontSize="small" /> },
          { label: 'Watchlist',        path: '/watchlist',   icon: <Bookmarks fontSize="small" /> },
          { label: 'Portfolio',        path: '/portfolio',   icon: <AccountBalance fontSize="small" /> },
          { label: 'Full Scanner',     path: '/scanner',     icon: <Analytics fontSize="small" /> },
          { label: 'Settings',         path: '/settings',    icon: <Settings fontSize="small" /> },
        ].map(item => (
          <ListItemButton key={item.path} sx={itemSx(item.path)} onClick={() => nav(item.path)}>
            <ListItemIcon sx={{ minWidth: 36, color: 'inherit' }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>

      <Divider />
      <Box sx={{ p: 1, textAlign: 'center' }}>
        <Typography variant="caption" color="text.disabled">v2.0 • NSE F&O Only</Typography>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {/* App Bar */}
      <AppBar position="fixed" elevation={0}
        sx={{ zIndex: theme.zIndex.drawer + 1, borderBottom: 1, borderColor: 'divider',
              bgcolor: 'background.paper', color: 'text.primary' }}>
        <Toolbar variant="dense">
          <IconButton edge="start" onClick={() => setMobileOpen(!mobileOpen)} sx={{ mr: 1 }}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" fontWeight={700} sx={{ flexGrow: 1, fontSize: 16 }}>
            🚀 Nifty F&O AI Analyzer
          </Typography>

          {market && (
            <Box sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center', gap: 2, mr: 2 }}>
              <Box textAlign="right">
                <Typography variant="caption" color="text.secondary">NIFTY</Typography>
                <Typography variant="body2" fontWeight={700}>
                  {market.nifty_price?.toLocaleString('en-IN', { maximumFractionDigits: 0 }) ?? '—'}
                </Typography>
              </Box>
              {market.vix && (
                <Chip label={`VIX ${market.vix.toFixed(1)}`} size="small"
                  color={market.vix_safe ? 'success' : 'error'} />
              )}
              <Chip
                label={market.market_trend?.toUpperCase()}
                size="small"
                color={market.market_trend === 'bullish' ? 'success' : market.market_trend === 'bearish' ? 'error' : 'warning'}
              />
            </Box>
          )}

          <Tooltip title="Notifications">
            <IconButton onClick={() => { navigate('/watchlist'); dispatch(markAllRead()); }}>
              <Badge badgeContent={unread} color="error">
                <Notifications fontSize="small" />
              </Badge>
            </IconButton>
          </Tooltip>

          <Tooltip title={themeMode === 'dark' ? 'Light mode' : 'Dark mode'}>
            <IconButton onClick={onToggleTheme}>
              {themeMode === 'dark' ? <WbSunny fontSize="small" /> : <DarkMode fontSize="small" />}
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>

      {/* Sidebar – desktop */}
      <Drawer variant="permanent"
        sx={{ width: DRAWER_W, flexShrink: 0, display: { xs: 'none', md: 'block' },
              '& .MuiDrawer-paper': { width: DRAWER_W, boxSizing: 'border-box', mt: '48px' } }}>
        {DrawerContent}
      </Drawer>

      {/* Sidebar – mobile */}
      <Drawer variant="temporary" open={mobileOpen} onClose={() => setMobileOpen(false)}
        sx={{ display: { xs: 'block', md: 'none' },
              '& .MuiDrawer-paper': { width: DRAWER_W } }}>
        {DrawerContent}
      </Drawer>

      {/* Main content */}
      <Box component="main"
        sx={{ flexGrow: 1, mt: '48px', ml: { md: `${DRAWER_W}px` }, minWidth: 0 }}>
        {children}
      </Box>
    </Box>
  );
};
