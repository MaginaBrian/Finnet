import { useState } from "react";
import { splitApiError } from "../utils/apiErrors";
import { todayIso } from "../utils/format";
import { hasErrors, validateTransaction } from "../utils/validators";
import Field from "./Field";

export default function TransactionForm({ currency, onSubmit, onCancel }) {
  const [values, setValues] = useState({
    instrument: "",
    type: "BUY",
    quantity: "",
    unit_price: "",
    trade_date: todayIso(),
  });
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [busy, setBusy] = useState(false);

  const set = (field) => (e) => setValues((v) => ({ ...v, [field]: e.target.value }));

  async function handleSubmit(e) {
    e.preventDefault();
    const found = validateTransaction(values, todayIso());
    setErrors(found);
    setFormError("");
    if (hasErrors(found)) return;
    setBusy(true);
    try {
      await onSubmit({
        instrument: values.instrument.trim().toUpperCase(),
        type: values.type,
        quantity: Number(values.quantity),
        unit_price: Number(values.unit_price),
        trade_date: values.trade_date,
      });
    } catch (err) {
      const { fieldErrors, formError: message } = splitApiError(err);
      setErrors(fieldErrors);
      setFormError(message);
      setBusy(false);
    }
  }

  return (
    <form className="form" onSubmit={handleSubmit} noValidate>
      {formError && (
        <div className="alert" role="alert">
          {formError}
        </div>
      )}
      <div className="form__row">
        <Field label="Instrument" error={errors.instrument} hint="e.g. SCOM, KCB, EQTY, T-BILL-91">
          {(p) => <input {...p} className="input" value={values.instrument} onChange={set("instrument")} maxLength={20} autoFocus />}
        </Field>
        <Field label="Type" error={errors.type}>
          {(p) => (
            <select {...p} className="input" value={values.type} onChange={set("type")}>
              <option value="BUY">Buy</option>
              <option value="SELL">Sell</option>
            </select>
          )}
        </Field>
      </div>
      <div className="form__row">
        <Field label="Quantity" error={errors.quantity}>
          {(p) => <input {...p} className="input input--num" type="number" inputMode="decimal" min="0" step="any" value={values.quantity} onChange={set("quantity")} />}
        </Field>
        <Field label={`Unit price (${currency})`} error={errors.unit_price}>
          {(p) => <input {...p} className="input input--num" type="number" inputMode="decimal" min="0" step="any" value={values.unit_price} onChange={set("unit_price")} />}
        </Field>
      </div>
      <Field label="Trade date" error={errors.trade_date}>
        {(p) => <input {...p} className="input" type="date" value={values.trade_date} max={todayIso()} onChange={set("trade_date")} />}
      </Field>
      <div className="form__actions">
        <button type="button" className="btn btn--secondary" onClick={onCancel} disabled={busy}>
          Cancel
        </button>
        <button type="submit" className="btn btn--primary" disabled={busy}>
          {busy ? "Saving…" : "Record trade"}
        </button>
      </div>
    </form>
  );
}
