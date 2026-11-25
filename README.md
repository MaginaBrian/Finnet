# FinTrack

Portfolio and transactions tracker by Finnet Technologies, part of Finnet Group.

An analyst signs in, keeps client portfolios in KES or USD, records buys and sells, and sees current holdings, profit and loss, and how value is split across instruments. The React app reads and writes only through the Flask API. Every client name and price in the demo data is fictional.

## Run it

Demo login after seeding: **demo** / **Demo@12345**.

Three portfolios are created: Growth Equities (Baraka Holdings Ltd, KES), Treasury Ladder (Kilima Pension Scheme, KES), and Offshore Income (Savannah Foundation, USD).

### On your machine

API:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app wsgi db upgrade
flask --app wsgi seed-demo
flask --app wsgi run --port 5000
```

Frontend, in a second terminal:

```bash
cd frontend
cp .env.example .env
npm ci
npm run dev
```

- App: http://localhost:5173
- API: http://localhost:5000
- Swagger UI: http://localhost:5000/api/docs
- OpenAPI file: http://localhost:5000/api/openapi.yaml

The browser calls the API directly. `VITE_API_URL` is the API origin with no trailing slash, and `CORS_ORIGINS` must list the exact page origin (`http://localhost:5173` in the examples).

`SEED_DEMO=true` loads the demo analyst only when the process starts through `backend/start.sh` (Docker and Render). A local `flask run` does not seed by itself, which is why the commands above include `seed-demo`.

### Docker Compose

From the repository root:

```bash
docker compose up --build
```

Postgres 16, the API, and the built frontend come up together. The API is published on port 5000 (gunicorn listens on 8000 inside the container). The site is published on port 5173. The frontend image is built with `VITE_API_URL=http://localhost:5000`, and the API allows `http://localhost:5173`.

## Architecture

```
Browser (React)  -- JSON, Bearer JWT -->  Flask API  -->  SQLAlchemy  -->  SQLite or PostgreSQL
```

| Path | Role |
| --- | --- |
| `backend/app/api` | HTTP routes for auth, portfolios, transactions, health, and Swagger |
| `backend/app/services/ledger.py` | Replays trades into positions and the summary |
| `backend/app/services/validation.py` | Rejects bad input before it is stored |
| `backend/app/security.py` | Issues the JWT and guards private routes |
| `frontend/src/api` | Fetch client used by every screen |
| `frontend/src/pages` | Sign in, register, portfolio list, portfolio detail |

Each portfolio belongs to one analyst. A request for someone else's id returns **404**, the same as a missing id.

Holdings use weighted-average cost. A sell reduces the remaining cost at that average and books realised profit or loss against the sale price. Current value uses the last unit price traded in that portfolio, not a live market quote. Trades are replayed by date, with buys before sells on the same day, so a back-dated sell is checked against the position it would actually have had.

## Tech stack

| Piece | Choice | Why |
| --- | --- | --- |
| API | Flask 3, Flask-SQLAlchemy, Flask-Migrate, PyJWT | A small REST surface. Passwords are hashed with Werkzeug. Tokens are HS256 and expire; there is no refresh token. |
| Database | SQLite locally, PostgreSQL 16 in Compose and on Render | No extra database is required to run the tests or the app locally. Postgres is used where the data has to outlive one container. Legacy `postgres://` URLs are rewritten to `postgresql://`. |
| Schema | Alembic migrations in `backend/migrations` | `flask db upgrade` creates the tables. |
| Frontend | React 18, Vite 5, React Router 6 | A single-page app. Lists, forms, and charts are filled from API responses. |
| Chart | Recharts | Allocation donut by current value. Slice colours are the `--chart-*` tokens, so dark mode changes them too. |
| Tests | pytest, Vitest, Testing Library | API behaviour, money formatting, and the transaction table. |

Visual design is defined once in `frontend/src/styles/tokens.css`: navy `#0B1F3A`, amber `#F5B301`, neutral greys, and IBM Plex Sans. Spacing is a 4px scale. Dark mode follows `prefers-color-scheme` by remapping those same variables. Green and red are only used next to a plus or a minus. Amounts are formatted like `KES 1,250,000.00`, and numeric columns are right-aligned.

The interface uses semantic headings and tables, labelled fields, a skip link, keyboard focus, and a confirmation dialog before a portfolio or trade is deleted. Empty, loading, and error states are on every API-backed view.

## Layout

```
├── backend/                 Flask API, migrations, OpenAPI spec, pytest
├── frontend/                React client
├── docker-compose.yml       Postgres, API, and frontend
├── render.yaml              Render blueprint for the API and Postgres
└── .github/workflows/ci.yml Tests and the frontend production build
```

## Environment

Copy the examples and keep the real files out of git. Both `.env.example` files are the templates. They contain the demo password on purpose so a reviewer can sign in. They do not contain a production secret.

`backend/.env.example`

| Variable | Role |
| --- | --- |
| `APP_ENV` | `development` or `production`. Production refuses the default `SECRET_KEY`. |
| `SECRET_KEY` | Signs JWTs. Generate a long random value on the host. |
| `DATABASE_URL` | `sqlite:///fintrack.db`, or a Postgres URL. |
| `CORS_ORIGINS` | Comma-separated browser origins allowed to call the API. |
| `JWT_EXPIRES_MINUTES` | Access-token lifetime. Default 60. |
| `SEED_DEMO` | When `true`, `start.sh` creates the demo analyst if that username is missing. |
| `DEMO_USERNAME` | Default `demo`. Stored in lowercase. |
| `DEMO_PASSWORD` | Default `Demo@12345`. Override this on the host if you want a different demo password, and give reviewers the value you set. |

`frontend/.env.example`

| Variable | Role |
| --- | --- |
| `VITE_API_URL` | API origin, no trailing slash. Vite inlines it when the frontend is built. |

## API

Register and login are public. Health and the docs are public. Every other route requires `Authorization: Bearer <token>`.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/auth/register` | Create an analyst. `201` with `{token, user}`. |
| POST | `/api/auth/login` | Sign in. Same response shape. |
| GET | `/api/auth/me` | The signed-in analyst. |
| GET | `/api/portfolios` | This analyst's portfolios, each with totals and a trade count. |
| POST | `/api/portfolios` | Create a portfolio. |
| GET | `/api/portfolios/{id}` | One portfolio and its totals. |
| PUT | `/api/portfolios/{id}` | Update name, client name, or base currency. |
| DELETE | `/api/portfolios/{id}` | Delete the portfolio and its trades. `204`. |
| GET | `/api/portfolios/{id}/summary` | Holdings and performance. |
| GET | `/api/portfolios/{id}/transactions` | One page of trades. |
| POST | `/api/portfolios/{id}/transactions` | Record a buy or sell. `201`. |
| GET | `/api/portfolios/{id}/transactions/export.csv` | CSV download of the filtered trades. |
| DELETE | `/api/transactions/{id}` | Delete one trade. `204`. |
| GET | `/api/health` | `{"status": "ok"}`. |
| GET | `/api/docs` | Swagger UI. |
| GET | `/api/openapi.yaml` | OpenAPI 3 document. |

Portfolio fields: `name`, `client_name`, `base_currency` (`KES` or `USD`). The created date is set by the server.

Transaction fields: `instrument` (for example `SCOM`, `KCB`, `EQTY`, `T-BILL-91`), `type` (`BUY` or `SELL`), `quantity`, `unit_price`, `trade_date` (`YYYY-MM-DD`). Quantity and price must be greater than zero and can have at most four decimal places. A trade date cannot be in the future.

Registration: `username`, `password`, optional `full_name`. Usernames are 3–50 characters from `a-z`, digits, `.`, `_`, and `-`, and are stored lowercase. Passwords are 8–128 characters.

Transaction list query: `instrument`, `type`, `date_from`, `date_to`, `sort` (`trade_date`, `instrument`, `type`, `quantity`, `unit_price`), `order` (`asc` or `desc`), `page`, `per_page` (1–100, default 20). The UI asks for 10 rows per page and sends the same filters to the CSV export.

The summary lists, per open instrument, net quantity, average cost, amount invested, last price, current value, unrealised profit or loss, and allocation percent. Portfolio totals add invested, value, unrealised profit or loss (amount and percent of cost), and realised profit or loss. A position that has been fully sold drops off the holdings list; its realised result stays in the total.

Failures use one JSON shape:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Some fields are invalid.",
    "details": { "quantity": "Quantity must be greater than zero." }
  }
}
```

| Status | When |
| --- | --- |
| 400 | The body is not a JSON object, or a field is invalid. |
| 401 | The token is missing, expired, or invalid, or the login is wrong. |
| 404 | That portfolio or trade does not exist for this analyst. |
| 409 | The username is taken, or deleting this trade would leave a later sell short. |
| 422 | The sell is larger than the quantity held on that date. |
| 500 | Unexpected failure. The message does not include internal detail. |

An unknown username and a wrong password return the same 401, so the API does not reveal which accounts exist.

## Tests

```bash
cd backend
source .venv/bin/activate
python -m pytest -q
```

```bash
cd frontend
npm test
npm run build
```

`.github/workflows/ci.yml` runs the same checks on every push to `main` and on pull requests: pytest, then `npm test` and `npm run build`. GitHub only picks up a workflow stored at the repository root as `.github/workflows/ci.yml`. The pipeline does not run a separate linter, because the project does not configure one.

## Assumptions

- There is no shared access and no admin role. Ownership is the only authorisation rule.
- An instrument is a ticker string. Nothing in this app calls an exchange.
- "Current value" means the last unit price recorded on a trade in that portfolio.
- The ledger stores buys and sells only. It does not store cash deposits, fees, dividends, or a conversion between KES and USD.
- A trade is corrected by deleting it and recording it again, when the remaining history still has enough holdings for later sells.
- The demo clients and prices are made up for this exercise.

## Trade-offs

- Positions are calculated by replaying the trades on each summary, instead of storing a balance table. Deletes stay consistent with later sells, which matters more here than shaving milliseconds off a handful of rows.
- SQLite keeps local setup to one command. Compose and Render use Postgres so the deployed data is durable.
- Swagger UI is loaded from a CDN. The spec file is served by this API, so the contract is still in the repo at `backend/openapi.yaml`.
- The access token sits in `localStorage`. Any 401 clears it and returns the analyst to the sign-in screen.
- Dark mode follows the operating system. There is no separate toggle in the header.

## Deployment

The site and the API have to stay publicly available over HTTPS for at least 14 days after submission. Put secrets in the host's environment, not in the repository. Set `CORS_ORIGINS` to the frontend origin only.

### API and database on Render

1. Push the repository to GitHub.
2. In Render, create a new Blueprint and point it at `render.yaml`. That file defines the Postgres database `fintrack-db` and the Docker web service `fintrack-api` (`rootDir: backend`, health check `/api/health`).
3. When Render asks, set `CORS_ORIGINS` to the frontend origin, for example `https://your-app.vercel.app`. No trailing slash.
4. Set `DEMO_PASSWORD` if it should not be `Demo@12345`. Render generates `SECRET_KEY`. `SEED_DEMO` is already `true`.
5. Open `https://<your-service>.onrender.com/api/health`, then `https://<your-service>.onrender.com/api/docs`.

On boot, `backend/start.sh` applies migrations, seeds the demo analyst when `SEED_DEMO=true`, and serves the API with gunicorn.

### Frontend on Vercel or Netlify

1. Import the same repository. Set the project root to `frontend`.
2. Add the build variable `VITE_API_URL` with the Render origin, including `https://` and with no trailing slash. Change it and redeploy if the API host changes, because Vite reads it at build time.
3. Build with `npm run build`. The output directory is `dist`. `frontend/vercel.json` and `frontend/public/_redirects` send client-side routes back to `index.html`.

### Live URLs

The hosts assign these. Write them here, and in the submission email, once the deploy is up.

| Surface | URL |
| --- | --- |
| Frontend | |
| API health | |
| Swagger UI | `/api/docs` on the API host |
| OpenAPI | `/api/openapi.yaml` on the API host |
| Demo login | `demo` / `Demo@12345`, unless `DEMO_PASSWORD` was changed on Render |

## Repository

This is a monorepo with `backend/` and `frontend/` at the root. Work landed as incremental commits on `main`.

https://github.com/MaginaBrian/Finnet

## Tools

Cursor was used as a coding assistant while building FinTrack. The behaviour above is what to review, and the implementation can be walked through line by line.

## What is left out

- Live market prices in place of the last trade in the ledger.
- Fees, dividends, cash movements, and an edit action on an existing trade.
- Continuing the git history through a feature branch and a pull request.
- A deploy that starts by itself when `main` moves. Render and Vercel still need to be connected once, using the blueprint and the frontend project above.
- A light/dark control inside the app. Dark mode already follows the system setting.

## Submission

Reply to the recruitment email with:

1. Repository: https://github.com/MaginaBrian/Finnet
2. Live frontend URL, live Swagger URL, and the demo login from the table above.
3. Approximate hours spent.
4. Notes: data is fictional. Valuation is the last traded price on a weighted-average cost basis. CORS on the API must be the deployed frontend origin.
