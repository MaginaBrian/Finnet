import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <header className="navbar">
      <div>
        <p className="eyebrow">Signed in</p>
        <strong>{user?.name}</strong>
      </div>
      <button className="button button-ghost" type="button" onClick={handleLogout}>
        Log out
      </button>
    </header>
  );
}
