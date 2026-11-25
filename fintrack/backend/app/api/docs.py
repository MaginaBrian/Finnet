"""Health check plus public Swagger UI at /api/docs."""
from pathlib import Path

from flask import Blueprint, Response, jsonify, send_file

bp = Blueprint("docs", __name__, url_prefix="/api")
SPEC_PATH = Path(__file__).resolve().parents[2] / "openapi.yaml"

SWAGGER_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>FinTrack API docs</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
  <script>
    window.ui = SwaggerUIBundle({ url: "openapi.yaml", dom_id: "#swagger-ui", persistAuthorization: true });
  </script>
</body>
</html>"""


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/docs")
def swagger_ui():
    return Response(SWAGGER_HTML, mimetype="text/html")


@bp.get("/openapi.yaml")
def openapi_spec():
    return send_file(SPEC_PATH, mimetype="application/yaml")
