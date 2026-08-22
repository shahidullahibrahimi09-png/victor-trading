"""Chart data service."""

import logging
from typing import Optional
from app.data.providers.binance_provider import BinanceProvider
from app.data.validation import validate_ohlc_data

logger = logging.getLogger(__name__)

class ChartService:
    """Service for retrieving and managing chart data."""
    
    def __init__(self):
        self.provider = BinanceProvider()
    
    async def get_chart_data(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 100
    ) -> Optional[dict]:
        """Get chart data for an asset."""
        try:
            # Fetch OHLC data from provider
            candles = await self.provider.get_candles(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit
            )
            
            if not candles:
                logger.warning(f"No candle data for {symbol} {timeframe}")
                return None
            
            # Validate data
            is_valid = validate_ohlc_data(candles)
            if not is_valid:
                logger.error(f"Invalid OHLC data for {symbol}")
                return None
            
            # Get current price
            current_price = await self.provider.get_current_price(symbol)
            
            # Format response
            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "candles": candles,
                "current_price": current_price,
                "previous_close": candles[-2]['close'] if len(candles) > 1 else None,
                "price_change": current_price - candles[-1]['close'] if candles else None,
                "price_change_percent": (
                    ((current_price - candles[-1]['close']) / candles[-1]['close'] * 100)
                    if candles and candles[-1]['close'] > 0 else None
                ),
                "timestamp": candles[-1]['time'] if candles else None,
                "data_source": "binance",
                "is_real_time": True
            }
        
        except Exception as e:
            logger.error(f"Error getting chart data for {symbol}: {e}")
            raise
    
    async def get_latest_candle(self, symbol: str, timeframe: str) -> Optional[dict]:
        """Get the latest candle for an asset."""
        try:
            candles = await self.provider.get_candles(
                symbol=symbol,
                timeframe=timeframe,
                limit=1
            )
            return candles[0] if candles else None
        except Exception as e:
            logger.error(f"Error getting latest candle for {symbol}: {e}")
            raise
    
    async def get_asset_info(self, symbol: str) -> Optional[dict]:
        """Get current asset information."""
        try:
            current_price = await self.provider.get_current_price(symbol)
            
            if current_price is None:
                return None
            
            # Get 24h stats
            stats = await self.provider.get_24h_stats(symbol)
            
            return {
                "symbol": symbol,
                "current_price": current_price,
                "24h_change": stats.get('price_change') if stats else None,
                "24h_change_percent": stats.get('price_change_percent') if stats else None,
                "24h_high": stats.get('high_price') if stats else None,
                "24h_low": stats.get('low_price') if stats else None,
                "24h_volume": stats.get('quote_asset_volume') if stats else None,
            }
        except Exception as e:
            logger.error(f"Error getting asset info for {symbol}: {e}")
            raise
