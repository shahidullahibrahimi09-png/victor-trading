"""Asset management service."""

import logging
from typing import List, Optional
from app.data.providers.binance_provider import BinanceProvider

logger = logging.getLogger(__name__)

class AssetService:
    """Service for managing trading assets."""
    
    def __init__(self):
        self.provider = BinanceProvider()
        self._assets_cache = None
    
    async def get_assets(
        self,
        skip: int = 0,
        limit: int = 100,
        asset_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[dict]:
        """Get available assets with optional filtering."""
        try:
            # Get from provider
            assets = await self.provider.get_available_symbols()
            
            if not assets:
                logger.warning("No assets available from provider")
                return []
            
            # Filter by type
            if asset_type:
                assets = [a for a in assets if a.get('asset_type') == asset_type]
            
            # Search by symbol or name
            if search:
                search_lower = search.lower()
                assets = [
                    a for a in assets
                    if search_lower in a.get('symbol', '').lower()
                    or search_lower in a.get('name', '').lower()
                ]
            
            # Apply pagination
            return assets[skip:skip + limit]
        
        except Exception as e:
            logger.error(f"Error getting assets: {e}")
            raise
    
    async def get_asset_by_symbol(self, symbol: str) -> Optional[dict]:
        """Get specific asset by symbol."""
        try:
            assets = await self.provider.get_available_symbols()
            for asset in assets:
                if asset.get('symbol').upper() == symbol.upper():
                    return asset
            return None
        except Exception as e:
            logger.error(f"Error getting asset {symbol}: {e}")
            raise
    
    async def get_assets_by_type(self, asset_type: str) -> List[dict]:
        """Get all assets of specific type."""
        try:
            assets = await self.provider.get_available_symbols()
            return [a for a in assets if a.get('asset_type') == asset_type]
        except Exception as e:
            logger.error(f"Error getting assets by type {asset_type}: {e}")
            raise
    
    async def refresh_assets(self) -> int:
        """Refresh asset list from provider."""
        try:
            assets = await self.provider.get_available_symbols()
            logger.info(f"Refreshed {len(assets)} assets")
            return len(assets)
        except Exception as e:
            logger.error(f"Error refreshing assets: {e}")
            raise
