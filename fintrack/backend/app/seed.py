from datetime import datetime, timezone
from decimal import Decimal

from app import create_app
from app.extensions import db
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction
from app.models.user import User

DEMO_EMAIL = "demo@fintrack.app"
DEMO_PASSWORD = "demo1234"


def run_seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        if User.query.filter_by(email=DEMO_EMAIL).first():
            print(f"Seed user already exists: {DEMO_EMAIL}")
            return

        user = User(name="Demo Investor", email=DEMO_EMAIL)
        user.set_password(DEMO_PASSWORD)
        growth = Portfolio(
            name="Growth",
            description="Long-term equity holdings",
            user=user,
        )
        income = Portfolio(
            name="Income",
            description="Cash and dividend holdings",
            user=user,
        )
        db.session.add(user)
        db.session.flush()

        growth.transactions.extend(
            [
                _cash("deposit", "5000.00", "2026-01-06", "Opening deposit"),
                _trade("buy", "AAPL", "10", "190.25", "2026-01-08", "Initial position"),
                _trade("buy", "MSFT", "4", "420.10", "2026-02-03", "Add to tech"),
            ]
        )
        income.transactions.extend(
            [
                _cash("deposit", "2000.00", "2026-01-15", "Cash reserve"),
                _trade("buy", "VOO", "2", "520.00", "2026-03-01", "Broad market"),
                _cash("dividend", "18.40", "2026-03-20", "VOO dividend"),
            ]
        )
        db.session.commit()
        print(f"Seeded {DEMO_EMAIL} / {DEMO_PASSWORD}")


def _when(day):
    return datetime.fromisoformat(day).replace(tzinfo=timezone.utc)


def _cash(kind, amount, day, notes):
    return Transaction(
        kind=kind,
        amount=Decimal(amount),
        notes=notes,
        occurred_at=_when(day),
    )


def _trade(kind, symbol, quantity, price, day, notes):
    qty = Decimal(quantity)
    px = Decimal(price)
    return Transaction(
        kind=kind,
        symbol=symbol,
        quantity=qty,
        price=px,
        amount=(qty * px).quantize(Decimal("0.01")),
        notes=notes,
        occurred_at=_when(day),
    )


if __name__ == "__main__":
    run_seed()
