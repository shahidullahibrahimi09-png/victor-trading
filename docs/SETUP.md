# VICTOR Trading - Setup Instructions

## Prerequisites

Before starting, ensure you have:

- **Git** - Version control
- **Docker & Docker Compose** - Recommended for easy setup
- **Python 3.10+** - For backend development (manual setup)
- **Flutter SDK** - For mobile app development
- **PostgreSQL 14+** - If running without Docker
- **Redis 7+** - If running without Docker

## Quick Start with Docker (Recommended)

The easiest way to get VICTOR running locally.

### 1. Clone the Repository

```bash
git clone https://github.com/shahidullahibrahimi09-png/victor-trading.git
cd victor-trading
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and update:
- `BINANCE_API_KEY` and `BINANCE_API_SECRET` (or leave as is for public data only)
- `SECRET_KEY` and `JWT_SECRET_KEY` (generate new random strings)
- Other configurations as needed

### 3. Start the Stack

```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Redis cache
- FastAPI backend server

### 4. Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### 5. Verify Services

```bash
# Check all services are running
docker-compose ps

# Backend API should be available at: http://localhost:8000
# API Documentation: http://localhost:8000/docs
# Database: localhost:5432 (user: victor, password: victor_password)
# Redis: localhost:6379
```

### 6. Build and Run Frontend

```bash
cd frontend
flutter pub get
flutter run
```

## Manual Backend Setup (Development)

If you prefer to run the backend directly without Docker.

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Database

Ensure PostgreSQL is running locally. Create the database:

```bash
psql -U postgres
CREATE DATABASE victor_db;
CREATE USER victor WITH PASSWORD 'victor_password';
ALTER ROLE victor SET client_encoding TO 'utf8';
ALTER ROLE victor SET default_transaction_isolation TO 'read committed';
ALTER ROLE victor SET default_transaction_deferrable TO on;
ALTER ROLE victor SET default_transaction_deferrable TO off;
GRANT ALL PRIVILEGES ON DATABASE victor_db TO victor;
\q
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`

## Manual Frontend Setup

### 1. Install Flutter

Follow the [official Flutter installation guide](https://flutter.dev/docs/get-started/install)

### 2. Get Dependencies

```bash
cd frontend
flutter pub get
```

### 3. Run on Emulator

```bash
# Start emulator
emulator @Pixel_4

# Run app
flutter run
```

### 4. Run on Physical Device

```bash
# Enable USB debugging on device
# Connect device via USB
flutter run
```

### 5. Build Release

```bash
# Android
flutter build apk

# iOS
flutter build ios
```

## Configuration

### Backend Configuration (`.env`)

Key environment variables:

| Variable | Description | Default |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | postgres://victor:password@localhost/victor_db |
| `REDIS_URL` | Redis connection string | redis://localhost:6379/0 |
| `BINANCE_API_KEY` | Binance API key | (empty - uses public endpoints) |
| `BINANCE_API_SECRET` | Binance API secret | (empty) |
| `BINANCE_TESTNET` | Use Binance testnet | True |
| `SECRET_KEY` | Flask/FastAPI secret key | (must set for production) |
| `JWT_SECRET_KEY` | JWT signing key | (must set for production) |
| `DEBUG` | Debug mode | False |
| `LOG_LEVEL` | Logging level | INFO |

### Binance API Setup (Optional)

To use private Binance endpoints for live trading:

1. Create Binance account at https://www.binance.com
2. Enable 2FA
3. Go to API Management
4. Create new API key
5. Set permissions: Read-only recommended
6. Add your API key and secret to `.env`

## Database Initialization

When starting fresh, the database needs to be initialized:

```bash
# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head

# View current revision
alembic current

# Downgrade to previous revision
alembic downgrade -1
```

## Verification Checklist

After setup, verify everything is working:

- [ ] Docker containers running: `docker-compose ps`
- [ ] Backend API responds: `curl http://localhost:8000/api/health`
- [ ] API docs available: http://localhost:8000/docs
- [ ] Database connected: Check logs in Docker or console
- [ ] Redis connected: Check logs
- [ ] Frontend builds: `flutter build apk --release` (no errors)
- [ ] Can fetch assets: `curl http://localhost:8000/api/assets`

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
psql -U victor -d victor_db -c "SELECT 1"

# View database logs
docker-compose logs postgres

# Reset database (⚠️ deletes all data)
docker-compose down postgres
docker volume rm victor-trading_postgres_data
docker-compose up -d postgres
```

### Backend Service Issues

```bash
# View backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Manual backend test (without Docker)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Redis Connection Issues

```bash
# Check Redis is running
redis-cli ping

# View Redis logs
docker-compose logs redis

# Clear Redis cache
redis-cli FLUSHALL
```

### Flutter Issues

```bash
# Get Flutter info
flutter doctor

# Clean build
flutter clean
flutter pub get
flutter run

# Run with verbose logging
flutter run -v
```

## Development Workflow

### Backend Development

1. Make code changes in `backend/`
2. Changes auto-reload with `--reload` flag
3. Check logs: `docker-compose logs backend -f`
4. Run tests: `pytest tests/`

### Frontend Development

1. Make code changes in `frontend/`
2. Changes auto-reload with hot reload
3. Test on device: `flutter run`

### Database Changes

1. Modify SQLAlchemy models in `backend/app/models/`
2. Create migration: `alembic revision --autogenerate -m "Description"`
3. Review migration in `backend/alembic/versions/`
4. Apply migration: `alembic upgrade head`

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_indicators.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Frontend Tests

```bash
cd frontend
flutter test
flutter test --coverage
```

## Production Deployment

### Before Deploying

1. Update version in `README.md` and `docs/`
2. Review all `.env` variables for production values
3. Run full test suite: `pytest` and `flutter test`
4. Test database migrations: `alembic upgrade head`
5. Build production app: `flutter build apk --release`

### Deployment Steps

1. Build Docker images: `docker-compose build`
2. Push to registry: `docker push your-registry/victor-backend:latest`
3. Deploy to Kubernetes/Docker Swarm
4. Run migrations: `kubectl exec -it deployment/victor-backend -- alembic upgrade head`
5. Verify health: `curl https://api.victor-trading.com/api/health`

## Support & Documentation

- API Documentation: http://localhost:8000/docs (interactive Swagger UI)
- Architecture Guide: See `docs/ARCHITECTURE.md`
- Analysis Guide: See `docs/ANALYSIS.md`
- API Reference: See `docs/API.md`

## Next Steps

After setup:

1. Explore the API: http://localhost:8000/docs
2. Test with sample data: Fetch assets and chart data
3. Run analysis on different assets/timeframes
4. Check analysis history
5. Review backtesting results
6. Configure settings

---

**Last Updated**: 2026-08-22
**Version**: 0.1.0
