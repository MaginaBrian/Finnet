from flask import Blueprint, g, jsonify
from sqlalchemy.orm import selectinload

from ..extensions import db
from ..models import Portfolio
from ..security import login_required
from ..services.access import get_owned_portfolio
from ..services.ledger import summarize
from ..services.validation import json_body, validate_portfolio

bp = Blueprint("portfolios", __name__, url_prefix="/api/portfolios")

def _with_totals(portfolio: Portfolio) -> dict:
    summary = summarize(portfolio.transactions, portfolio.base_currency)
    return {
        **portfolio.to_dict(),
        "transaction_count": len(portfolio.transactions),
        "totals": summary["totals"],
    }

@bp.get("")
@login_required
def list_portfolios():
    portfolios = (
        Portfolio.query.options(selectinload(Portfolio.transactions))
        .filter_by(owner_id=g.current_user.id)
        .order_by(Portfolio.created_at.desc(), Portfolio.id.desc())
        .all()
    )
    return jsonify({"data": [_with_totals(p) for p in portfolios]})

@bp.post("")
@login_required
def create_portfolio():
    data = validate_portfolio(json_body())
    portfolio = Portfolio(owner_id=g.current_user.id, **data)
    db.session.add(portfolio)
    db.session.commit()
    return jsonify(_with_totals(portfolio)), 201

@bp.get("/<int:portfolio_id>")
@login_required
def get_portfolio(portfolio_id):
    return jsonify(_with_totals(get_owned_portfolio(portfolio_id)))

@bp.put("/<int:portfolio_id>")
@login_required
def update_portfolio(portfolio_id):
    portfolio = get_owned_portfolio(portfolio_id)
    data = validate_portfolio(json_body())
    for field, value in data.items():
        setattr(portfolio, field, value)
    db.session.commit()
    return jsonify(_with_totals(portfolio))

@bp.delete("/<int:portfolio_id>")
@login_required
def delete_portfolio(portfolio_id):
    portfolio = get_owned_portfolio(portfolio_id)
    db.session.delete(portfolio)
    db.session.commit()
    return "", 204

@bp.get("/<int:portfolio_id>/summary")
@login_required
def portfolio_summary(portfolio_id):
    portfolio = get_owned_portfolio(portfolio_id)
    summary = summarize(portfolio.transactions, portfolio.base_currency)
    return jsonify({"portfolio_id": portfolio.id, **summary})
