import React from 'react';
import { ScreenerPage } from '../components/ScreenerPage';
import { fetchTopBuy } from '../services/api';
export default function TopBuyPage() {
  return (
    <ScreenerPage
      title="Top Buy Today"
      icon="🔥"
      subtitle="Stocks with Buy Score ≥ 76, strong EMA trend, bullish MACD, RSI in ideal zone and high volume."
      queryKey="top-buy"
      fetcher={() => fetchTopBuy(30)}
    />
  );
}
