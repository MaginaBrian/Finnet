from flask import g

from app.extensions import db
from app.models import Portfolio
from app.services.access import get_owned_portfolio
from app.services.ledger import summarize


def list_portfolios():
    portfolios = (
        Portfolio.query.filter_by(owner_id=g.current_user.id)
        .order_by(Portfolio.created_at.desc())
        .all()
    )
    return [serialize_portfolio(portfolio) for portfolio in portfolios]


def get_portfolio(portfolio_id, include_transactions=False):
    return serialize_portfolio(get_owned_portfolio(portfolio_id), include_transactions)


def create_portfolio(clean):
    portfolio = Portfolio(owner_id=g.current_user.id, **clean)
    db.session.add(portfolio)
    db.session.commit()
    return serialize_portfolio(portfolio)


def update_portfolio(portfolio_id, clean):
    portfolio = get_owned_portfolio(portfolio_id)
    portfolio.name = clean["name"]
    portfolio.client_name = clean["client_name"]
    portfolio.base_currency = clean["base_currency"]
    db.session.commit()
    return serialize_portfolio(portfolio)


def delete_portfolio(portfolio_id):
    portfolio = get_owned_portfolio(portfolio_id)
    db.session.delete(portfolio)
    db.session.commit()


def serialize_portfolio(portfolio, include_transactions=False):
    payload = {**portfolio.to_dict(), **summarize(portfolio.transactions, portfolio.base_currency)}
    if include_transactions:
        ordered = sorted(portfolio.transactions, key=lambda txn: (txn.trade_date, txn.id or 0), reverse=True)
        payload["transactions"] = [txn.to_dict() for txn in ordered]
    return payload
