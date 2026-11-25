import { formatMoney, formatSignedPercent, plClass } from "../utils/format";
import Pl from "./Pl";

export default function KpiStrip({ totals, currency }) {
  return (
    <section className="kpis" aria-label="Portfolio performance summary">
      <div className="panel kpi">
        <p className="kpi__label">Total value</p>
        <p className="kpi__value">{formatMoney(totals.total_value, currency)}</p>
      </div>
      <div className="panel kpi">
        <p className="kpi__label">Total invested</p>
        <p className="kpi__value">{formatMoney(totals.total_invested, currency)}</p>
      </div>
      <div className="panel kpi">
        <p className="kpi__label">Unrealised P/L</p>
        <p className="kpi__value">
          <Pl value={totals.unrealized_pl} currency={currency} />
        </p>
        <p className={`kpi__sub pl ${plClass(totals.unrealized_pl_pct)}`}>
          {formatSignedPercent(totals.unrealized_pl_pct)} on cost
        </p>
      </div>
      <div className="panel kpi">
        <p className="kpi__label">Realised P/L</p>
        <p className="kpi__value">
          <Pl value={totals.realized_pl} currency={currency} />
        </p>
      </div>
    </section>
  );
}
