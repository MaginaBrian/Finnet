from flask import g

from ..errors import not_found
from ..extensions import db
from ..models import Portfolio, Transaction

def get_owned_portfolio(portfolio_id: int) -> Portfolio:
    portfolio = db.session.get(Portfolio, portfolio_id)
    if portfolio is None or portfolio.owner_id != g.current_user.id:
        raise not_found("Portfolio")
    return portfolio

def get_owned_transaction(transaction_id: int) -> Transaction:
    txn = db.session.get(Transaction, transaction_id)
    if txn is None or txn.portfolio.owner_id != g.current_user.id:
        raise not_found("Transaction")
    return txn
