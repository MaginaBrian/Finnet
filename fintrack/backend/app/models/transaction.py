from datetime import datetime, timezone
from decimal import Decimal

from app.extensions import db


def _money(value):
    if value is None:
        return None
    return float(Decimal(value).quantize(Decimal("0.01")))


def _quantity(value):
    if value is None:
        return None
    return float(Decimal(value).quantize(Decimal("0.0001")))


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(
        db.Integer, db.ForeignKey("portfolios.id"), nullable=False, index=True
    )
    kind = db.Column(db.String(20), nullable=False)
    symbol = db.Column(db.String(16))
    quantity = db.Column(db.Numeric(18, 4))
    price = db.Column(db.Numeric(18, 4))
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    notes = db.Column(db.String(500), default="")
    occurred_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    portfolio = db.relationship("Portfolio", back_populates="transactions")

    def to_dict(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "kind": self.kind,
            "symbol": self.symbol,
            "quantity": _quantity(self.quantity),
            "price": _money(self.price),
            "amount": _money(self.amount),
            "notes": self.notes or "",
            "occurred_at": self.occurred_at.isoformat(),
            "created_at": self.created_at.isoformat(),
        }
