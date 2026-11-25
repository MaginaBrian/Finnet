import { useEffect, useState } from "react";
import PortfolioCard from "../components/PortfolioCard";
import { messageFrom } from "../api/axios";
import { createPortfolio, listPortfolios } from "../api/portfolioApi";

const emptyForm = { name: "", client_name: "", base_currency: "KES" };

export default function Portfolios() {
  const [portfolios, setPortfolios] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    listPortfolios()
      .then(setPortfolios)
      .catch(() => setError("Could not load portfolios"));
  }, []);

  function update(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      const created = await createPortfolio(form);
      setPortfolios((current) => [created, ...current]);
      setForm(emptyForm);
    } catch (err) {
      setError(messageFrom(err) || "Could not create the portfolio");
    } finally {
      setSaving(false);
    }
  }

  return (
    <section>
      <header className="page-header">
        <div>
          <p className="eyebrow">Accounts</p>
          <h1>Portfolios</h1>
        </div>
      </header>
      <form className="panel form-row" onSubmit={handleSubmit}>
        <label>
          Name
          <input name="name" value={form.name} onChange={update} required />
        </label>
        <label>
          Client
          <input name="client_name" value={form.client_name} onChange={update} required />
        </label>
        <label>
          Currency
          <select name="base_currency" value={form.base_currency} onChange={update}>
            <option value="KES">KES</option>
            <option value="USD">USD</option>
          </select>
        </label>
        <button className="button" type="submit" disabled={saving}>
          {saving ? "Adding…" : "Add portfolio"}
        </button>
      </form>
      {error ? <p className="form-error">{error}</p> : null}
      {portfolios.length ? (
        <div className="card-grid">
          {portfolios.map((portfolio) => (
            <PortfolioCard key={portfolio.id} portfolio={portfolio} />
          ))}
        </div>
      ) : (
        <p className="empty">No portfolios yet.</p>
      )}
    </section>
  );
}
