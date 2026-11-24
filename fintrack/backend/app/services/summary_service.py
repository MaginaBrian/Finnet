from decimal import Decimal

from app.models.portfolio import Portfolio

ZERO = Decimal("0")
KIND_BUY = "buy"
KIND_SELL = "sell"
KIND_DEPOSIT = "deposit"
KIND_WITHDRAWAL = "withdrawal"
KIND_DIVIDEND = "dividend"
SHARE_KINDS = {KIND_BUY, KIND_SELL}
CASH_KINDS = {KIND_DEPOSIT, KIND_WITHDRAWAL, KIND_DIVIDEND}


def _money(value):
    return float(Decimal(value).quantize(Decimal("0.01")))


def _quantity(value):
    return float(Decimal(value).quantize(Decimal("0.0001")))


def value_transactions(transactions):
    cash = ZERO
    positions = {}

    ordered = sorted(transactions, key=lambda tx: (tx.occurred_at, tx.id is None, tx.id or 0))
    for tx in ordered:
        amount = Decimal(tx.amount or 0)
        if tx.kind == KIND_DEPOSIT or tx.kind == KIND_DIVIDEND:
            cash += amount
        elif tx.kind == KIND_WITHDRAWAL:
            cash -= amount
        elif tx.kind == KIND_BUY:
            cash -= amount
            _apply_position(positions, tx.symbol, Decimal(tx.quantity or 0), amount)
        elif tx.kind == KIND_SELL:
            cash += amount
            _apply_position(positions, tx.symbol, -Decimal(tx.quantity or 0), -_cost_removed(positions, tx))

    holdings = []
    holdings_value = ZERO
    for symbol, position in sorted(positions.items()):
        quantity = position["quantity"]
        cost = position["cost"]
        if quantity == 0 and cost == 0:
            continue
        holdings_value += cost
        average = (cost / quantity) if quantity else ZERO
        holdings.append(
            {
                "symbol": symbol,
                "quantity": _quantity(quantity),
                "cost": _money(cost),
                "average_cost": _money(average),
            }
        )

    return {
        "cash": _money(cash),
        "holdings_value": _money(holdings_value),
        "net_worth": _money(cash + holdings_value),
        "holdings": holdings,
    }


def _apply_position(positions, symbol, quantity_delta, cost_delta):
    position = positions.setdefault(symbol, {"quantity": ZERO, "cost": ZERO})
    position["quantity"] += quantity_delta
    position["cost"] += cost_delta


def _cost_removed(positions, tx):
    position = positions.get(tx.symbol) or {"quantity": ZERO, "cost": ZERO}
    quantity = Decimal(tx.quantity or 0)
    if position["quantity"] <= 0:
        return Decimal(tx.amount or 0)
    average = position["cost"] / position["quantity"]
    return average * quantity


def overview_for_user(user):
    portfolios = (
        Portfolio.query.filter_by(user_id=user.id)
        .order_by(Portfolio.created_at.desc())
        .all()
    )
    cards = []
    recent = []
    cash = ZERO
    holdings_value = ZERO

    for portfolio in portfolios:
        valuation = value_transactions(portfolio.transactions)
        cash += Decimal(str(valuation["cash"]))
        holdings_value += Decimal(str(valuation["holdings_value"]))
        cards.append({**portfolio.to_dict(), **valuation})
        recent.extend(portfolio.transactions)

    recent.sort(key=lambda tx: (tx.occurred_at, tx.id or 0), reverse=True)
    return {
        "cash": _money(cash),
        "holdings_value": _money(holdings_value),
        "net_worth": _money(cash + holdings_value),
        "portfolio_count": len(cards),
        "portfolios": cards,
        "recent_transactions": [tx.to_dict() for tx in recent[:8]],
    }


def holdings_for_portfolio(portfolio):
    return value_transactions(portfolio.transactions)
