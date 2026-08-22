"""Binance data provider."""

import logging
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class BinanceProvider:
    """Binance API data provider."""
    
    BASE_URL = "https://api.binance.com/api/v3"
    TESTNET_URL = "https://testnet.binance.vision/api/v3"
    
    TIMEFRAME_MAP = {
        "5s": "1s",   # Use 1s and aggregate
        "10s": "1s",
        "15s": "1s",
        "30s": "1s",
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "1h",
        "4h": "4h",
        "1d": "1d"
    }
    
    def __init__(self, testnet: bool = True, api_key: str = None, api_secret: str = None):
        self.testnet = testnet
        self.base_url = self.TESTNET_URL if testnet else self.BASE_URL
        self.api_key = api_key
        self.api_secret = api_secret
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
    
    async def get_available_symbols(self) -> List[Dict[str, Any]]:
        """Get list of available trading pairs."""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/exchangeInfo"
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    logger.error(f"API error {resp.status}")
                    return []
                
                data = await resp.json()
                symbols = data.get('symbols', [])
                
                # Filter trading pairs
                assets = []
                for symbol in symbols:
                    if symbol['status'] == 'TRADING':
                        assets.append({
                            'symbol': f"{symbol['baseAsset']}/{symbol['quoteAsset']}",
                            'name': f"{symbol['baseAsset']} - {symbol['quoteAsset']}",
                            'asset_type': 'crypto',
                            'exchange': 'binance',
                            'base_asset': symbol['baseAsset'],
                            'quote_asset': symbol['quoteAsset']
                        })
                
                logger.info(f"Retrieved {len(assets)} trading symbols")
                return assets[:100]  # Return top 100
        
        except asyncio.TimeoutError:
            logger.error("Timeout fetching exchange info")
            return []
        except Exception as e:
            logger.error(f"Error fetching symbols: {e}")
            return []
    
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get OHLC candle data."""
        try:
            # Normalize symbol
            symbol = symbol.replace('/', '')
            
            # Get Binance timeframe
            binance_tf = self.TIMEFRAME_MAP.get(timeframe, timeframe)
            
            session = await self._get_session()
            url = f"{self.base_url}/klines"
            
            params = {
                'symbol': symbol,
                'interval': binance_tf,
                'limit': min(limit, 1000)
            }
            
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    logger.error(f"API error {resp.status} for {symbol}")
                    return []
                
                data = await resp.json()
                candles = []
                
                for kline in data:
                    candle = {
                        'time': datetime.utcfromtimestamp(kline[0] / 1000),
                        'open': float(kline[1]),
                        'high': float(kline[2]),
                        'low': float(kline[3]),
                        'close': float(kline[4]),
                        'volume': float(kline[7])
                    }
                    candles.append(candle)
                
                logger.info(f"Retrieved {len(candles)} candles for {symbol}")
                return candles
        
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching candles for {symbol}")
            return []
        except Exception as e:
            logger.error(f"Error fetching candles: {e}")
            return []
    
    async def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol."""
        try:
            symbol = symbol.replace('/', '')
            session = await self._get_session()
            url = f"{self.base_url}/ticker/price"
            
            params = {'symbol': symbol}
            
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status != 200:
                    logger.error(f"API error {resp.status}")
                    return None
                
                data = await resp.json()
                return float(data.get('price', 0))
        
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            return None
    
    async def get_24h_stats(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get 24-hour statistics for a symbol."""
        try:
            symbol = symbol.replace('/', '')
            session = await self._get_session()
            url = f"{self.base_url}/ticker/24hr"
            
            params = {'symbol': symbol}
            
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status != 200:
                    logger.error(f"API error {resp.status}")
                    return None
                
                data = await resp.json()
                return {
                    'price_change': float(data.get('priceChange', 0)),
                    'price_change_percent': float(data.get('priceChangePercent', 0)),
                    'high_price': float(data.get('highPrice', 0)),
                    'low_price': float(data.get('lowPrice', 0)),
                    'quote_asset_volume': float(data.get('quoteAssetVolume', 0))
                }
        
        except Exception as e:
            logger.error(f"Error fetching 24h stats: {e}")
            return None
