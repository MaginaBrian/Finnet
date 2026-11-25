import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import Field from "../components/Field";
import { useAuth } from "../context/AuthContext";
import { useDocumentTitle } from "../hooks/useDocumentTitle";
import { hasErrors, validateLogin } from "../utils/validators";
import { splitApiError } from "../utils/apiErrors";

const DEMO = { username: "demo", password: "Demo@12345" };

export default function LoginPage() {
  useDocumentTitle("Sign in");
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [values, setValues] = useState({ username: "", password: "" });
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [busy, setBusy] = useState(false);

  if (isAuthenticated) return <Navigate to="/" replace />;

  const set = (field) => (e) => setValues((v) => ({ ...v, [field]: e.target.value }));

  async function handleSubmit(e) {
    e.preventDefault();
    const found = validateLogin(values);
    setErrors(found);
    setFormError("");
    if (hasErrors(found)) return;
    setBusy(true);
    try {
      await login(values.username.trim(), values.password);
      navigate(location.state?.from ?? "/", { replace: true });
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
        <h1>Sign in to FinTrack</h1>
        <p className="auth__alt">Use your analyst account to manage client portfolios.</p>
      </div>
      <form className="form" onSubmit={handleSubmit} noValidate>
        {formError && (
          <div className="alert" role="alert">
            {formError}
          </div>
        )}
        <Field label="Username" error={errors.username}>
          {(p) => <input {...p} className="input" autoComplete="username" value={values.username} onChange={set("username")} autoFocus />}
        </Field>
        <Field label="Password" error={errors.password}>
          {(p) => <input {...p} className="input" type="password" autoComplete="current-password" value={values.password} onChange={set("password")} />}
        </Field>
        <button type="submit" className="btn btn--primary" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
      <div className="demo-hint">
        <p>
          Reviewing this project? Demo login: <code>{DEMO.username}</code> / <code>{DEMO.password}</code>
        </p>
        <button type="button" className="btn btn--link" onClick={() => setValues(DEMO)}>
          Fill in demo login
        </button>
      </div>
      <p className="auth__alt">
        New analyst? <Link to="/register">Create an account</Link>
      </p>
    </AuthLayout>
  );
}
