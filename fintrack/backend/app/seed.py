"""Fictional demo data. Safe to run repeatedly."""
import os
from datetime import date

from .extensions import db
from .models import Portfolio, Transaction, User

# (instrument, type, quantity, unit_price, trade_date)
KES_EQUITIES = [
    ("SCOM", "BUY", 50000, 14.20, date(2025, 11, 10)),
    ("KCB", "BUY", 12000, 38.50, date(2025, 11, 17)),
    ("EQTY", "BUY", 8000, 46.75, date(2025, 12, 2)),
    ("SCOM", "BUY", 20000, 16.80, date(2026, 1, 14)),
    ("KCB", "SELL", 4000, 44.25, date(2026, 2, 20)),
    ("EQTY", "BUY", 3000, 52.00, date(2026, 3, 9)),
    ("SCOM", "SELL", 15000, 21.30, date(2026, 5, 6)),
    ("KCB", "BUY", 5000, 49.10, date(2026, 8, 18)),
    ("T-BILL-91", "BUY", 2000, 97.45, date(2026, 9, 1)),
]

KES_FIXED_INCOME = [
    ("T-BILL-91", "BUY", 10000, 97.20, date(2026, 1, 12)),
    ("T-BILL-182", "BUY", 8000, 94.60, date(2026, 2, 3)),
    ("T-BILL-91", "SELL", 4000, 98.90, date(2026, 4, 13)),
    ("T-BILL-364", "BUY", 6000, 90.15, date(2026, 6, 22)),
    ("T-BILL-91", "BUY", 5000, 97.80, date(2026, 10, 5)),
]

USD_PORTFOLIO = [
    ("EUROBOND-2028", "BUY", 400, 96.50, date(2026, 2, 9)),
    ("USD-MMF", "BUY", 1500, 10.02, date(2026, 3, 16)),
    ("EUROBOND-2028", "BUY", 150, 98.10, date(2026, 6, 8)),
    ("USD-MMF", "SELL", 500, 10.31, date(2026, 10, 12)),
]

PORTFOLIOS = [
    ("Growth Equities", "Baraka Holdings Ltd", "KES", KES_EQUITIES),
    ("Treasury Ladder", "Kilima Pension Scheme", "KES", KES_FIXED_INCOME),
    ("Offshore Income", "Savannah Foundation", "USD", USD_PORTFOLIO),
]


def seed_demo() -> bool:
    username = os.getenv("DEMO_USERNAME", "demo").lower()
    password = os.getenv("DEMO_PASSWORD", "Demo@12345")
    if User.query.filter_by(username=username).first():
        return False

    user = User(username=username, full_name="Demo Analyst")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    for name, client, currency, trades in PORTFOLIOS:
        portfolio = Portfolio(owner_id=user.id, name=name, client_name=client, base_currency=currency)
        db.session.add(portfolio)
        db.session.flush()
        for instrument, kind, qty, price, traded in trades:
            db.session.add(
                Transaction(
                    portfolio_id=portfolio.id, instrument=instrument, type=kind,
                    quantity=qty, unit_price=price, trade_date=traded,
                )
            )
    db.session.commit()
    return True
