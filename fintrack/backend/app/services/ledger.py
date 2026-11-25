"""Pure portfolio maths: replay transactions into positions.

Method: weighted-average cost. A SELL reduces the cost basis at the current
average cost and books realised P/L against the sale price. Transactions are
replayed in trade-date order (BUYs before SELLs on the same day), so a
back-dated trade is validated against the history it would actually sit in.
"""
from dataclasses import dataclass
from decimal import Decimal

ZERO = Decimal("0")
_FAR_FUTURE_ID = 10**12


class InsufficientHoldings(Exception):
    def __init__(self, instrument, trade_date, held, requested):
        super().__init__(f"Cannot sell {requested} {instrument}: only {held} held.")
        self.instrument = instrument
        self.trade_date = trade_date
        self.held = held
        self.requested = requested


@dataclass
class Position:
    quantity: Decimal = ZERO
    cost: Decimal = ZERO  # total cost basis of what is still held
    realized_pl: Decimal = ZERO
    last_price: Decimal = ZERO

    @property
    def average_cost(self) -> Decimal:
        return self.cost / self.quantity if self.quantity else ZERO


def _sort_key(txn):
    return (txn.trade_date, 0 if txn.type == "BUY" else 1, txn.id if txn.id is not None else _FAR_FUTURE_ID)


def replay(transactions) -> dict[str, Position]:
    """Replay transactions in order. Raises InsufficientHoldings on an oversell."""
    positions: dict[str, Position] = {}
    for txn in sorted(transactions, key=_sort_key):
        pos = positions.setdefault(txn.instrument, Position())
        qty, price = Decimal(txn.quantity), Decimal(txn.unit_price)
        if txn.type == "BUY":
            pos.quantity += qty
            pos.cost += qty * price
        else:
            if qty > pos.quantity:
                raise InsufficientHoldings(txn.instrument, txn.trade_date, pos.quantity, qty)
            avg = pos.average_cost
            pos.realized_pl += qty * (price - avg)
            pos.cost -= qty * avg
            pos.quantity -= qty
            if pos.quantity == 0:
                pos.cost = ZERO
        pos.last_price = price
    return positions


def _money(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.0001")))


def _pct(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01")))


def build_summary(positions: dict[str, Position], currency: str) -> dict:
    """Turn positions into the JSON shape returned by the summary endpoint."""
    open_positions = {k: p for k, p in positions.items() if p.quantity > 0}
    total_invested = sum((p.cost for p in open_positions.values()), ZERO)
    total_value = sum((p.quantity * p.last_price for p in open_positions.values()), ZERO)
    realized = sum((p.realized_pl for p in positions.values()), ZERO)
    unrealized = total_value - total_invested

    holdings = []
    for instrument, pos in sorted(open_positions.items()):
        value = pos.quantity * pos.last_price
        pl = value - pos.cost
        holdings.append(
            {
                "instrument": instrument,
                "net_quantity": _money(pos.quantity),
                "average_cost": _money(pos.average_cost),
                "total_invested": _money(pos.cost),
                "last_price": _money(pos.last_price),
                "total_value": _money(value),
                "unrealized_pl": _money(pl),
                "unrealized_pl_pct": _pct(pl / pos.cost * 100) if pos.cost else 0.0,
                "allocation_pct": _pct(value / total_value * 100) if total_value else 0.0,
            }
        )

    return {
        "base_currency": currency,
        "valuation_basis": "last_trade_price",
        "holdings": holdings,
        "totals": {
            "total_invested": _money(total_invested),
            "total_value": _money(total_value),
            "unrealized_pl": _money(unrealized),
            "unrealized_pl_pct": _pct(unrealized / total_invested * 100) if total_invested else 0.0,
            "realized_pl": _money(realized),
        },
    }


def summarize(transactions, currency: str) -> dict:
    return build_summary(replay(transactions), currency)
