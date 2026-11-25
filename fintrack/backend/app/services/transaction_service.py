from app.errors import ApiError
from app.extensions import db
from app.models import Transaction
from app.services.access import get_owned_portfolio, get_owned_transaction
from app.services.ledger import InsufficientHoldings, replay


def list_transactions(portfolio_id, query):
    portfolio = get_owned_portfolio(portfolio_id)
    rows = list(portfolio.transactions)
    if query["type"]:
        rows = [txn for txn in rows if txn.type == query["type"]]
    if query["instrument"]:
        rows = [txn for txn in rows if query["instrument"] in txn.instrument]
    if query["date_from"]:
        rows = [txn for txn in rows if txn.trade_date >= query["date_from"]]
    if query["date_to"]:
        rows = [txn for txn in rows if txn.trade_date <= query["date_to"]]
    rows.sort(key=lambda txn: getattr(txn, query["sort"]), reverse=query["order"] == "desc")
    total = len(rows)
    start = (query["page"] - 1) * query["per_page"]
    page = rows[start : start + query["per_page"]]
    return {
        "items": [txn.to_dict() for txn in page],
        "page": query["page"],
        "per_page": query["per_page"],
        "total": total,
    }


def create_transaction(portfolio_id, clean):
    portfolio = get_owned_portfolio(portfolio_id)
    txn = Transaction(portfolio_id=portfolio.id, **clean)
    portfolio.transactions.append(txn)
    _guard(portfolio)
    db.session.commit()
    return txn.to_dict()


def update_transaction(transaction_id, clean):
    txn = get_owned_transaction(transaction_id)
    txn.instrument = clean["instrument"]
    txn.type = clean["type"]
    txn.quantity = clean["quantity"]
    txn.unit_price = clean["unit_price"]
    txn.trade_date = clean["trade_date"]
    _guard(txn.portfolio)
    db.session.commit()
    return txn.to_dict()


def delete_transaction(transaction_id):
    txn = get_owned_transaction(transaction_id)
    portfolio = txn.portfolio
    db.session.delete(txn)
    db.session.flush()
    _guard(portfolio)
    db.session.commit()


def _guard(portfolio):
    try:
        replay(portfolio.transactions)
    except InsufficientHoldings as exc:
        db.session.rollback()
        raise ApiError(400, "insufficient_holdings", str(exc)) from exc
