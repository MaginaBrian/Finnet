import { useState } from "react";
import { exportTransactionsCsv, listTransactions } from "../api/transactions";
import { useAsync } from "../hooks/useAsync";
import Field from "./Field";
import { EmptyState, ErrorState, LoadingState } from "./StateViews";
import TransactionTable from "./TransactionTable";

const NO_FILTERS = { instrument: "", type: "", date_from: "", date_to: "" };
const PER_PAGE = 10;

export default function TransactionsPanel({ portfolioId, currency, version, onAdd, onDelete }) {
  const [draft, setDraft] = useState(NO_FILTERS);
  const [filters, setFilters] = useState(NO_FILTERS);
  const [sort, setSort] = useState("trade_date");
  const [order, setOrder] = useState("desc");
  const [page, setPage] = useState(1);
  const [exportError, setExportError] = useState("");

  const query = { ...filters, sort, order };
  const { data, error, loading, reload } = useAsync(
    (signal) => listTransactions(portfolioId, { ...query, page, per_page: PER_PAGE }, signal),
    [portfolioId, JSON.stringify(query), page, version],
  );

  const filtered = Object.values(filters).some(Boolean);
  const set = (field) => (e) => setDraft((d) => ({ ...d, [field]: e.target.value }));

  function applyFilters(e) {
    e.preventDefault();
    setFilters(draft);
    setPage(1);
  }

  function clearFilters() {
    setDraft(NO_FILTERS);
    setFilters(NO_FILTERS);
    setPage(1);
  }

  function handleSort(key) {
    if (key === sort) setOrder((o) => (o === "asc" ? "desc" : "asc"));
    else {
      setSort(key);
      setOrder(key === "trade_date" ? "desc" : "asc");
    }
    setPage(1);
  }

  async function handleExport() {
    setExportError("");
    try {
      const blob = await exportTransactionsCsv(portfolioId, query);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `portfolio-${portfolioId}-transactions.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setExportError(err.message);
    }
  }

  const meta = data?.meta;
  const transactions = data?.data ?? [];

  return (
    <section className="panel" aria-labelledby="txn-heading">
      <div className="panel__head">
        <h2 id="txn-heading">Transactions</h2>
        <div className="page-head__actions">
          <button type="button" className="btn btn--secondary btn--sm" onClick={handleExport}>
            Export CSV
          </button>
          <button type="button" className="btn btn--primary btn--sm" onClick={onAdd}>
            Add transaction
          </button>
        </div>
      </div>

      <form className="filters" onSubmit={applyFilters} aria-label="Filter transactions">
        <Field label="Instrument">{(p) => <input {...p} className="input" value={draft.instrument} onChange={set("instrument")} placeholder="e.g. SCOM" />}</Field>
        <Field label="Type">
          {(p) => (
            <select {...p} className="input" value={draft.type} onChange={set("type")}>
              <option value="">All</option>
              <option value="BUY">Buy</option>
              <option value="SELL">Sell</option>
            </select>
          )}
        </Field>
        <Field label="From">{(p) => <input {...p} className="input" type="date" value={draft.date_from} onChange={set("date_from")} />}</Field>
        <Field label="To">{(p) => <input {...p} className="input" type="date" value={draft.date_to} onChange={set("date_to")} />}</Field>
        <button type="submit" className="btn btn--secondary">Apply</button>
        {filtered && (
          <button type="button" className="btn btn--link" onClick={clearFilters}>
            Clear filters
          </button>
        )}
      </form>

      {exportError && (
        <div className="alert" role="alert" style={{ margin: "0 var(--space-4) var(--space-4)" }}>
          Export failed: {exportError}
        </div>
      )}

      <div aria-live="polite" aria-busy={loading}>
        {loading && !data && <LoadingState label="Loading transactions…" />}
        {error && <ErrorState error={error} onRetry={reload} title="Couldn't load transactions" />}
        {data && !error && transactions.length === 0 && (
          filtered ? (
            <EmptyState title="No trades match these filters" action={<button type="button" className="btn btn--secondary" onClick={clearFilters}>Clear filters</button>}>
              Try a different instrument or date range.
            </EmptyState>
          ) : (
            <EmptyState title="No trades yet" action={<button type="button" className="btn btn--primary" onClick={onAdd}>Record the first trade</button>}>
              Add a buy to start building this portfolio's holdings.
            </EmptyState>
          )
        )}
        {data && !error && transactions.length > 0 && (
          <TransactionTable transactions={transactions} currency={currency} sort={sort} order={order} onSort={handleSort} onDelete={onDelete} />
        )}
      </div>

      {meta && meta.total > 0 && (
        <div className="pager">
          <span>
            Page {meta.page} of {meta.pages} · {meta.total} {meta.total === 1 ? "trade" : "trades"}
          </span>
          <div className="pager__btns">
            <button type="button" className="btn btn--secondary btn--sm" disabled={meta.page <= 1} onClick={() => setPage(page - 1)}>
              Previous
            </button>
            <button type="button" className="btn btn--secondary btn--sm" disabled={meta.page >= meta.pages} onClick={() => setPage(page + 1)}>
              Next
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
