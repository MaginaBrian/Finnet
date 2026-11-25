from datetime import datetime, timezone

from ..extensions import db

TRANSACTION_TYPES = ("BUY", "SELL")

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolios.id"), nullable=False, index=True)
    instrument = db.Column(db.String(20), nullable=False, index=True)
    type = db.Column(db.String(4), nullable=False)
    quantity = db.Column(db.Numeric(18, 4), nullable=False)
    unit_price = db.Column(db.Numeric(18, 4), nullable=False)
    trade_date = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    portfolio = db.relationship("Portfolio", back_populates="transactions")

    __table_args__ = (
        db.CheckConstraint("quantity > 0", name="ck_transactions_quantity_positive"),
        db.CheckConstraint("unit_price > 0", name="ck_transactions_price_positive"),
        db.CheckConstraint("type IN ('BUY','SELL')", name="ck_transactions_type"),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "instrument": self.instrument,
            "type": self.type,
            "quantity": float(self.quantity),
            "unit_price": float(self.unit_price),
            "total": float(self.quantity * self.unit_price),
            "trade_date": self.trade_date.isoformat(),
        }
