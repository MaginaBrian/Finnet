from datetime import datetime, timezone
from decimal import Decimal

from app.extensions import db
from app.models.transaction import Transaction
from app.services.portfolio_service import owned_portfolio
from app.services.summary_service import CASH_KINDS, SHARE_KINDS
from app.utils.responses import APIError

KINDS = SHARE_KINDS | CASH_KINDS


def list_transactions(user, portfolio_id):
    portfolio = owned_portfolio(user, portfolio_id)
    ordered = sorted(
        portfolio.transactions, key=lambda tx: (tx.occurred_at, tx.id or 0), reverse=True
    )
    return [tx.to_dict() for tx in ordered]


def create_transaction(user, portfolio_id, payload):
    portfolio = owned_portfolio(user, portfolio_id)
    transaction = Transaction(portfolio_id=portfolio.id, created_at=datetime.now(timezone.utc))
    _apply_payload(transaction, payload)
    portfolio.transactions.append(transaction)
    _assert_no_short(portfolio.transactions)
    db.session.add(transaction)
    db.session.commit()
    return transaction.to_dict()


def update_transaction(user, transaction_id, payload):
    transaction = owned_transaction(user, transaction_id)
    _apply_payload(transaction, payload)
    _assert_no_short(transaction.portfolio.transactions)
    db.session.commit()
    return transaction.to_dict()


def delete_transaction(user, transaction_id):
    transaction = owned_transaction(user, transaction_id)
    db.session.delete(transaction)
    db.session.commit()


def owned_transaction(user, transaction_id):
    transaction = (
        Transaction.query.join(Transaction.portfolio)
        .filter(Transaction.id == transaction_id, Transaction.portfolio.has(user_id=user.id))
        .first()
    )
    if transaction is None:
        raise APIError("Transaction not found", 404)
    return transaction


def _apply_payload(transaction, payload):
    kind = (payload.get("kind") or transaction.kind or "").strip().lower()
    if kind not in KINDS:
        raise APIError("Kind must be buy, sell, deposit, withdrawal, or dividend")

    notes = payload.get("notes", transaction.notes or "")
    occurred_at = _parse_datetime(payload.get("occurred_at")) or transaction.occurred_at
    if occurred_at is None:
        occurred_at = datetime.now(timezone.utc)

    transaction.kind = kind
    transaction.notes = (notes or "").strip()
    transaction.occurred_at = occurred_at

    if kind in SHARE_KINDS:
        symbol = (payload.get("symbol") or transaction.symbol or "").strip().upper()
        quantity = _decimal(payload.get("quantity", transaction.quantity), "quantity")
        price = _decimal(payload.get("price", transaction.price), "price")
        if not symbol:
            raise APIError("Symbol is required for buy and sell")
        if quantity <= 0:
            raise APIError("Quantity must be greater than zero")
        if price < 0:
            raise APIError("Price cannot be negative")
        transaction.symbol = symbol
        transaction.quantity = quantity
        transaction.price = price
        transaction.amount = (quantity * price).quantize(Decimal("0.01"))
        return

    amount = _decimal(payload.get("amount", transaction.amount), "amount")
    if amount <= 0:
        raise APIError("Amount must be greater than zero")
    transaction.symbol = None
    transaction.quantity = None
    transaction.price = None
    transaction.amount = amount.quantize(Decimal("0.01"))


def _decimal(value, label):
    if value is None or value == "":
        raise APIError(f"{label.capitalize()} is required")
    try:
        return Decimal(str(value))
    except Exception as exc:
        raise APIError(f"{label.capitalize()} must be a number") from exc


def _parse_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise APIError("occurred_at must be an ISO date") from exc


def _sort_key(tx):
    return (tx.occurred_at, tx.id is None, tx.id or 0)


def _assert_no_short(transactions):
    quantities = {}
    ordered = sorted(transactions, key=_sort_key)
    for tx in ordered:
        if tx.kind not in SHARE_KINDS or not tx.symbol:
            continue
        quantities.setdefault(tx.symbol, Decimal("0"))
        delta = Decimal(tx.quantity or 0)
        quantities[tx.symbol] += delta if tx.kind == "buy" else -delta
        if quantities[tx.symbol] < 0:
            raise APIError(f"Not enough {tx.symbol} to sell", 400)
