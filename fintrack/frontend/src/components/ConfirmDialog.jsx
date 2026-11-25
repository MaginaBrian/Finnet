import { useEffect, useState } from "react";
import Dialog from "./Dialog";

/** Confirmation before destructive actions. `onConfirm` may throw to show an error. */
export default function ConfirmDialog({ open, title, confirmLabel = "Delete", onConfirm, onClose, children }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (open) {
      setBusy(false);
      setError("");
    }
  }, [open]);

  async function handleConfirm() {
    setBusy(true);
    setError("");
    try {
      await onConfirm();
    } catch (err) {
      setError(err?.message ?? "That didn't work. Try again.");
      setBusy(false);
    }
  }

  return (
    <Dialog open={open} onClose={onClose} title={title}>
      <div className="form">
        <div>{children}</div>
        {error && (
          <div className="alert" role="alert">
            {error}
          </div>
        )}
        <div className="form__actions">
          <button type="button" className="btn btn--secondary" onClick={onClose} disabled={busy}>
            Cancel
          </button>
          <button type="button" className="btn btn--danger" onClick={handleConfirm} disabled={busy}>
            {busy ? "Working…" : confirmLabel}
          </button>
        </div>
      </div>
    </Dialog>
  );
}
