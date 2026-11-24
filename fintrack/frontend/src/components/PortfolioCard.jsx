import { Link } from "react-router-dom";

function formatMoney(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number(value) || 0);
}

export default function PortfolioCard({ portfolio }) {
  return (
    <Link className="portfolio-card" to={`/portfolios/${portfolio.id}`}>
      <div>
        <h3>{portfolio.name}</h3>
        <p>{portfolio.description || "No description"}</p>
      </div>
      <dl>
        <div>
          <dt>Net worth</dt>
          <dd>{formatMoney(portfolio.net_worth)}</dd>
        </div>
        <div>
          <dt>Cash</dt>
          <dd>{formatMoney(portfolio.cash)}</dd>
        </div>
        <div>
          <dt>Holdings</dt>
          <dd>{formatMoney(portfolio.holdings_value)}</dd>
        </div>
      </dl>
    </Link>
  );
}
