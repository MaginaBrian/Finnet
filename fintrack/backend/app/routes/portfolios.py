from flask import Blueprint, request

from app.services.portfolio_service import (
    create_portfolio,
    delete_portfolio,
    get_portfolio,
    list_portfolios,
    update_portfolio,
)
from app.utils.decorators import get_current_user
from app.utils.responses import ok

portfolios_bp = Blueprint("portfolios", __name__)


@portfolios_bp.get("/", strict_slashes=False)
def index():
    return ok(list_portfolios(get_current_user()))


@portfolios_bp.post("/", strict_slashes=False)
def create():
    data = request.get_json(silent=True) or {}
    portfolio = create_portfolio(
        get_current_user(), data.get("name"), data.get("description", "")
    )
    return ok(portfolio, 201)


@portfolios_bp.get("/<int:portfolio_id>")
def show(portfolio_id):
    return ok(get_portfolio(get_current_user(), portfolio_id, include_transactions=True))


@portfolios_bp.put("/<int:portfolio_id>")
def update(portfolio_id):
    data = request.get_json(silent=True) or {}
    portfolio = update_portfolio(
        get_current_user(),
        portfolio_id,
        name=data.get("name"),
        description=data.get("description"),
    )
    return ok(portfolio)


@portfolios_bp.delete("/<int:portfolio_id>")
def destroy(portfolio_id):
    delete_portfolio(get_current_user(), portfolio_id)
    return ok({"deleted": True})
