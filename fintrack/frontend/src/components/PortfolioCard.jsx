import { Link } from "react-router-dom";

function formatMoney(value, currency) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency || "KES",
  }).format(Number(value) || 0);
}

export default function PortfolioCard({ portfolio }) {
  return (
    <Link className="portfolio-card" to={`/portfolios/${portfolio.id}`}>
      <div>
        <h3>{portfolio.name}</h3>
        <p>
          {portfolio.client_name} · {portfolio.base_currency}
        </p>
      </div>
      <dl>
        <div>
          <dt>Market value</dt>
          <dd>{formatMoney(portfolio.totals?.total_value, portfolio.base_currency)}</dd>
        </div>
        <div>
          <dt>Invested</dt>
          <dd>{formatMoney(portfolio.totals?.total_invested, portfolio.base_currency)}</dd>
        </div>
        <div>
          <dt>Unrealized</dt>
          <dd>{formatMoney(portfolio.totals?.unrealized_pl, portfolio.base_currency)}</dd>
        </div>
      </dl>
    </Link>
  );
}
