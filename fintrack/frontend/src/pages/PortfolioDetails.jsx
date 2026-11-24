import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import TransactionForm from "../components/TransactionForm";
import TransactionTable from "../components/TransactionTable";
import { deletePortfolio, getPortfolio } from "../api/portfolioApi";
import { createTransaction, deleteTransaction } from "../api/transactionApi";

function formatMoney(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
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

  return (
    <section>
      <header className="page-header">
        <div>
          <p className="eyebrow">
            <Link to="/portfolios">Portfolios</Link>
          </p>
          <h1>{portfolio.name}</h1>
          <p className="lede">{portfolio.description}</p>
        </div>
        <button className="button button-ghost" type="button" onClick={handleDeletePortfolio}>
          Delete portfolio
        </button>
      </header>
      <div className="stat-grid">
        <article>
          <p>Net worth</p>
          <strong>{formatMoney(portfolio.net_worth)}</strong>
        </article>
        <article>
          <p>Cash</p>
          <strong>{formatMoney(portfolio.cash)}</strong>
        </article>
        <article>
          <p>Holdings at cost</p>
          <strong>{formatMoney(portfolio.holdings_value)}</strong>
        </article>
      </div>
      <h2>Holdings</h2>
      {portfolio.holdings?.length ? (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Average cost</th>
                <th>Cost basis</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.holdings.map((holding) => (
                <tr key={holding.symbol}>
                  <td>{holding.symbol}</td>
                  <td>{holding.quantity}</td>
                  <td>{formatMoney(holding.average_cost)}</td>
                  <td>{formatMoney(holding.cost)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="empty">No share positions yet.</p>
      )}
      <h2>Add a transaction</h2>
      <div className="panel">
        <TransactionForm onSubmit={handleCreate} />
      </div>
      <h2>Transactions</h2>
      <TransactionTable transactions={portfolio.transactions} onDelete={handleDeleteTransaction} />
    </section>
  );
}
