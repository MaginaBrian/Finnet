from flask import g

from app.models import Portfolio
from app.services.ledger import summarize
from app.services.portfolio_service import serialize_portfolio


def overview_for_user():
    portfolios = (
        Portfolio.query.filter_by(owner_id=g.current_user.id)
        .order_by(Portfolio.created_at.desc())
        .all()
    )
    cards = [serialize_portfolio(portfolio) for portfolio in portfolios]
    recent = [txn for portfolio in portfolios for txn in portfolio.transactions]
    recent.sort(key=lambda txn: (txn.trade_date, txn.id or 0), reverse=True)
    return {
        "portfolio_count": len(cards),
        "portfolios": cards,
        "recent_transactions": [txn.to_dict() for txn in recent[:8]],
    }


def holdings_for_portfolio(portfolio):
    return summarize(portfolio.transactions, portfolio.base_currency)
