# Fintrack

Personal portfolio tracker. A Flask API stores users, portfolios, and transactions. A React client shows balances, holdings, and a transaction log.

## Layout

```
fintrack/
├── backend/     Flask API, SQLAlchemy models, services, and tests
└── frontend/    React + Vite client
```

Holdings are valued at cost. Buy and sell transactions update share quantity and cash. Deposits, withdrawals, and dividends update cash only.

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app wsgi db upgrade
flask --app wsgi seed-demo
python run.py
```

The API listens on `http://localhost:5000`. Production uses `./start.sh`, which migrates, seeds when `SEED_DEMO=true`, and serves with gunicorn on port 8000.

Demo login after seeding (`DEMO_USERNAME=demo`):

- username: `demo`
- password: `Demo@12345`

Tests:

```bash
pytest
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server runs at `http://localhost:5173` and proxies `/api` to the Flask app.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/auth/register` | Create an account |
| POST | `/api/auth/login` | Sign in |
| GET | `/api/auth/me` | Current user |
| GET | `/api/portfolios` | List portfolios |
| POST | `/api/portfolios` | Create a portfolio |
| GET | `/api/portfolios/<id>` | Portfolio and totals |
| GET | `/api/portfolios/<id>/summary` | Holdings and profit or loss |
| GET | `/api/portfolios/<id>/transactions` | Paginated trades |
| POST | `/api/portfolios/<id>/transactions` | Add a trade |
| DELETE | `/api/transactions/<id>` | Remove a trade |
