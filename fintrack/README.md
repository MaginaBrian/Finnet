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
python -m app.seed
python run.py
```

The API listens on `http://localhost:5000`.

Demo login after seeding:

- email: `demo@fintrack.app`
- password: `demo1234`

To use Flask-Migrate instead of `db.create_all()` inside the seed script:

```bash
flask --app run.py db init
flask --app run.py db migrate -m "initial"
flask --app run.py db upgrade
```

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
| GET | `/api/portfolios/<id>` | Portfolio, holdings, and transactions |
| POST | `/api/portfolios/<id>/transactions` | Add a transaction |
| GET | `/api/summary` | Dashboard totals |
