from flask import jsonify


class APIError(Exception):
    def __init__(self, message, status=400, code=None, details=None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.details = details


def ok(data=None, status=200):
    return jsonify({"data": data}), status


def error(message, status=400, code="error", details=None):
    body = {"code": code, "message": message}
    if details:
        body["details"] = details
    return jsonify({"error": body}), status
