import { useState } from "react";

const CASH_KINDS = ["deposit", "withdrawal", "dividend"];

const emptyForm = {
  kind: "buy",
  symbol: "",
  quantity: "",
  price: "",
  amount: "",
  occurred_at: new Date().toISOString().slice(0, 10),
  notes: "",
};

export default function TransactionForm({ onSubmit }) {
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const isCash = CASH_KINDS.includes(form.kind);

  function update(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSaving(true);
    const payload = {
      kind: form.kind,
      occurred_at: form.occurred_at,
      notes: form.notes,
    };
    if (isCash) {
      payload.amount = form.amount;
    } else {
      payload.symbol = form.symbol;
      payload.quantity = form.quantity;
      payload.price = form.price;
    }
    try {
      await onSubmit(payload);
      setForm((current) => ({ ...emptyForm, kind: current.kind, occurred_at: current.occurred_at }));
    } catch (err) {
      setError(err.response?.data?.error || "Could not save the transaction");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="stack-form" onSubmit={handleSubmit}>
      <div className="form-grid">
        <label>
          Type
          <select name="kind" value={form.kind} onChange={update}>
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
            <option value="deposit">Deposit</option>
            <option value="withdrawal">Withdrawal</option>
            <option value="dividend">Dividend</option>
          </select>
        </label>
        <label>
          Date
          <input type="date" name="occurred_at" value={form.occurred_at} onChange={update} required />
        </label>
        {isCash ? (
          <label>
            Amount
            <input name="amount" value={form.amount} onChange={update} inputMode="decimal" required />
          </label>
        ) : (
          <>
            <label>
              Symbol
              <input name="symbol" value={form.symbol} onChange={update} required />
            </label>
            <label>
              Quantity
              <input name="quantity" value={form.quantity} onChange={update} inputMode="decimal" required />
            </label>
            <label>
              Price
              <input name="price" value={form.price} onChange={update} inputMode="decimal" required />
            </label>
          </>
        )}
        <label className="span-2">
          Notes
          <input name="notes" value={form.notes} onChange={update} />
        </label>
      </div>
      {error ? <p className="form-error">{error}</p> : null}
      <button className="button" type="submit" disabled={saving}>
        {saving ? "Saving…" : "Add transaction"}
      </button>
    </form>
  );
}
