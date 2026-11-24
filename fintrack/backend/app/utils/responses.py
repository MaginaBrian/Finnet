from flask import jsonify


class APIError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def ok(data=None, status=200):
    return jsonify({"data": data}), status


def error(message, status=400):
    return jsonify({"error": message}), status
