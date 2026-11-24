from flask import Blueprint, request

from app.services.transaction_service import (
    create_transaction,
    delete_transaction,
    list_transactions,
    update_transaction,
)
from app.utils.decorators import get_current_user
from app.utils.responses import ok

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.get("/portfolios/<int:portfolio_id>/transactions")
def index(portfolio_id):
    return ok(list_transactions(get_current_user(), portfolio_id))


@transactions_bp.post("/portfolios/<int:portfolio_id>/transactions")
def create(portfolio_id):
    data = request.get_json(silent=True) or {}
    return ok(create_transaction(get_current_user(), portfolio_id, data), 201)


@transactions_bp.put("/transactions/<int:transaction_id>")
def update(transaction_id):
    data = request.get_json(silent=True) or {}
    return ok(update_transaction(get_current_user(), transaction_id, data))


@transactions_bp.delete("/transactions/<int:transaction_id>")
def destroy(transaction_id):
    delete_transaction(get_current_user(), transaction_id)
    return ok({"deleted": True})
