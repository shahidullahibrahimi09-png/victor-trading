"""Analysis orchestration service."""

import logging
from typing import Optional, Dict, Any
from app.ai.analyzer import Analyzer
from app.services.chart_service import ChartService

logger = logging.getLogger(__name__)

class AnalysisService:
    """Service for running AI analysis."""
    
    def __init__(self):
        self.analyzer = Analyzer()
        self.chart_service = ChartService()
    
    async def analyze(
        self,
        symbol: str,
        timeframe: str,
        include_history: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Run comprehensive AI analysis."""
        try:
            logger.info(f"Starting analysis for {symbol} {timeframe}")
            
            # Get chart data
            chart_data = await self.chart_service.get_chart_data(
                symbol=symbol,
                timeframe=timeframe,
                limit=200
            )
            
            if not chart_data or not chart_data.get('candles'):
                logger.warning(f"Insufficient data for analysis: {symbol}")
                return None
            
            # Run analysis
            analysis_result = await self.analyzer.analyze(
                symbol=symbol,
                timeframe=timeframe,
                candles=chart_data['candles'],
                current_price=chart_data['current_price']
            )
            
            if not analysis_result:
                logger.warning(f"Analysis returned no result for {symbol}")
                return None
            
            return analysis_result
        
        except Exception as e:
            logger.error(f"Analysis error: {e}", exc_info=True)
            raise
    
    async def quick_analyze(
        self,
        symbol: str,
        timeframe: str
    ) -> Optional[Dict[str, Any]]:
        """Run fast 5-second analysis."""
        try:
            # Get latest data only
            chart_data = await self.chart_service.get_chart_data(
                symbol=symbol,
                timeframe=timeframe,
                limit=50
            )
            
            if not chart_data:
                return None
            
            # Quick analysis
            result = await self.analyzer.quick_analyze(
                symbol=symbol,
                candles=chart_data['candles'],
                current_price=chart_data['current_price']
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Quick analysis error: {e}")
            raise
    
    async def store_analysis(self, analysis_data: Dict[str, Any]) -> None:
        """Store analysis result in database."""
        try:
            # This would be implemented with database storage
            logger.info(f"Storing analysis for {analysis_data.get('symbol')}")
        except Exception as e:
            logger.error(f"Error storing analysis: {e}")
