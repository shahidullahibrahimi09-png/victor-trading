# VICTOR Trading - Architecture Documentation

## System Architecture Overview

VICTOR is built as a modern, scalable trading analysis platform with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     Mobile Frontend (Flutter)                │
│  - Chart Display    - Asset Selection   - Analysis Results   │
│  - Real-time Updates - UI/UX            - Settings           │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API + WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                   FastAPI Backend Server                    │
├───────────────────────────────────────────────────��────────��┤
│  API Layer          │  Business Logic      │  Data Layer    │
│  - Routes           │  - Analysis Engine   │  - Providers   │
│  - Validation       │  - AI Models         │  - Cache       │
│  - Authentication   │  - Backtesting       │  - Validation  │
│  - WebSocket        │  - Indicators        │  - Storage     │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐      ┌────▼────┐     ┌────▼────┐
   │ Database │      │   Redis  │     │ External │
   │PostgreSQL│      │  Cache   │     │ APIs     │
   └──────────┘      └──────────┘     └──────────┘
        │                                    │
   ┌────▼────────────────────────────────┐  │
   │    Market Data Sources              │  │
   │  - Binance WebSocket/REST           │  │
   │  - Forex APIs (future)              │  │
   │  - Stock APIs (future)              │  │
   └─────────────────────────────────────┘  │
        │                                    │
        └────────────────────────────────────┘
```

## Component Breakdown

### 1. Frontend (Flutter)

**Location**: `frontend/`

**Responsibilities**:
- User interface and charts
- Real-time price display
- User interaction handling
- State management
- API integration

**Key Components**:
- `screens/` - Main UI pages
- `widgets/` - Reusable UI components
- `providers/` - State management (GetX/Provider)
- `services/` - API communication
- `models/` - Data models

### 2. Backend API (FastAPI)

**Location**: `backend/`

**Responsibilities**:
- REST API endpoints
- WebSocket connections
- Request validation
- Authentication/Authorization
- Data retrieval and transformation

**Key Modules**:

#### `app/api/` - API Routes
- `routes/assets.py` - Asset listing and search
- `routes/chart.py` - Chart data endpoints
- `routes/analysis.py` - Analysis endpoints
- `routes/history.py` - Analysis history
- `routes/settings.py` - User settings
- `routes/backtest.py` - Backtesting endpoints
- `routes/websocket.py` - WebSocket handlers

#### `app/services/` - Business Logic
- `analysis_service.py` - Orchestrates analysis
- `chart_service.py` - Chart data management
- `asset_service.py` - Asset management
- `cache_service.py` - Caching layer

#### `app/models/` - Database Models
- `asset.py` - Asset/instrument definitions
- `analysis.py` - Saved analyses
- `user.py` - User accounts
- `settings.py` - User settings
- `prediction.py` - Prediction history

#### `app/schemas/` - Request/Response Validation
- Pydantic models for all endpoints
- Input validation
- Response serialization

### 3. AI Analysis Engine

**Location**: `backend/ai/`

**Responsibilities**:
- Technical analysis
- Pattern recognition
- Signal generation
- Confidence calculation

**Core Modules**:

#### `ai/analysis/`
- `candlestick.py` - Candlestick pattern recognition
- `price_action.py` - Price action analysis
- `trend.py` - Trend analysis
- `structure.py` - Market structure detection
- `analyzer.py` - Main analysis orchestrator

#### `ai/indicators/`
- `moving_averages.py` - SMA, EMA
- `momentum.py` - RSI, Stochastic, Momentum
- `volatility.py` - Bollinger Bands, ATR
- `trend_indicators.py` - MACD, ADX
- `volume.py` - Volume analysis (when available)

#### `ai/models/`
- `signal_model.py` - Main prediction model
- `confidence_scorer.py` - Confidence calculation
- `multi_timeframe.py` - Multi-timeframe analysis

#### `ai/backtesting/`
- `engine.py` - Backtesting framework
- `results.py` - Result calculation and storage
- `metrics.py` - Performance metrics

### 4. Data Layer

**Location**: `backend/data/`

**Responsibilities**:
- Real-time data collection
- Data validation
- Caching
- Connection management

**Key Modules**:

#### `data/providers/`
- `binance_provider.py` - Binance API integration
- `base_provider.py` - Abstract provider interface
- `forex_provider.py` - Forex integration (future)
- `stock_provider.py` - Stock integration (future)

#### `data/websocket/`
- `binance_ws.py` - Binance WebSocket client
- `manager.py` - WebSocket connection management
- `handlers.py` - Message handlers

#### `data/validation.py`
- OHLC data validation
- Timestamp validation
- Missing data detection
- Data integrity checks

### 5. Database Layer

**Location**: `backend/app/database/`

**Responsibilities**:
- PostgreSQL integration
- ORM models
- Migrations
- Query operations

**Key Components**:
- `connection.py` - Database connection pool
- `session.py` - SQLAlchemy session management
- `base.py` - Base model class

### 6. Authentication & Security

**Location**: `backend/app/auth/`

**Responsibilities**:
- JWT token generation/validation
- User authentication
- Permission checks
- Secure password handling

**Key Modules**:
- `jwt_handler.py` - JWT operations
- `security.py` - Password hashing
- `middleware.py` - Auth middleware

## Data Flow

### 1. Chart Data Request Flow

```
Mobile App
    │ GET /api/chart/BTC/USDT?timeframe=1h
    ▼
FastAPI Route Handler
    │ Validate request
    ▼
Chart Service
    │ Check cache (Redis)
    ├─ HIT: Return cached data
    └─ MISS: Get from provider
         ▼
    Data Provider (Binance)
         │ Fetch OHLC data
         ▼
    Data Validation
         │ Verify OHLC integrity
         │ Check timestamps
         │ Detect missing candles
         ▼
    Cache Service (Redis)
         │ Store for 5 minutes
         ▼
    Response to Frontend
```

### 2. Analysis Request Flow

```
Mobile App
    │ POST /api/analyze { asset, timeframe }
    ▼
FastAPI Route Handler
    │ Validate parameters
    ▼
Analysis Service
    ├─ Fetch current chart data
    ├─ Validate data
    ├─ Run AI Analysis:
    │  ├─ Candlestick patterns
    │  ├─ Price action
    │  ├─ Technical indicators
    │  ├─ Trend analysis
    │  ├─ Support/resistance
    │  └─ Multi-timeframe check
    ├─ Calculate confidence
    ├─ Generate signal (UP/DOWN/WAIT)
    ├─ Store result in database
    └─ Return to frontend
```

### 3. Real-Time Price Update Flow

```
Binance WebSocket
    │ Price tick
    ▼
WebSocket Manager
    │ Validate data
    ▼
Cache Service (Redis)
    │ Update latest price
    ▼
WebSocket Broadcast
    │ Push to connected clients
    ▼
Mobile App
    │ Update chart and price display
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Web Server**: Uvicorn
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy
- **Caching**: Redis
- **Real-time**: WebSocket (native FastAPI)
- **Validation**: Pydantic
- **Authentication**: JWT
- **Data Science**: NumPy, Pandas, SciPy
- **Testing**: pytest, pytest-asyncio

### Frontend
- **Framework**: Flutter
- **State Management**: GetX or Provider
- **HTTP Client**: Dio
- **WebSocket**: web_socket_channel
- **Charts**: fl_chart or candlestick_chart
- **Storage**: get_storage or sqflite

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database Migration**: Alembic
- **Environment**: .env configuration

## Key Design Decisions

### 1. No Fake Data
- All chart data comes from real market sources (Binance API)
- No random signal generation
- Analysis only when sufficient data available

### 2. Evidence-Based Analysis
- Confidence calculated from measurable factors
- Each signal backed by technical analysis
- Results stored with reasoning

### 3. Modular Architecture
- AI analysis separated into focused modules
- Easy to test individual components
- Supports future ML model additions

### 4. Real-Time Capability
- WebSocket for live price feeds
- Redis caching for performance
- Background tasks for data updates

### 5. Security First
- API keys on backend only
- JWT authentication for all endpoints
- Input validation on all routes
- CORS configuration

### 6. Scalability
- Horizontal scaling support (stateless API)
- Connection pooling for database
- Redis cluster support
- WebSocket connection management

## Error Handling Strategy

### Data Errors
- Missing market data: Return WAIT state
- Invalid OHLC: Log error, fetch fresh data
- Stale data: Add warning to response
- Connection failure: Auto-retry with exponential backoff

### Analysis Errors
- Insufficient data: Return WAIT with reason
- Calculation errors: Validate inputs, log error
- Model errors: Fallback to simpler analysis

### API Errors
- 400: Invalid request (validation fails)
- 401: Unauthenticated
- 403: Unauthorized
- 404: Resource not found
- 429: Rate limited
- 500: Server error (log and return generic error)

## Performance Considerations

### Caching Strategy
- Chart data: 5 minutes
- Asset list: 1 hour
- Analysis results: No cache (always fresh)
- Price ticks: Real-time via WebSocket

### Database Optimization
- Indexes on frequently queried columns
- Connection pooling
- Query optimization for analysis history

### API Performance
- Response compression
- Pagination for list endpoints
- Selective field loading
- Batch data fetching where possible

## Testing Strategy

### Unit Tests
- Individual indicator calculations
- Pattern recognition logic
- Data validation functions

### Integration Tests
- API endpoint testing
- Database operations
- Cache interactions

### System Tests
- End-to-end workflows
- WebSocket connections
- Error scenarios

### Backtesting
- Historical accuracy measurement
- Performance metrics validation
- Model performance tracking

## Deployment Architecture

### Development
- Docker Compose for local environment
- Auto-reload for development
- Debug logging enabled

### Production
- Kubernetes or Docker Swarm
- Load balancing
- Database replication
- Redis cluster
- Monitoring and logging

## Security Architecture

### Network Security
- HTTPS/WSS for all connections
- CORS configuration
- Rate limiting per IP/user
- DDoS protection

### Data Security
- Encrypted password storage (bcrypt)
- JWT tokens with expiration
- API key isolation (backend only)
- SQL injection prevention (ORM + parameterized queries)

### Application Security
- Input validation on all endpoints
- Output encoding
- CSRF protection
- Dependency scanning

---

**Last Updated**: 2026-08-22
**Version**: 0.1.0
