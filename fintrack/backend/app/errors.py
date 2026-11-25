"""One consistent JSON error shape for every failure.

    {"error": {"code": "validation_error", "message": "...", "details": {...}}}
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, details: dict | None = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details or {}


def validation_error(details: dict, message: str = "Some fields are invalid.") -> ApiError:
    return ApiError(400, "validation_error", message, details)


def not_found(what: str = "Resource") -> ApiError:
    return ApiError(404, "not_found", f"{what} not found.")


def _payload(code: str, message: str, details: dict | None = None):
    return jsonify({"error": {"code": code, "message": message, "details": details or {}}})


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(err: ApiError):
        response = _payload(err.code, err.message, err.details)
        response.status_code = err.status
        if err.status == 401:
            response.headers["WWW-Authenticate"] = "Bearer"
        return response

    @app.errorhandler(HTTPException)
    def handle_http_error(err: HTTPException):
        code = (err.name or "error").lower().replace(" ", "_")
        response = _payload(code, err.description or err.name)
        response.status_code = err.code or 500
        return response

    @app.errorhandler(Exception)
    def handle_unexpected(err: Exception):
        app.logger.exception("Unhandled error: %s", err)
        response = _payload("internal_error", "Something went wrong on our side.")
        response.status_code = 500
        return response
