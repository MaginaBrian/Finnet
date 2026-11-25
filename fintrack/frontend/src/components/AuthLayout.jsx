import Logo from "./Logo";

export default function AuthLayout({ children }) {
  return (
    <div className="auth">
      <aside className="auth__brand">
        <Logo to={null} />
        <div>
          <p className="auth__headline">Every position and trade, in one place.</p>
          <p className="auth__lede">
            Record client trades, see current holdings and track performance across KES and USD portfolios.
          </p>
        </div>
        <p className="auth__foot">Internal tool for Finnet investment operations.</p>
      </aside>
      <main id="main" className="auth__panel">
        <div className="auth__card">{children}</div>
      </main>
    </div>
  );
}
