import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { deletePortfolio, getPortfolio, getSummary, updatePortfolio } from "../api/portfolios";
import { createTransaction, deleteTransaction } from "../api/transactions";
import AllocationChart from "../components/AllocationChart";
import ConfirmDialog from "../components/ConfirmDialog";
import Dialog from "../components/Dialog";
import HoldingsTable from "../components/HoldingsTable";
import KpiStrip from "../components/KpiStrip";
import PortfolioForm from "../components/PortfolioForm";
import { ErrorState, LoadingState } from "../components/StateViews";
import TransactionForm from "../components/TransactionForm";
import TransactionsPanel from "../components/TransactionsPanel";
import { useAsync } from "../hooks/useAsync";
import { useDocumentTitle } from "../hooks/useDocumentTitle";
import { formatDate } from "../utils/format";

export default function PortfolioDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [version, setVersion] = useState(0);
  const [dialog, setDialog] = useState(null);
  const [txnToDelete, setTxnToDelete] = useState(null);

  const portfolio = useAsync((signal) => getPortfolio(id, signal), [id, version]);
  const summary = useAsync((signal) => getSummary(id, signal), [id, version]);
  useDocumentTitle(portfolio.data?.name ?? "Portfolio");

  const refresh = () => setVersion((v) => v + 1);
  const close = () => setDialog(null);

  if (portfolio.loading && !portfolio.data) return <LoadingState label="Loading portfolio…" />;
  if (portfolio.error) {
    return (
      <div className="panel">
        <ErrorState
          error={portfolio.error}
          title={portfolio.error.status === 404 ? "Portfolio not found" : "Couldn't load this portfolio"}
          onRetry={portfolio.error.status === 404 ? undefined : portfolio.reload}
        />
        <p style={{ textAlign: "center", paddingBottom: "var(--space-5)" }}>
          <Link to="/">Back to portfolios</Link>
        </p>
      </div>
    );
  }

  const p = portfolio.data;
  const currency = p.base_currency;

  return (
    <>
      <div className="page-head">
        <div>
          <p className="breadcrumb">
            <Link to="/">Portfolios</Link> / {p.name}
          </p>
          <h1>{p.name}</h1>
          <p className="page-head__sub">
            {p.client_name} · {currency} · created {formatDate(p.created_at)}
          </p>
        </div>
        <div className="page-head__actions">
          <button type="button" className="btn btn--secondary" onClick={() => setDialog("edit")}>
            Edit
          </button>
          <button type="button" className="btn btn--secondary" onClick={() => setDialog("delete-portfolio")}>
            Delete
          </button>
        </div>
      </div>

      {summary.loading && !summary.data && <LoadingState label="Calculating holdings…" />}
      {summary.error && <ErrorState error={summary.error} onRetry={summary.reload} title="Couldn't load the summary" />}
      {summary.data && (
        <>
          <KpiStrip totals={summary.data.totals} currency={currency} />
          <div className="split">
            <section className="panel" aria-labelledby="holdings-heading">
              <div className="panel__head">
                <h2 id="holdings-heading">Holdings</h2>
              </div>
              <HoldingsTable holdings={summary.data.holdings} currency={currency} />
            </section>
            <section className="panel" aria-labelledby="alloc-heading">
              <div className="panel__head">
                <h2 id="alloc-heading">Allocation by value</h2>
              </div>
              <AllocationChart holdings={summary.data.holdings} currency={currency} totalValue={summary.data.totals.total_value} />
            </section>
          </div>
        </>
      )}

      <TransactionsPanel
        portfolioId={id}
        currency={currency}
        version={version}
        onAdd={() => setDialog("add")}
        onDelete={setTxnToDelete}
      />

      <Dialog open={dialog === "add"} onClose={close} title="Add transaction">
        {dialog === "add" && (
          <TransactionForm
            currency={currency}
            onCancel={close}
            onSubmit={async (values) => {
              await createTransaction(id, values);
              close();
              refresh();
            }}
          />
        )}
      </Dialog>

      <Dialog open={dialog === "edit"} onClose={close} title="Edit portfolio">
        {dialog === "edit" && (
          <PortfolioForm
            initial={p}
            submitLabel="Save changes"
            onCancel={close}
            onSubmit={async (values) => {
              await updatePortfolio(id, values);
              close();
              refresh();
            }}
          />
        )}
      </Dialog>

      <ConfirmDialog
        open={dialog === "delete-portfolio"}
        title="Delete portfolio?"
        confirmLabel="Delete portfolio"
        onClose={close}
        onConfirm={async () => {
          await deletePortfolio(id);
          navigate("/", { replace: true });
        }}
      >
        <p>
          <strong>{p.name}</strong> and all {p.transaction_count} of its trades will be permanently deleted. This
          can't be undone.
        </p>
      </ConfirmDialog>

      <ConfirmDialog
        open={txnToDelete !== null}
        title="Delete transaction?"
        confirmLabel="Delete transaction"
        onClose={() => setTxnToDelete(null)}
        onConfirm={async () => {
          await deleteTransaction(txnToDelete.id);
          setTxnToDelete(null);
          refresh();
        }}
      >
        {txnToDelete && (
          <p>
            Delete the {txnToDelete.type} of {txnToDelete.quantity} {txnToDelete.instrument} on{" "}
            {formatDate(txnToDelete.trade_date)}? Holdings will be recalculated.
          </p>
        )}
      </ConfirmDialog>
    </>
  );
}
