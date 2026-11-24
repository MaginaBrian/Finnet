from flask import Blueprint

from app.services.summary_service import holdings_for_portfolio, overview_for_user
from app.services.portfolio_service import owned_portfolio
from app.utils.decorators import get_current_user
from app.utils.responses import ok

summary_bp = Blueprint("summary", __name__)


@summary_bp.get("/", strict_slashes=False)
def overview():
    return ok(overview_for_user(get_current_user()))


@summary_bp.get("/portfolios/<int:portfolio_id>")
def portfolio_summary(portfolio_id):
    user = get_current_user()
    portfolio = owned_portfolio(user, portfolio_id)
    return ok({"portfolio": portfolio.to_dict(), **holdings_for_portfolio(portfolio)})
