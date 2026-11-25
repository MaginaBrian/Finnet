import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import Field from "../components/Field";
import { useAuth } from "../context/AuthContext";
import { useDocumentTitle } from "../hooks/useDocumentTitle";
import { splitApiError } from "../utils/apiErrors";
import { hasErrors, validateRegister } from "../utils/validators";

export default function RegisterPage() {
  useDocumentTitle("Create account");
  const { register, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [values, setValues] = useState({ full_name: "", username: "", password: "", confirm: "" });
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [busy, setBusy] = useState(false);

  if (isAuthenticated) return <Navigate to="/" replace />;

  const set = (field) => (e) => setValues((v) => ({ ...v, [field]: e.target.value }));

  async function handleSubmit(e) {
    e.preventDefault();
    const found = validateRegister(values);
    setErrors(found);
    setFormError("");
    if (hasErrors(found)) return;
    setBusy(true);
    try {
      await register(values.username.trim(), values.password, values.full_name.trim());
      navigate("/", { replace: true });
    } catch (err) {
      const { fieldErrors, formError: message } = splitApiError(err);
      setErrors(fieldErrors);
      setFormError(message);
      setBusy(false);
    }
  }

  return (
    <AuthLayout>
      <div>
        <h1>Create your analyst account</h1>
        <p className="auth__alt">You'll be signed in straight away.</p>
      </div>
      <form className="form" onSubmit={handleSubmit} noValidate>
        {formError && (
          <div className="alert" role="alert">
            {formError}
          </div>
        )}
        <Field label="Full name (optional)" error={errors.full_name}>
          {(p) => <input {...p} className="input" autoComplete="name" value={values.full_name} onChange={set("full_name")} autoFocus />}
        </Field>
        <Field label="Username" error={errors.username}>
          {(p) => <input {...p} className="input" autoComplete="username" value={values.username} onChange={set("username")} />}
        </Field>
        <Field label="Password" error={errors.password} hint="At least 8 characters.">
          {(p) => <input {...p} className="input" type="password" autoComplete="new-password" value={values.password} onChange={set("password")} />}
        </Field>
        <Field label="Confirm password" error={errors.confirm}>
          {(p) => <input {...p} className="input" type="password" autoComplete="new-password" value={values.confirm} onChange={set("confirm")} />}
        </Field>
        <button type="submit" className="btn btn--primary" disabled={busy}>
          {busy ? "Creating account…" : "Create account"}
        </button>
      </form>
      <p className="auth__alt">
        Already registered? <Link to="/login">Sign in</Link>
      </p>
    </AuthLayout>
  );
}
