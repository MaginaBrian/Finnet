from flask import Blueprint, request

from app.security import login_required
from app.services.transaction_service import (
    create_transaction,
    delete_transaction,
    list_transactions,
    update_transaction,
)
from app.services.validation import json_body, parse_transaction_query, validate_transaction
from app.utils.responses import ok

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.get("/portfolios/<int:portfolio_id>/transactions")
@login_required
def index(portfolio_id):
    return ok(list_transactions(portfolio_id, parse_transaction_query(request.args)))

@transactions_bp.post("/portfolios/<int:portfolio_id>/transactions")
@login_required
def create(portfolio_id):
    return ok(create_transaction(portfolio_id, validate_transaction(json_body())), 201)

@transactions_bp.put("/transactions/<int:transaction_id>")
@login_required
def update(transaction_id):
    return ok(update_transaction(transaction_id, validate_transaction(json_body())))

@transactions_bp.delete("/transactions/<int:transaction_id>")
@login_required
def destroy(transaction_id):
    delete_transaction(transaction_id)
    return ok({"deleted": True})
