import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { messageFrom } from "../api/axios";
import { useAuth } from "../hooks/useAuth";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", fullName: "", password: "" });
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
      await register(form.username, form.fullName, form.password);
      navigate("/");
    } catch (err) {
      setError(messageFrom(err) || "Could not create the account");
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="auth-screen">
      <form className="auth-card" onSubmit={handleSubmit}>
        <p className="eyebrow">Fintrack</p>
        <h1>Create your account</h1>
        <p className="lede">Track buys and sells for KES and USD portfolios.</p>
        <label>
          Username
          <input name="username" value={form.username} onChange={update} minLength={3} required />
        </label>
        <label>
          Full name
          <input name="fullName" value={form.fullName} onChange={update} />
        </label>
        <label>
          Password
          <input name="password" type="password" value={form.password} onChange={update} minLength={8} required />
        </label>
        {error ? <p className="form-error">{error}</p> : null}
        <button className="button" type="submit" disabled={saving}>
          {saving ? "Creating…" : "Create account"}
        </button>
        <p className="auth-switch">
          Already registered? <Link to="/login">Sign in</Link>
        </p>
      </form>
    </main>
  );
}
