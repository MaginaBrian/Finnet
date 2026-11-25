import { useState } from "react";
import { splitApiError } from "../utils/apiErrors";
import { hasErrors, validatePortfolio } from "../utils/validators";
import Field from "./Field";

const EMPTY = { name: "", client_name: "", base_currency: "KES" };

export default function PortfolioForm({ initial, submitLabel, onSubmit, onCancel }) {
  const [values, setValues] = useState({ ...EMPTY, ...initial });
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [busy, setBusy] = useState(false);

  const set = (field) => (e) => setValues((v) => ({ ...v, [field]: e.target.value }));

  async function handleSubmit(e) {
    e.preventDefault();
    const found = validatePortfolio(values);
    setErrors(found);
    setFormError("");
    if (hasErrors(found)) return;
    setBusy(true);
    try {
      await onSubmit({
        name: values.name.trim(),
        client_name: values.client_name.trim(),
        base_currency: values.base_currency,
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
      <Field label="Portfolio name" error={errors.name}>
        {(p) => <input {...p} className="input" value={values.name} onChange={set("name")} maxLength={100} autoFocus />}
      </Field>
      <Field label="Client name" error={errors.client_name}>
        {(p) => <input {...p} className="input" value={values.client_name} onChange={set("client_name")} maxLength={100} />}
      </Field>
      <Field label="Base currency" error={errors.base_currency}>
        {(p) => (
          <select {...p} className="input" value={values.base_currency} onChange={set("base_currency")}>
            <option value="KES">KES: Kenyan shilling</option>
            <option value="USD">USD: US dollar</option>
          </select>
        )}
      </Field>
      <div className="form__actions">
        <button type="button" className="btn btn--secondary" onClick={onCancel} disabled={busy}>
          Cancel
        </button>
        <button type="submit" className="btn btn--primary" disabled={busy}>
          {busy ? "Saving…" : submitLabel}
        </button>
      </div>
    </form>
  );
}
