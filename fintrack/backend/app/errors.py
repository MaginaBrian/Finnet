"""One consistent JSON error shape for every failure.

    {"error": {"code": "validation_error", "message": "...", "details": {...}}}
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.extensions import db
from app.utils.responses import APIError

_CODES = {
    400: "validation_error",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
    409: "conflict",
    422: "validation_error",
    500: "server_error",
}


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(err):
        db.session.rollback()
        return _error(err.status, err.code or _CODES.get(err.status, "error"), err.message, err.details)

    @app.errorhandler(HTTPException)
    def handle_http_error(err):
        return _error(err.code or 500, _CODES.get(err.code, "error"), err.description)

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        if app.propagate_exceptions:
            raise err
        app.logger.exception("Unhandled error")
        db.session.rollback()
        return _error(500, "server_error", "Something went wrong")


def _error(status, code, message, details=None):
    body = {"code": code, "message": message}
    if details:
        body["details"] = details
    return jsonify({"error": body}), status
