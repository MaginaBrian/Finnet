import { useState } from "react";
import { createPortfolio, deletePortfolio, listPortfolios, updatePortfolio } from "../api/portfolios";
import ConfirmDialog from "../components/ConfirmDialog";
import Dialog from "../components/Dialog";
import PortfolioCard from "../components/PortfolioCard";
import PortfolioForm from "../components/PortfolioForm";
import { EmptyState, ErrorState, LoadingState } from "../components/StateViews";
import { useAsync } from "../hooks/useAsync";
import { useDocumentTitle } from "../hooks/useDocumentTitle";

export default function PortfoliosPage() {
  useDocumentTitle("Portfolios");
  const { data, error, loading, reload } = useAsync((signal) => listPortfolios(signal), []);
  const [editing, setEditing] = useState(null);
  const [deleting, setDeleting] = useState(null);

  const portfolios = data?.data ?? [];
  const closeEditor = () => setEditing(null);

  async function save(values) {
    if (editing === "new") await createPortfolio(values);
    else await updatePortfolio(editing.id, values);
    closeEditor();
    reload();
  }

  async function confirmDelete() {
    await deletePortfolio(deleting.id);
    setDeleting(null);
    reload();
  }

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Portfolios</h1>
          <p className="page-head__sub">Client portfolios you manage, valued at the last traded price.</p>
        </div>
        <div className="page-head__actions">
          <button type="button" className="btn btn--primary" onClick={() => setEditing("new")}>
            New portfolio
          </button>
        </div>
      </div>

      {loading && !data && <LoadingState label="Loading portfolios…" />}
      {error && <ErrorState error={error} onRetry={reload} title="Couldn't load portfolios" />}
      {data && portfolios.length === 0 && (
        <div className="panel">
          <EmptyState
            title="No portfolios yet"
            action={
              <button type="button" className="btn btn--primary" onClick={() => setEditing("new")}>
                Create your first portfolio
              </button>
            }
          >
            A portfolio groups one client's trades. Create one, then record buys and sells against it.
          </EmptyState>
        </div>
      )}
      {portfolios.length > 0 && (
        <ul className="card-grid">
          {portfolios.map((p) => (
            <PortfolioCard key={p.id} portfolio={p} onEdit={setEditing} onDelete={setDeleting} />
          ))}
        </ul>
      )}

      <Dialog open={editing !== null} onClose={closeEditor} title={editing === "new" ? "New portfolio" : "Edit portfolio"}>
        {editing !== null && (
          <PortfolioForm
            initial={editing === "new" ? undefined : editing}
            submitLabel={editing === "new" ? "Create portfolio" : "Save changes"}
            onSubmit={save}
            onCancel={closeEditor}
          />
        )}
      </Dialog>

      <ConfirmDialog
        open={deleting !== null}
        title="Delete portfolio?"
        confirmLabel="Delete portfolio"
        onConfirm={confirmDelete}
        onClose={() => setDeleting(null)}
      >
        <p>
          <strong>{deleting?.name}</strong> and all {deleting?.transaction_count} of its trades will be permanently
          deleted. This can't be undone.
        </p>
      </ConfirmDialog>
    </>
  );
}
