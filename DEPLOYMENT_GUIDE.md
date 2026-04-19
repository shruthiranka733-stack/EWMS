# EWMS Deployment Guide

## Prerequisites
- PostgreSQL 14+
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose (optional)

---

## Local Development

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:3000/dashboard

---

## Docker (one command)
```bash
cd backend
docker-compose up
```

Services started:
- PostgreSQL on port 5432
- API on port 8000 → http://localhost:8000/api/docs
- Frontend on port 3000 → http://localhost:3000

---

## Run Tests
```bash
cd backend
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

---

## Production Deployment

### Backend (Railway / Fly.io / AWS ECS)
```bash
# Build image
docker build -t ewms-api .

# Set env vars on your platform:
# DATABASE_URL, ENVIRONMENT=production, JWT_SECRET

# Deploy
docker push your-registry/ewms-api:latest
```

### Frontend (Vercel)
```bash
cd frontend
npm run build
npx vercel deploy --prod
# Set NEXT_PUBLIC_API_URL to your backend URL
```

### Database (Supabase / AWS RDS)
```bash
# After provisioning, run migrations:
alembic upgrade head

# Seed initial data (optional):
python scripts/seed_dev_data.py
```
