import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import TransactionForm from "../components/TransactionForm";
import TransactionTable from "../components/TransactionTable";
import { deletePortfolio, getPortfolio } from "../api/portfolioApi";
import { createTransaction, deleteTransaction } from "../api/transactionApi";

function formatMoney(value, currency) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency || "KES",
  }).format(Number(value) || 0);
}

export default function PortfolioDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [portfolio, setPortfolio] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getPortfolio(id)
      .then(setPortfolio)
      .catch(() => setError("Portfolio not found"));
  }, [id]);

  async function refresh() {
    setPortfolio(await getPortfolio(id));
  }

  async function handleCreate(payload) {
    await createTransaction(id, payload);
    await refresh();
  }

  async function handleDeleteTransaction(transactionId) {
    await deleteTransaction(transactionId);
    await refresh();
  }

  async function handleDeletePortfolio() {
    await deletePortfolio(id);
    navigate("/portfolios");
  }

  if (error) {
    return <p className="form-error">{error}</p>;
  }
  if (!portfolio) {
    return <p className="page-loading">Loading portfolio…</p>;
  }

  const currency = portfolio.base_currency;
  const totals = portfolio.totals || {};

  return (
    <section>
      <header className="page-header">
        <div>
          <p className="eyebrow">
            <Link to="/portfolios">Portfolios</Link>
          </p>
          <h1>{portfolio.name}</h1>
          <p className="lede">
            {portfolio.client_name} · {currency}
          </p>
        </div>
        <button className="button button-ghost" type="button" onClick={handleDeletePortfolio}>
          Delete portfolio
        </button>
      </header>
      <div className="stat-grid">
        <article>
          <p>Market value</p>
          <strong>{formatMoney(totals.total_value, currency)}</strong>
        </article>
        <article>
          <p>Invested</p>
          <strong>{formatMoney(totals.total_invested, currency)}</strong>
        </article>
        <article>
          <p>Unrealized P/L</p>
          <strong>{formatMoney(totals.unrealized_pl, currency)}</strong>
        </article>
      </div>
      <h2>Holdings</h2>
      {portfolio.holdings?.length ? (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Instrument</th>
                <th>Quantity</th>
                <th>Average cost</th>
                <th>Last price</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.holdings.map((holding) => (
                <tr key={holding.instrument}>
                  <td>{holding.instrument}</td>
                  <td>{holding.net_quantity}</td>
                  <td>{formatMoney(holding.average_cost, currency)}</td>
                  <td>{formatMoney(holding.last_price, currency)}</td>
                  <td>{formatMoney(holding.total_value, currency)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="empty">No open positions yet.</p>
      )}
      <h2>Add a trade</h2>
      <div className="panel">
        <TransactionForm onSubmit={handleCreate} />
      </div>
      <h2>Transactions</h2>
      <TransactionTable transactions={portfolio.transactions} onDelete={handleDeleteTransaction} currency={currency} />
    </section>
  );
}
