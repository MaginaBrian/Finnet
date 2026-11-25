"""Index of the HTTP API. Registered first so /api is documented."""
from flask import Blueprint, jsonify

bp = Blueprint("docs", __name__)


@bp.get("/api")
def index():
    return jsonify(
        {
            "name": "Fintrack",
            "endpoints": [
                "POST /api/auth/register",
                "POST /api/auth/login",
                "GET /api/auth/me",
                "GET /api/portfolios",
                "POST /api/portfolios",
                "GET /api/portfolios/<id>",
                "PUT /api/portfolios/<id>",
                "DELETE /api/portfolios/<id>",
                "GET /api/portfolios/<id>/summary",
                "GET /api/portfolios/<id>/transactions",
                "GET /api/portfolios/<id>/transactions/export.csv",
                "POST /api/portfolios/<id>/transactions",
                "DELETE /api/transactions/<id>",
            ],
        }
    )
