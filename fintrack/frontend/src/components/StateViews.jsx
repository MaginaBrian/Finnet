export function LoadingState({ label = "Loading…" }) {
  return (
    <div className="state" role="status" aria-live="polite">
      <div className="spinner" aria-hidden="true" />
      <p>{label}</p>
    </div>
  );
}

export function EmptyState({ title, children, action }) {
  return (
    <div className="state">
      <h3 className="state__title">{title}</h3>
      {children && <p>{children}</p>}
      {action}
    </div>
  );
}

export function ErrorState({ error, onRetry, title = "We couldn't load this" }) {
  return (
    <div className="state" role="alert">
      <h3 className="state__title">{title}</h3>
      <p>{error?.message ?? "Something went wrong."}</p>
      {onRetry && (
        <button type="button" className="btn btn--secondary" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}
