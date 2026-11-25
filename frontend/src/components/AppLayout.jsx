import { Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Logo from "./Logo";

export default function AppLayout() {
  const { user, logout } = useAuth();
  return (
    <>
      <a className="skip-link" href="#main">
        Skip to main content
      </a>
      <header className="app-header">
        <div className="app-header__inner">
          <Logo />
          <div className="app-header__user">
            <span className="app-header__name">{user?.full_name || user?.username}</span>
            <button type="button" className="btn btn--ghost btn--sm" onClick={logout}>
              Sign out
            </button>
          </div>
        </div>
      </header>
      <main id="main" className="page" tabIndex={-1}>
        <Outlet />
      </main>
    </>
  );
}
