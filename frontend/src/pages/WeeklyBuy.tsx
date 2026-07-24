import React from 'react';
import { ScreenerPage } from '../components/ScreenerPage';
import { fetchWeeklyBuy } from '../services/api';
export default function WeeklyBuyPage() {
  return <ScreenerPage title="Weekly Buy" icon="📅" subtitle="5–7 day positional setups. Supertrend BUY, ADX 20+, strong score." queryKey="weekly-buy" fetcher={() => fetchWeeklyBuy(30)} />;
}
