import csv
import io

from flask import Blueprint, Response, jsonify, request

from ..errors import ApiError
from ..extensions import db
from ..models import Transaction
from ..security import login_required
from ..services.access import get_owned_portfolio, get_owned_transaction
from ..services.ledger import InsufficientHoldings, replay
from ..services.validation import json_body, parse_transaction_query, validate_transaction

bp = Blueprint("transactions", __name__, url_prefix="/api")

SORT_COLUMNS = {
    "trade_date": Transaction.trade_date,
    "instrument": Transaction.instrument,
    "type": Transaction.type,
    "quantity": Transaction.quantity,
    "unit_price": Transaction.unit_price,
}

def _filtered_query(portfolio_id: int, params: dict):
    query = Transaction.query.filter_by(portfolio_id=portfolio_id)
    if params["instrument"]:
        query = query.filter(Transaction.instrument.contains(params["instrument"], autoescape=True))
    if params["type"]:
        query = query.filter(Transaction.type == params["type"])
    if params["date_from"]:
        query = query.filter(Transaction.trade_date >= params["date_from"])
    if params["date_to"]:
        query = query.filter(Transaction.trade_date <= params["date_to"])
    column = SORT_COLUMNS[params["sort"]]
    direction = column.asc() if params["order"] == "asc" else column.desc()
    tie_break = Transaction.id.asc() if params["order"] == "asc" else Transaction.id.desc()
    return query.order_by(direction, tie_break)

@bp.get("/portfolios/<int:portfolio_id>/transactions")
@login_required
def list_transactions(portfolio_id):
    portfolio = get_owned_portfolio(portfolio_id)
    params = parse_transaction_query(request.args)
    page = _filtered_query(portfolio.id, params).paginate(
        page=params["page"], per_page=params["per_page"], error_out=False
    )
    return jsonify(
        {
            "data": [t.to_dict() for t in page.items],
            "meta": {
                "page": page.page,
                "per_page": page.per_page,
                "total": page.total,
                "pages": page.pages,
            },
        }
    )

@bp.get("/portfolios/<int:portfolio_id>/transactions/export.csv")
@login_required
def export_transactions(portfolio_id):
    portfolio = get_owned_portfolio(portfolio_id)
    params = parse_transaction_query(request.args)
    rows = _filtered_query(portfolio.id, params).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["trade_date", "instrument", "type", "quantity", "unit_price", "total", "currency"])
    for t in rows:
        writer.writerow(
            [t.trade_date.isoformat(), t.instrument, t.type, t.quantity, t.unit_price,
             t.quantity * t.unit_price, portfolio.base_currency]
        )
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename="portfolio-{portfolio.id}-transactions.csv"'},
    )

@bp.post("/portfolios/<int:portfolio_id>/transactions")
@login_required
def create_transaction(portfolio_id):
    portfolio = get_owned_portfolio(portfolio_id)
    data = validate_transaction(json_body())
    txn = Transaction(portfolio_id=portfolio.id, **data)

    try:
        replay([*portfolio.transactions, txn])
    except InsufficientHoldings as exc:
        raise ApiError(
            422,
            "insufficient_holdings",
            f"Cannot sell {exc.requested.normalize():f} {exc.instrument} on {exc.trade_date}: "
            f"only {exc.held.normalize():f} held at that date.",
            {"quantity": "Exceeds the quantity held."},
        )

    db.session.add(txn)
    db.session.commit()
    return jsonify(txn.to_dict()), 201

@bp.delete("/transactions/<int:transaction_id>")
@login_required
def delete_transaction(transaction_id):
    txn = get_owned_transaction(transaction_id)
    remaining = [t for t in txn.portfolio.transactions if t.id != txn.id]
    try:
        replay(remaining)
    except InsufficientHoldings as exc:
        raise ApiError(
            409,
            "ledger_conflict",
            f"Deleting this trade would leave a later sale of {exc.instrument} without enough "
            "holdings. Delete the later sale first.",
        )
    db.session.delete(txn)
    db.session.commit()
    return "", 204
