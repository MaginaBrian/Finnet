import { formatDate, formatMoney, formatPrice, formatQuantity } from "../utils/format";

const COLUMNS = [
  { key: "trade_date", label: "Date" },
  { key: "instrument", label: "Instrument" },
  { key: "type", label: "Type" },
  { key: "quantity", label: "Quantity", numeric: true },
  { key: "unit_price", label: "Unit price", numeric: true },
];

function SortHeader({ column, sort, order, onSort }) {
  const active = sort === column.key;
  const ariaSort = active ? (order === "asc" ? "ascending" : "descending") : "none";
  return (
    <th scope="col" className={column.numeric ? "num" : undefined} aria-sort={ariaSort}>
      <button type="button" className="sort-btn" onClick={() => onSort(column.key)}>
        {column.label}
        <span aria-hidden="true">{active ? (order === "asc" ? "▲" : "▼") : "↕"}</span>
      </button>
    </th>
  );
}

export default function TransactionTable({ transactions, currency, sort, order, onSort, onDelete }) {
  return (
    <div className="table-wrap">
      <table className="table">
        <caption className="visually-hidden">Transactions in {currency}. Use the column buttons to sort.</caption>
        <thead>
          <tr>
            {COLUMNS.map((c) => (
              <SortHeader key={c.key} column={c} sort={sort} order={order} onSort={onSort} />
            ))}
            <th scope="col" className="num">Total</th>
            <th scope="col"><span className="visually-hidden">Actions</span></th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((t) => (
            <tr key={t.id}>
              <td>{formatDate(t.trade_date)}</td>
              <th scope="row">{t.instrument}</th>
              <td><span className="tag">{t.type}</span></td>
              <td className="num">{formatQuantity(t.quantity)}</td>
              <td className="num">{formatPrice(t.unit_price)}</td>
              <td className="num">{formatMoney(t.total, currency)}</td>
              <td>
                <button type="button" className="btn btn--secondary btn--sm" onClick={() => onDelete(t)}>
                  Delete<span className="visually-hidden"> {t.type} {t.instrument} on {formatDate(t.trade_date)}</span>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
