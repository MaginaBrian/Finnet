import { Link } from "react-router-dom";
import { formatDate, formatMoney } from "../utils/format";
import Pl from "./Pl";

export default function PortfolioCard({ portfolio, onEdit, onDelete }) {
  const { totals, base_currency: currency } = portfolio;
  return (
    <li>
      <article className="panel pcard">
        <Link to={`/portfolios/${portfolio.id}`} className="pcard__main">
          <div>
            <h2 className="pcard__name">{portfolio.name}</h2>
            <p className="pcard__client">{portfolio.client_name}</p>
          </div>
          <div>
            <p className="pcard__value">{formatMoney(totals.total_value, currency)}</p>
            <p className="pcard__client">
              <Pl value={totals.unrealized_pl} currency={currency} percent={totals.unrealized_pl_pct} /> unrealised
            </p>
          </div>
          <p className="pcard__meta">
            <span className="badge">{currency}</span>
            <span>
              {portfolio.transaction_count} {portfolio.transaction_count === 1 ? "trade" : "trades"} · created{" "}
              {formatDate(portfolio.created_at)}
            </span>
          </p>
        </Link>
        <div className="pcard__actions">
          <button type="button" className="btn btn--secondary btn--sm" onClick={() => onEdit(portfolio)}>
            Edit<span className="visually-hidden"> {portfolio.name}</span>
          </button>
          <button type="button" className="btn btn--secondary btn--sm" onClick={() => onDelete(portfolio)}>
            Delete<span className="visually-hidden"> {portfolio.name}</span>
          </button>
        </div>
      </article>
    </li>
  );
}
