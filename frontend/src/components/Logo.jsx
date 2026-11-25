import { Link } from "react-router-dom";

export function LogoMark({ className = "logo__mark" }) {
  return (
    <svg className={className} viewBox="0 0 32 32" aria-hidden="true" focusable="false">
      <rect width="32" height="32" rx="7" fill="#102a4c" stroke="#2a4a78" />
      <rect x="7" y="17" width="4" height="8" rx="1" fill="#ffffff" />
      <rect x="14" y="12" width="4" height="13" rx="1" fill="#ffffff" />
      <rect x="21" y="7" width="4" height="18" rx="1" fill="#f5b301" />
    </svg>
  );
}

export default function Logo({ to = "/" }) {
  const content = (
    <>
      <LogoMark />
      <span className="logo__text">
        <span className="logo__name">FinTrack</span>
        <span className="logo__by">by Finnet Technologies</span>
      </span>
    </>
  );
  return to ? (
    <Link to={to} className="logo" aria-label="FinTrack by Finnet Technologies, home">
      {content}
    </Link>
  ) : (
    <span className="logo">{content}</span>
  );
}
