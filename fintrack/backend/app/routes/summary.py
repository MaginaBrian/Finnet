from flask import Blueprint

from app.security import login_required
from app.services.access import get_owned_portfolio
from app.services.summary_service import holdings_for_portfolio, overview_for_user
from app.utils.responses import ok

summary_bp = Blueprint("summary", __name__)


@summary_bp.get("/", strict_slashes=False)
@login_required
def overview():
    return ok(overview_for_user())


@summary_bp.get("/portfolios/<int:portfolio_id>")
@login_required
def portfolio_summary(portfolio_id):
    portfolio = get_owned_portfolio(portfolio_id)
    return ok({"portfolio": portfolio.to_dict(), **holdings_for_portfolio(portfolio)})
