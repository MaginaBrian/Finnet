import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark">F</span>
        <div>
          <strong>Fintrack</strong>
          <p>Portfolio tracker</p>
        </div>
      </div>
      <nav className="side-nav">
        <NavLink to="/" end>
          Dashboard
        </NavLink>
        <NavLink to="/portfolios">Portfolios</NavLink>
      </nav>
    </aside>
  );
}
