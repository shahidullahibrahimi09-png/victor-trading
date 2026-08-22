# VICTOR Trading - Professional AI-Powered Chart Analysis Platform

A serious, professional AI-powered trading chart analysis application built with real-time market data, advanced technical analysis, and machine learning capabilities.

## 🎯 Key Features

### Professional Trading Chart
- **Interactive Candlestick Charts** - Real OHLC data with zoom, scroll, and price levels
- **Real-Time Updates** - Live market data with connection monitoring
- **Technical Indicators** - RSI, MACD, Bollinger Bands, Moving Averages, Stochastic, ATR
- **Chart Tools** - Support and resistance lines, trend analysis, breakout detection

### Market Data & Assets
- **Multi-Asset Support** - Crypto, Forex, Stocks, Commodities (from real data sources)
- **Multiple Timeframes** - 5s, 10s, 15s, 30s, 1m, 5m, 15m, 30m, 1h, 4h, 1d
- **Real Data Integration** - WebSocket and REST API from legitimate market data providers
- **Data Validation** - Timestamp validation, missing data detection, stale data warnings

### AI Analysis Engine
- **Candlestick Pattern Recognition** - Doji, Hammer, Engulfing, Morning/Evening Star, etc.
- **Price Action Analysis** - Support/Resistance, Breakouts, Pullbacks, Reversals
- **Trend Analysis** - Higher Highs/Lows, Market Structure, Break of Structure
- **Multi-Timeframe Analysis** - Correlation across different timeframes
- **Confidence Calculation** - Evidence-based scoring from measurable factors

### Signal System
- **Clear Predictions** - UP / DOWN / WAIT with confidence percentages
- **Detailed Analysis** - Reasons, supporting indicators, risk levels
- **No Fake Data** - Real analysis or WAIT state only

### Backtesting & History
- **Historical Backtesting** - Test AI against historical market data
- **Analysis History** - Track predictions vs actual outcomes
- **Performance Metrics** - Accuracy, win rate, P&L simulation
- **Model Versioning** - Track AI model improvements over time

### Professional UI
- **Dark Trading Interface** - Modern, responsive design
- **Real-Time Price Updates** - Current market status and direction
- **Smooth Animations** - Professional feel without performance impact
- **Settings & Customization** - Theme, indicators, notifications, data sources

## 🏗️ Architecture

```
victor-trading/
├── frontend/                 # Flutter mobile app
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/         # UI screens
│   │   ├── widgets/         # Reusable components
│   │   ├── models/          # Data models
│   │   ├── providers/       # State management
│   │   └── services/        # API integration
│   └── pubspec.yaml
│
├── backend/                  # Python FastAPI server
│   ├── app/
│   │   ├── main.py
│   │   ├── api/             # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Request/response schemas
│   │   ├── database/        # PostgreSQL integration
│   │   ├── auth/            # Authentication
│   │   └── config.py        # Configuration
│   ├── ai/                  # AI/ML modules
│   │   ├── analysis/        # Technical analysis
│   │   ├── indicators/      # Indicator calculations
│   │   ├── patterns/        # Candlestick patterns
│   │   ├── models/          # ML models
│   │   └── backtesting/     # Backtesting engine
│   ├── data/                # Data collection & validation
│   │   ├���─ providers/       # Market data sources
│   │   ├── websocket/       # WebSocket clients
│   │   └── validation.py    # Data validation
│   ├── requirements.txt
│   └── .env.example
│
├── database/                # Database schemas
│   ├── migrations/
│   └── schema.sql
│
├── docs/                    # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   └── ANALYSIS.md
│
└── docker-compose.yml       # Local development stack
```

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.10+ (for backend development)
- Flutter SDK (for mobile development)
- PostgreSQL 14+
- Git

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/shahidullahibrahimi09-png/victor-trading.git
cd victor-trading

# Start the development environment
docker-compose up -d

# The application will be available at:
# Backend API: http://localhost:8000
# Database: localhost:5432
# WebSocket: ws://localhost:8000/ws
```

### Backend Setup (Manual)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Get dependencies
flutter pub get

# Run on device/emulator
flutter run

# Build release
flutter build apk    # Android
flutter build ios    # iOS
```

## 📊 Analysis Engine

### Supported Technical Indicators
- Moving Averages (SMA, EMA)
- Relative Strength Index (RSI)
- MACD
- Bollinger Bands
- Stochastic
- Average True Range (ATR)
- Volume (when available)
- Momentum
- Volatility Analysis

### Analysis Process
1. **Data Validation** - Verify OHLC data integrity
2. **Candlestick Analysis** - Pattern recognition
3. **Price Action** - Support/resistance, structure
4. **Indicator Analysis** - Multi-indicator confirmation
5. **Trend Analysis** - Market direction and structure
6. **Risk Assessment** - Volatility and position sizing
7. **Confidence Calculation** - Evidence-based scoring
8. **AI Synthesis** - Combine all factors for final signal

### Confidence System
Confidence is calculated from measurable factors:
- Trend confirmation
- Candlestick pattern strength
- Momentum signals
- Support/resistance validation
- Indicator alignment
- Multi-timeframe confirmation
- Historical model performance
- Volatility conditions

**No random percentages. No guaranteed predictions.**

## 🔄 Real-Time Data

Supported data sources:
- Binance (Crypto) - WebSocket + REST
- Forex APIs (when integrated)
- Stock market APIs (when integrated)
- Custom data providers

Data features:
- Real-time price updates
- OHLC candle data
- Volume when available
- Connection monitoring
- Automatic reconnection
- Timestamp validation
- Missing data detection

## 📈 Backtesting

Test AI signals against historical data:

```python
from ai.backtesting import BacktestEngine

engine = BacktestEngine()
results = engine.backtest(
    asset="BTC/USDT",
    timeframe="1h",
    start_date="2023-01-01",
    end_date="2024-01-01"
)

print(f"Total Predictions: {results.total}")
print(f"Accuracy: {results.accuracy}%")
print(f"Win Rate: {results.win_rate}%")
```

## 🔐 Security

- API keys stored securely on backend only
- Authentication & authorization
- Secure WebSocket connections
- Input validation on all endpoints
- Rate limiting
- No sensitive data in mobile app

## 📝 API Documentation

Full API documentation available at `/docs` when backend is running.

Key endpoints:
- `GET /api/assets` - Available trading instruments
- `GET /api/chart/{asset}/{timeframe}` - Historical candle data
- `POST /api/analyze` - Run AI analysis
- `GET /api/history` - Previous analyses
- `WS /ws` - Real-time price feed

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
flutter test
```

## 🤝 Contributing

This is a professional trading application. Any contributions should:
1. Maintain data integrity and accuracy
2. Never generate fake data or random signals
3. Include proper testing
4. Follow the existing architecture
5. Document changes thoroughly

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

VICTOR is an analysis tool for educational and research purposes. It does NOT guarantee profitable trading. Always conduct your own research and risk assessment before making trading decisions. Past performance does not indicate future results.

## 📞 Support

For issues, questions, or feature requests, please open a GitHub issue.

---

**Status**: 🚀 Active Development

**Last Updated**: 2026-08-22

**Version**: 0.1.0-alpha
