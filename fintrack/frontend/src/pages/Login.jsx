import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { messageFrom } from "../api/axios";
import { useAuth } from "../hooks/useAuth";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  function update(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      await login(form.username, form.password);
      navigate("/");
    } catch (err) {
      setError(messageFrom(err) || "Could not sign in");
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="auth-screen">
      <form className="auth-card" onSubmit={handleSubmit}>
        <p className="eyebrow">Fintrack</p>
        <h1>Welcome back</h1>
        <p className="lede">Sign in to see client portfolios and positions.</p>
        <label>
          Username
          <input name="username" value={form.username} onChange={update} autoComplete="username" required />
        </label>
        <label>
          Password
          <input name="password" type="password" value={form.password} onChange={update} required />
        </label>
        {error ? <p className="form-error">{error}</p> : null}
        <button className="button" type="submit" disabled={saving}>
          {saving ? "Signing in…" : "Sign in"}
        </button>
        <p className="auth-switch">
          New here? <Link to="/register">Create an account</Link>
        </p>
      </form>
    </main>
  );
}
