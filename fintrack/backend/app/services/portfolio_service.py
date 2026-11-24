from app.extensions import db
from app.models.portfolio import Portfolio
from app.services.summary_service import value_transactions
from app.utils.responses import APIError


def list_portfolios(user):
    portfolios = (
        Portfolio.query.filter_by(user_id=user.id)
        .order_by(Portfolio.created_at.desc())
        .all()
    )
    return [serialize_portfolio(portfolio) for portfolio in portfolios]


def get_portfolio(user, portfolio_id, include_transactions=False):
    portfolio = owned_portfolio(user, portfolio_id)
    return serialize_portfolio(portfolio, include_transactions=include_transactions)


def create_portfolio(user, name, description=""):
    cleaned_name = (name or "").strip()
    if not cleaned_name:
        raise APIError("Portfolio name is required")
    portfolio = Portfolio(
        user_id=user.id,
        name=cleaned_name,
        description=(description or "").strip(),
    )
    db.session.add(portfolio)
    db.session.commit()
    return serialize_portfolio(portfolio)


def update_portfolio(user, portfolio_id, name=None, description=None):
    portfolio = owned_portfolio(user, portfolio_id)
    if name is not None:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise APIError("Portfolio name is required")
        portfolio.name = cleaned_name
    if description is not None:
        portfolio.description = description.strip()
    db.session.commit()
    return serialize_portfolio(portfolio)


def delete_portfolio(user, portfolio_id):
    portfolio = owned_portfolio(user, portfolio_id)
    db.session.delete(portfolio)
    db.session.commit()


def owned_portfolio(user, portfolio_id):
    portfolio = Portfolio.query.filter_by(id=portfolio_id, user_id=user.id).first()
    if portfolio is None:
        raise APIError("Portfolio not found", 404)
    return portfolio


def serialize_portfolio(portfolio, include_transactions=False):
    payload = {**portfolio.to_dict(), **value_transactions(portfolio.transactions)}
    if include_transactions:
        ordered = sorted(
            portfolio.transactions, key=lambda tx: (tx.occurred_at, tx.id or 0), reverse=True
        )
        payload["transactions"] = [tx.to_dict() for tx in ordered]
    return payload
