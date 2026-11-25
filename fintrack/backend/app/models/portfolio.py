from datetime import datetime, timezone

from ..extensions import db

CURRENCIES = ("KES", "USD")


class Portfolio(db.Model):
    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    base_currency = db.Column(db.String(3), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    owner = db.relationship("User", back_populates="portfolios")
    transactions = db.relationship(
        "Transaction", back_populates="portfolio", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "client_name": self.client_name,
            "base_currency": self.base_currency,
            "created_at": self.created_at.date().isoformat(),
        }
