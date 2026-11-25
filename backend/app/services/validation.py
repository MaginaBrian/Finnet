import re
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from flask import request

from ..errors import ApiError, validation_error
from ..models import CURRENCIES, TRANSACTION_TYPES

INSTRUMENT_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,19}$")
USERNAME_RE = re.compile(r"^[a-z0-9._-]{3,50}$")
MAX_AMOUNT = Decimal("1000000000")
SORTABLE = ("trade_date", "instrument", "type", "quantity", "unit_price")

def json_body() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError(400, "invalid_json", "Request body must be a JSON object.")
    return data

def _text(data, field, errors, label, max_len=100):
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        errors[field] = f"{label} is required."
        return None
    value = value.strip()
    if len(value) > max_len:
        errors[field] = f"{label} must be {max_len} characters or fewer."
        return None
    return value

def _decimal(data, field, errors, label):
    raw = data.get(field)
    if raw is None or isinstance(raw, bool) or raw == "":
        errors[field] = f"{label} is required."
        return None
    try:
        value = Decimal(str(raw))
    except InvalidOperation:
        errors[field] = f"{label} must be a number."
        return None
    if not value.is_finite():
        errors[field] = f"{label} must be a number."
    elif value <= 0:
        errors[field] = f"{label} must be greater than zero."
    elif value > MAX_AMOUNT:
        errors[field] = f"{label} is too large."
    elif -value.as_tuple().exponent > 4:
        errors[field] = f"{label} can have at most 4 decimal places."
    else:
        return value
    return None

def validate_credentials(data: dict, registering: bool) -> dict:
    errors = {}
    username = data.get("username")
    password = data.get("password")
    clean = {}

    if not isinstance(username, str) or not username.strip():
        errors["username"] = "Username is required."
    else:
        username = username.strip().lower()
        if registering and not USERNAME_RE.match(username):
            errors["username"] = "Use 3-50 letters, numbers, dots, dashes or underscores."
        clean["username"] = username

    if not isinstance(password, str) or not password:
        errors["password"] = "Password is required."
    elif registering and not (8 <= len(password) <= 128):
        errors["password"] = "Password must be 8-128 characters."
    clean["password"] = password

    if registering:
        full_name = data.get("full_name", "")
        if not isinstance(full_name, str) or len(full_name.strip()) > 100:
            errors["full_name"] = "Full name must be 100 characters or fewer."
        clean["full_name"] = full_name.strip() if isinstance(full_name, str) else ""

    if errors:
        raise validation_error(errors)
    return clean

def validate_portfolio(data: dict) -> dict:
    errors = {}
    name = _text(data, "name", errors, "Portfolio name")
    client = _text(data, "client_name", errors, "Client name")
    currency = data.get("base_currency")
    if currency not in CURRENCIES:
        errors["base_currency"] = f"Base currency must be one of: {', '.join(CURRENCIES)}."
    if errors:
        raise validation_error(errors)
    return {"name": name, "client_name": client, "base_currency": currency}

def validate_transaction(data: dict) -> dict:
    errors = {}

    instrument = data.get("instrument")
    if not isinstance(instrument, str) or not instrument.strip():
        errors["instrument"] = "Instrument is required."
        instrument = None
    else:
        instrument = instrument.strip().upper()
        if not INSTRUMENT_RE.match(instrument):
            errors["instrument"] = "Use letters, numbers, dots or dashes (e.g. SCOM, T-BILL-91)."
            instrument = None

    txn_type = data.get("type")
    if txn_type not in TRANSACTION_TYPES:
        errors["type"] = "Type must be BUY or SELL."

    quantity = _decimal(data, "quantity", errors, "Quantity")
    unit_price = _decimal(data, "unit_price", errors, "Unit price")

    trade_date = None
    raw_date = data.get("trade_date")
    if not isinstance(raw_date, str) or not raw_date:
        errors["trade_date"] = "Trade date is required."
    else:
        try:
            trade_date = date.fromisoformat(raw_date)
        except ValueError:
            errors["trade_date"] = "Trade date must be a valid date (YYYY-MM-DD)."
        else:

            if trade_date > date.today() + timedelta(days=1):
                errors["trade_date"] = "Trade date cannot be in the future."
            elif trade_date.year < 1990:
                errors["trade_date"] = "Trade date is too far in the past."

    if errors:
        raise validation_error(errors)
    return {
        "instrument": instrument,
        "type": txn_type,
        "quantity": quantity,
        "unit_price": unit_price,
        "trade_date": trade_date,
    }

def _int_arg(args, name, default, minimum, maximum, errors):
    raw = args.get(name)
    if raw in (None, ""):
        return default
    try:
        value = int(raw)
    except ValueError:
        errors[name] = f"{name} must be an integer."
        return default
    if not minimum <= value <= maximum:
        errors[name] = f"{name} must be between {minimum} and {maximum}."
    return value

def _date_arg(args, name, errors):
    raw = args.get(name)
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        errors[name] = f"{name} must be a valid date (YYYY-MM-DD)."
        return None

def parse_transaction_query(args) -> dict:
    errors = {}
    sort = args.get("sort", "trade_date")
    if sort not in SORTABLE:
        errors["sort"] = f"sort must be one of: {', '.join(SORTABLE)}."
    order = args.get("order", "desc").lower()
    if order not in ("asc", "desc"):
        errors["order"] = "order must be asc or desc."
    txn_type = args.get("type", "").upper() or None
    if txn_type and txn_type not in TRANSACTION_TYPES:
        errors["type"] = "type must be BUY or SELL."

    query = {
        "sort": sort,
        "order": order,
        "type": txn_type,
        "instrument": (args.get("instrument") or "").strip().upper() or None,
        "date_from": _date_arg(args, "date_from", errors),
        "date_to": _date_arg(args, "date_to", errors),
        "page": _int_arg(args, "page", 1, 1, 100000, errors),
        "per_page": _int_arg(args, "per_page", 20, 1, 100, errors),
    }
    if errors:
        raise validation_error(errors, "Invalid query parameters.")
    return query
