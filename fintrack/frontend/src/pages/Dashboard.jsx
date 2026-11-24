import { useEffect, useState } from "react";
import PortfolioCard from "../components/PortfolioCard";
import TransactionTable from "../components/TransactionTable";
import { fetchSummary } from "../api/portfolioApi";

function formatMoney(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number(value) || 0);
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchSummary()
      .then(setSummary)
      .catch(() => setError("Could not load the dashboard"));
  }, []);

  if (error) {
    return <p className="form-error">{error}</p>;
  }
  if (!summary) {
    return <p className="page-loading">Loading dashboard…</p>;
  }

  return (
    <section>
      <header className="page-header">
        <div>
          <p className="eyebrow">Overview</p>
          <h1>Dashboard</h1>
        </div>
      </header>
      <div className="stat-grid">
        <article>
          <p>Net worth</p>
          <strong>{formatMoney(summary.net_worth)}</strong>
        </article>
        <article>
          <p>Cash</p>
          <strong>{formatMoney(summary.cash)}</strong>
        </article>
        <article>
          <p>Holdings at cost</p>
          <strong>{formatMoney(summary.holdings_value)}</strong>
        </article>
      </div>
      <h2>Portfolios</h2>
      {summary.portfolios.length ? (
        <div className="card-grid">
          {summary.portfolios.map((portfolio) => (
            <PortfolioCard key={portfolio.id} portfolio={portfolio} />
          ))}
        </div>
      ) : (
        <p className="empty">Create a portfolio to start tracking transactions.</p>
      )}
      <h2>Recent activity</h2>
      <TransactionTable transactions={summary.recent_transactions} />
    </section>
  );
}
