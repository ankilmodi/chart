import React from 'react';
import { ScreenerPage } from '../components/ScreenerPage';
import { fetchSwingBuy } from '../services/api';
export default function SwingBuyPage() {
  return <ScreenerPage title="Swing Buy" icon="📈" subtitle="2–5 day swing trade setups. Uptrend confirmed, RSI 50+, volume expanding." queryKey="swing-buy" fetcher={() => fetchSwingBuy(30)} />;
}
