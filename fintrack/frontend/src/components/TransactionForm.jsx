import { useState } from "react";
import { messageFrom } from "../api/axios";

const emptyForm = {
  type: "BUY",
  instrument: "",
  quantity: "",
  unit_price: "",
  trade_date: new Date().toISOString().slice(0, 10),
};

export default function TransactionForm({ onSubmit }) {
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  function update(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSaving(true);
    try {
      await onSubmit(form);
      setForm((current) => ({ ...emptyForm, type: current.type, trade_date: current.trade_date }));
    } catch (err) {
      setError(messageFrom(err) || "Could not save the transaction");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="stack-form" onSubmit={handleSubmit}>
      <div className="form-grid">
        <label>
          Type
          <select name="type" value={form.type} onChange={update}>
            <option value="BUY">Buy</option>
            <option value="SELL">Sell</option>
          </select>
        </label>
        <label>
          Date
          <input type="date" name="trade_date" value={form.trade_date} onChange={update} required />
        </label>
        <label>
          Instrument
          <input name="instrument" value={form.instrument} onChange={update} required />
        </label>
        <label>
          Quantity
          <input name="quantity" value={form.quantity} onChange={update} inputMode="decimal" required />
        </label>
        <label>
          Unit price
          <input name="unit_price" value={form.unit_price} onChange={update} inputMode="decimal" required />
        </label>
      </div>
      {error ? <p className="form-error">{error}</p> : null}
      <button className="button" type="submit" disabled={saving}>
        {saving ? "Saving…" : "Add trade"}
      </button>
    </form>
  );
}
