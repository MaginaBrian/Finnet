import { useEffect, useId, useRef } from "react";

export default function Dialog({ open, onClose, title, children }) {
  const ref = useRef(null);
  const titleId = useId();

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (open && !el.open) el.showModal();
    if (!open && el.open) el.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      className="dialog"
      aria-labelledby={titleId}
      onClose={onClose}
      onMouseDown={(e) => e.target === ref.current && onClose()}
    >
      {open && (
        <>
          <div className="dialog__head">
            <h2 id={titleId}>{title}</h2>
          </div>
          <div className="dialog__body">{children}</div>
        </>
      )}
    </dialog>
  );
}
